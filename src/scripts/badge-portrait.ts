export type StoredPortrait = { image: string; active: boolean };

const databaseName = 'crew-pass-portraits-v1';
const storeName = 'portraits';

function openPortraitDatabase(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(databaseName, 1);
    let blocked = false;
    request.onupgradeneeded = () => request.result.createObjectStore(storeName);
    request.onerror = () => reject(request.error);
    request.onblocked = () => { blocked = true; reject(new Error('Portrait storage is blocked')); };
    request.onsuccess = () => { if (blocked) request.result.close(); else resolve(request.result); };
  });
}

export async function loadPortrait(key: string): Promise<StoredPortrait | null> {
  const db = await openPortraitDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(storeName, 'readonly');
    const request = transaction.objectStore(storeName).get(key);
    let value: unknown;
    request.onsuccess = () => { value = request.result; };
    transaction.oncomplete = () => {
      db.close();
      const portrait = value as Partial<StoredPortrait> | undefined;
      resolve(portrait && typeof portrait.image === 'string' && portrait.image.startsWith('data:image/png;base64,')
        ? { image: portrait.image, active: portrait.active === true } : null);
    };
    transaction.onabort = transaction.onerror = () => { db.close(); reject(transaction.error); };
  });
}

export async function savePortrait(key: string, portrait: StoredPortrait | null): Promise<void> {
  const db = await openPortraitDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(storeName, 'readwrite');
    const store = transaction.objectStore(storeName);
    if (portrait) store.put(portrait, key); else store.delete(key);
    transaction.oncomplete = () => { db.close(); resolve(); };
    transaction.onabort = transaction.onerror = () => { db.close(); reject(transaction.error); };
  });
}

export function initPortraitCrop(editor: HTMLDialogElement, en: boolean, onApply: (image: string) => void, isBusy: () => boolean): { isLoading: () => boolean; cancelPending: () => void } {
  const fileInput = editor.querySelector<HTMLInputElement>('[data-portrait-file]')!;
  const upload = editor.querySelector<HTMLButtonElement>('[data-edit-upload]')!;
  const examples = editor.querySelectorAll<HTMLButtonElement>('[data-portrait-example]');
  const status = editor.querySelector<HTMLElement>('[data-edit-status]')!;
  const dialog = document.querySelector<HTMLDialogElement>('[data-portrait-crop]')!;
  const canvas = dialog.querySelector<HTMLCanvasElement>('[data-crop-canvas]')!;
  const zoom = dialog.querySelector<HTMLInputElement>('[data-crop-zoom]')!;
  const cropStatus = dialog.querySelector<HTMLElement>('[data-crop-status]')!;
  let source: HTMLImageElement | null = null;
  let centerX = 0;
  let centerY = 0;
  let loading = 0;
  let imageLoading = false;
  let drag: { x: number; y: number; centerX: number; centerY: number; size: number; width: number } | null = null;

  const cropSize = () => source ? Math.min(source.naturalWidth, source.naturalHeight) / Number(zoom.value) : 0;
  const clampCenter = () => {
    if (!source) return;
    const half = cropSize() / 2;
    centerX = Math.max(half, Math.min(source.naturalWidth - half, centerX));
    centerY = Math.max(half, Math.min(source.naturalHeight - half, centerY));
  };
  const draw = (target: HTMLCanvasElement) => {
    if (!source) return;
    clampCenter();
    const size = cropSize();
    const context = target.getContext('2d');
    if (!context) throw new Error('Canvas is unavailable');
    context.clearRect(0, 0, target.width, target.height);
    context.drawImage(source, centerX - size / 2, centerY - size / 2, size, size, 0, 0, target.width, target.height);
  };
  const showError = (message: string) => { status.textContent = message; };

  const cancelPending = () => { loading++; imageLoading = false; };
  editor.addEventListener('close', cancelPending);
  upload.addEventListener('click', () => fileInput.click());
  const openImage = async (url: string, token: number, revoke: boolean, isExample: boolean) => {
    imageLoading = true;
    status.textContent = en ? 'Loading image…' : '正在读取图片…';
    try {
      const image = new Image();
      image.src = url;
      await image.decode();
      if (token !== loading || !editor.open || isBusy()) return;
      if (!image.naturalWidth || !image.naturalHeight || image.naturalWidth * image.naturalHeight > 40000000) {
        throw new Error('Invalid image dimensions');
      }
      source = image;
      centerX = image.naturalWidth / 2;
      centerY = image.naturalHeight / 2;
      zoom.value = '1';
      cropStatus.textContent = '';
      status.textContent = '';
      draw(canvas);
      dialog.showModal();
      canvas.focus();
    } catch {
      if (token === loading && editor.open && !isBusy()) showError(isExample
        ? (en ? 'Could not load the sample image. Try again.' : '示例图片加载失败，请重试。')
        : (en ? 'Could not open this image. Try another image.' : '无法读取这张图片，请换一张图片重试。'));
    } finally {
      if (token === loading) imageLoading = false;
      if (revoke) URL.revokeObjectURL(url);
    }
  };
  examples.forEach(example => example.addEventListener('click', () => {
    if (!editor.open || isBusy()) return;
    void openImage(example.dataset.exampleSrc!, ++loading, false, true);
  }));
  fileInput.addEventListener('change', () => {
    const file = fileInput.files?.[0];
    fileInput.value = '';
    if (!file || !editor.open || isBusy()) return;
    const token = ++loading;
    imageLoading = false;
    if (!file.type.startsWith('image/')) {
      showError(en ? 'Choose an image file and try again.' : '请选择图片文件后重试。');
      return;
    }
    if (!file.size || file.size > 20 * 1024 * 1024) {
      showError(en ? 'Choose an image smaller than 20 MB.' : '请选择小于 20 MB 的图片。');
      return;
    }
    void openImage(URL.createObjectURL(file), token, true, false);
  });

  zoom.addEventListener('input', () => draw(canvas));
  canvas.addEventListener('pointerdown', event => {
    if (!source || event.button !== 0) return;
    event.preventDefault();
    canvas.setPointerCapture(event.pointerId);
    drag = { x: event.clientX, y: event.clientY, centerX, centerY, size: cropSize(), width: canvas.getBoundingClientRect().width };
  });
  canvas.addEventListener('pointermove', event => {
    if (!drag) return;
    centerX = drag.centerX - (event.clientX - drag.x) * drag.size / drag.width;
    centerY = drag.centerY - (event.clientY - drag.y) * drag.size / drag.width;
    draw(canvas);
  });
  canvas.addEventListener('pointerup', () => { drag = null; });
  canvas.addEventListener('pointercancel', () => { drag = null; });
  canvas.addEventListener('keydown', event => {
    const delta = cropSize() * (event.shiftKey ? .01 : .05);
    if (event.key === 'ArrowLeft') centerX += delta;
    else if (event.key === 'ArrowRight') centerX -= delta;
    else if (event.key === 'ArrowUp') centerY += delta;
    else if (event.key === 'ArrowDown') centerY -= delta;
    else return;
    event.preventDefault();
    draw(canvas);
  });
  dialog.querySelector<HTMLButtonElement>('[data-crop-cancel]')!.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { source = null; drag = null; });
  dialog.querySelector<HTMLButtonElement>('[data-crop-apply]')!.addEventListener('click', () => {
    if (!source) return;
    try {
      const output = document.createElement('canvas');
      output.width = output.height = 1024;
      draw(output);
      onApply(output.toDataURL('image/png'));
      dialog.close();
    } catch {
      cropStatus.textContent = en ? 'Could not crop this image. Try another image.' : '裁剪失败，请换一张图片重试。';
    }
  });
  return { isLoading: () => imageLoading, cancelPending };
}
