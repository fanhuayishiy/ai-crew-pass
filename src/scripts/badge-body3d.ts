import {
  Color, DoubleSide, ExtrudeGeometry, Group,
  Mesh, MeshBasicMaterial, PerspectiveCamera, Path, Scene, Shape,
  SRGBColorSpace, WebGLRenderer,
} from 'three';

export type BadgeBody3D = {
  setViewport(width: number, height: number, cardWidth: number, cardHeight: number, holeOffset: number): void;
  update(x: number, y: number, rotation: number, tiltX: number, tiltY: number, flip: number, visible: boolean): void;
};

/** A bevelled, solid card behind the accessible printed DOM faces.
 * Uses the same centre, hole pivot, rotation and flip as the original rope rig.
 * There is no second animation loop: physics renders the body when it renders the strap.
 */
export function createBadgeBody3D(canvas: HTMLCanvasElement, color: string): BadgeBody3D {
  const renderer = new WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setClearColor(0, 0);
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  const scene = new Scene();
  const camera = new PerspectiveCamera(40, 1, 0.1, 4000);
  const CSS_PERSPECTIVE = 1400;
  let viewportWidth = 1, viewportHeight = 1;
  let baseProjection = camera.projectionMatrix.clone();
  camera.position.set(0, 0, CSS_PERSPECTIVE);
  camera.lookAt(0, 0, 0);
  // The visible print stays bright. Use a pale substrate for the thin exposed
  // edge, avoiding the black, phone-case-like rim of the earlier glossy body.
  const cap = new MeshBasicMaterial({ color: new Color(color).lerp(new Color('#ffffff'), 0.85), side: DoubleSide });
  const edge = new MeshBasicMaterial({ color: new Color(color).lerp(new Color('#ffffff'), 0.6), side: DoubleSide });
  const root = new Group();
  const pivot = new Group();
  root.add(pivot);
  scene.add(root);
  const mesh = new Mesh(new ExtrudeGeometry(), [cap, edge]);
  pivot.add(mesh);
  canvas.dataset.depth = '3';

  return {
    setViewport(width, height, cardWidth, cardHeight, holeOffset) {
      renderer.setSize(width, height);
      viewportWidth = width;
      viewportHeight = height;
      camera.aspect = width / height;
      camera.fov = 2 * Math.atan(height / (2 * CSS_PERSPECTIVE)) * 180 / Math.PI;
      camera.updateProjectionMatrix();
      baseProjection = camera.projectionMatrix.clone();
      baseProjection.elements[5] *= -1; // CSS coordinates grow downwards.
      const w = cardWidth - 1, h = cardHeight - 1, r = 12;
      const left = -w / 2, top = -h / 2;
      const shape = new Shape();
      shape.moveTo(left + r, top);
      shape.lineTo(left + w - r, top);
      shape.quadraticCurveTo(left + w, top, left + w, top + r);
      shape.lineTo(left + w, top + h - r);
      shape.quadraticCurveTo(left + w, top + h, left + w - r, top + h);
      shape.lineTo(left + r, top + h);
      shape.quadraticCurveTo(left, top + h, left, top + h - r);
      shape.lineTo(left, top + r);
      shape.quadraticCurveTo(left, top, left + r, top);
      const hole = new Path();
      hole.absarc(0, -cardHeight / 2 + holeOffset, 5.5, 0, Math.PI * 2, true);
      shape.holes.push(hole);
      const geometry = new ExtrudeGeometry(shape, { depth: 2, bevelEnabled: true, bevelSize: 0.3, bevelThickness: 0.5, bevelSegments: 3, steps: 1, curveSegments: 18 });
      geometry.translate(0, 0, -2.5);
      mesh.geometry.dispose();
      mesh.geometry = geometry;
      pivot.position.y = -cardHeight / 2 + holeOffset;
      mesh.position.y = cardHeight / 2 - holeOffset;
    },
    update(x, y, rotation, tiltX, tiltY, flip, visible) {
      canvas.hidden = !visible;
      if (!visible) return;
      const radians = Math.PI / 180;
      // Each badge establishes its own CSS perspective origin at its centre.
      // Match that lens rather than using a viewport-wide orthographic projection.
      camera.position.set(x, y, CSS_PERSPECTIVE);
      camera.lookAt(x, y, 0);
      camera.projectionMatrix.copy(baseProjection);
      camera.projectionMatrix.elements[8] = 1 - 2 * x / viewportWidth;
      camera.projectionMatrix.elements[9] = 2 * y / viewportHeight - 1;
      camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
      root.position.set(x, y, 0);
      root.rotation.z = rotation * radians;
      pivot.rotation.set(tiltX * radians, (tiltY + flip) * radians, 0, 'XYZ');
      renderer.render(scene, camera);
      canvas.dataset.triangles = String(renderer.info.render.triangles);
      canvas.dataset.flip = flip.toFixed(2);
    },
  };
}
