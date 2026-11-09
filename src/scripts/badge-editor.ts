import { setBadgeFaces } from './badge-editor-state';

type Edits = Record<string, string>;
const width = 1200;
const height = 1688;

export function initBadgeEditor(): void {
  const dialog = document.querySelector<HTMLDialogElement>('[data-badge-editor]');
  const trigger = document.querySelector<HTMLButtonElement>('[data-edit-pass]');
  const scene = dialog?.querySelector<HTMLElement>('[data-edit-scene]');
  const input = dialog?.querySelector<HTMLTextAreaElement>('[data-edit-text]');
  const status = dialog?.querySelector<HTMLElement>('[data-edit-status]');
  if (!dialog || !trigger || !scene || !input || !status) return;
  const template = scene.querySelector<HTMLTemplateElement>('[data-edit-artwork]')!;
  const artwork = document.importNode(template.content.querySelector<HTMLElement>('.badge-card')!, true);
  template.remove();
  const en = document.documentElement.lang === 'en';
  const page = document.querySelector<HTMLElement>('[data-character-id]')!;
  const character = page.dataset.characterId!;
  const locale = page.dataset.locale!;
  const storageKey = `crew-pass-edits-v1:${character}:${locale}`;
  const fields = new Map<string, HTMLElement>();
  const originals: Edits = {};
  let selected: HTMLElement | null = null;
  let edits: Edits = {};
  let applied = '{}';
  let busy = false;
  let urls: string[] = [];
  let assetsReady: Promise<void> | undefined;

  artwork.querySelectorAll<HTMLElement>('[data-edit-field]').forEach(field => {
    const side = field.closest<HTMLElement>('[data-badge-face]')!.dataset.badgeFace;
    const key = `${side}:${field.dataset.editField}`;
    fields.set(key, field);
    originals[key] = field.textContent || '';
    // Empty aliases have no visible text to select.
    if (!originals[key]) return;
    field.tabIndex = 0;
    field.setAttribute('role', 'button');
    field.setAttribute('aria-label', `${en ? 'Edit' : '编辑'}: ${originals[key]}`);
    const select = () => {
      if (busy) return;
      selected?.removeAttribute('data-edit-selected');
      selected = field;
      field.dataset.editSelected = '';
      input.disabled = false;
      input.value = field.textContent || '';
      const selection = dialog.querySelector<HTMLElement>('[data-edit-selection]');
      if (selection) selection.textContent = `${en ? 'Editing' : '正在编辑'}: ${originals[key]}`;
      input.focus();
      input.select();
    };
    field.addEventListener('click', select);
    field.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); select(); }
    });
  });

  try {
    const stored: unknown = JSON.parse(localStorage.getItem(storageKey) || '{}');
    if (stored && typeof stored === 'object' && !Array.isArray(stored)) {
      for (const [key, value] of Object.entries(stored)) {
        if (fields.has(key) && typeof value === 'string' && value !== originals[key]) edits[key] = value;
      }
    }
  } catch { /* Editing remains available when browser storage is blocked. */ }

  const paintText = () => fields.forEach((field, key) => { field.textContent = edits[key] ?? originals[key]; });
  paintText();

  const loadAssets = () => assetsReady ||= Promise.all([
    document.fonts.ready,
    ...Array.from(artwork.querySelectorAll<HTMLImageElement>('img[data-print-src]'), async image => {
      image.src = image.dataset.printSrc!;
      await image.decode();
    }),
  ]).then(() => undefined).catch(error => { assetsReady = undefined; throw error; });

  input.addEventListener('input', () => {
    if (!selected) return;
    const key = Array.from(fields).find(([, field]) => field === selected)![0];
    const value = input.value;
    if (value === originals[key]) delete edits[key];
    else edits[key] = value;
    selected.textContent = value;
    status.textContent = '';
  });
  dialog.querySelectorAll<HTMLButtonElement>('[data-edit-side]').forEach(button => {
    button.addEventListener('click', () => {
      artwork.querySelectorAll<HTMLElement>('[data-badge-face]').forEach(face => { face.hidden = face.dataset.badgeFace !== button.dataset.editSide; });
      dialog.querySelectorAll('[data-edit-side]').forEach(tab => tab.setAttribute('aria-pressed', String(tab === button)));
    });
  });
  dialog.querySelector('[data-edit-reset]')?.addEventListener('click', () => {
    edits = {};
    paintText();
    selected?.removeAttribute('data-edit-selected');
    selected = null;
    input.value = '';
    input.disabled = true;
    status.textContent = en ? 'Original text restored. Finish editing to apply.' : '已恢复原版文字，完成编辑后生效。';
  });

  const downloadDialog = document.querySelector('[data-download-dialog]')!;
  const downloadLinks = Array.from(downloadDialog.querySelectorAll<HTMLAnchorElement>('[data-download-face], [data-download-zip]'));
  const previews = Array.from(downloadDialog.querySelectorAll<HTMLImageElement>('[data-print-preview]'));
  const originalLinks = downloadLinks.map(link => link.href);
  const originalPreviews = previews.map(image => image.src);
  const downloadTrigger = document.querySelector<HTMLAnchorElement>('[data-download-pass]')!;
  downloadTrigger.addEventListener('click', event => {
    if (busy) { event.preventDefault(); event.stopImmediatePropagation(); }
  }, true);
  const publish = (result: { front: string; back: string; zip: string } | null) => {
    downloadLinks.forEach((link, index) => { link.href = result ? result[(link.dataset.downloadFace || 'zip') as keyof typeof result] : originalLinks[index]; });
    previews.forEach((image, index) => { image.src = result ? result[image.dataset.printPreview as 'front' | 'back'] : originalPreviews[index]; });
    const preview = document.querySelector<HTMLImageElement>('.badge-loading-preview img');
    if (preview) preview.src = result?.front || originalPreviews[previews.findIndex(image => image.dataset.printPreview === 'front')];
    setBadgeFaces(result ? { front: result.front, back: result.back } : null);
  };

  const render = async () => {
    await loadAssets();
    const [{ toCanvas }, { zipSync }] = await Promise.all([import('html-to-image'), import('fflate')]);
    const clone = scene.cloneNode(false) as HTMLElement;
    clone.append(artwork.cloneNode(true));
    clone.style.cssText = 'position:fixed!important;left:-10000px!important;top:0!important;transform:none!important';
    clone.querySelectorAll<HTMLElement>('[data-edit-field]').forEach(field => {
      field.removeAttribute('data-edit-field');
      field.removeAttribute('data-edit-selected');
      field.removeAttribute('tabindex');
    });
    document.body.append(clone);
    try {
      await Promise.all(Array.from(clone.querySelectorAll('img'), image => image.decode()));
      const result: Record<string, Uint8Array> = {};
      const images: Record<string, Blob> = {};
      for (const side of ['front', 'back']) {
        clone.querySelectorAll<HTMLElement>('[data-badge-face]').forEach(face => { face.hidden = face.dataset.badgeFace !== side; });
        const face = clone.querySelector<HTMLElement>(`[data-badge-face="${side}"]`)!;
        const rendered = await toCanvas(face, { width: 324, height: 455.625, pixelRatio: width / 324, preferredFontFormat: 'woff2' });
        const canvas = document.createElement('canvas');
        canvas.width = width; canvas.height = height;
        const context = canvas.getContext('2d')!;
        // The same raster feeds the hanging pass, fallback, previews and PNG/ZIP.
        context.beginPath();
        context.roundRect(0, 0, width, height, 50);
        context.clip();
        context.drawImage(rendered, 0, 0, width, height);
        context.globalCompositeOperation = 'destination-out';
        context.beginPath();
        context.roundRect(468, 64, 264, 48, 24);
        context.fill();
        const blob = await new Promise<Blob>((resolve, reject) => canvas.toBlob(value => value ? resolve(value) : reject(new Error('PNG export failed')), 'image/png'));
        images[side] = blob;
        result[`${character}-${locale}-${side}.png`] = new Uint8Array(await blob.arrayBuffer());
      }
      return { images, zip: new Blob([zipSync(result, { level: 0 })], { type: 'application/zip' }) };
    } finally { clone.remove(); }
  };

  const apply = async (close: boolean) => {
    if (busy) return;
    if (JSON.stringify(edits) === applied) { if (close) dialog.close(); return; }
    busy = true;
    dialog.querySelectorAll<HTMLButtonElement>('button').forEach(button => { button.disabled = true; });
    input.disabled = true;
    trigger.disabled = true;
    downloadTrigger.setAttribute('aria-disabled', 'true');
    status.textContent = en ? 'Preparing your edited pass…' : '正在生成编辑后的工牌…';
    try {
      const previousUrls = urls;
      if (Object.keys(edits).length) {
        const result = await render();
        const front = URL.createObjectURL(result.images.front);
        const back = URL.createObjectURL(result.images.back);
        const zip = URL.createObjectURL(result.zip);
        urls = [front, back, zip];
        publish({ front, back, zip });
      } else { urls = []; publish(null); }
      // Let consumers release the previous texture before revoking its URL.
      window.setTimeout(() => previousUrls.forEach(url => URL.revokeObjectURL(url)), 1000);
      applied = JSON.stringify(edits);
      try {
        if (Object.keys(edits).length) localStorage.setItem(storageKey, applied);
        else localStorage.removeItem(storageKey);
      } catch { /* The edited pass still works for this visit. */ }
      status.textContent = en ? 'Your edited pass is ready.' : '编辑后的工牌已生效。';
      if (close) dialog.close();
    } catch (error) {
      console.error('Could not generate edited crew pass', error);
      status.textContent = en ? 'Could not generate the pass. Please try again.' : '生成工牌失败，请重试；已输入的文字还在。';
      scene.append(artwork);
      if (!dialog.open) dialog.showModal();
    } finally {
      busy = false;
      trigger.disabled = false;
      downloadTrigger.removeAttribute('aria-disabled');
      dialog.querySelectorAll<HTMLButtonElement>('button').forEach(button => { button.disabled = false; });
      input.disabled = !selected;
    }
  };

  trigger.hidden = false;
  trigger.addEventListener('click', () => {
    scene.append(artwork);
    dialog.showModal();
    void loadAssets().catch(() => { status.textContent = en ? 'Artwork failed to load. Finish editing to retry.' : '卡面素材加载失败，完成编辑时会重试。'; });
  });
  dialog.querySelector('[data-edit-done]')?.addEventListener('click', () => { void apply(true); });
  dialog.addEventListener('cancel', event => { event.preventDefault(); void apply(true); });
  if (Object.keys(edits).length) void apply(false);
}
