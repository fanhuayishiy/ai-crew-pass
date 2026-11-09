export type BadgeFaces = { front: string; back: string };

let faces: BadgeFaces | null = null;

export const getBadgeFaces = () => faces;

export function setBadgeFaces(value: BadgeFaces | null): void {
  faces = value;
  window.dispatchEvent(new CustomEvent('badge-faces-updated', { detail: value }));
}
