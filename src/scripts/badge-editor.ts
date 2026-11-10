import { setBadgeFaces } from './badge-editor-state';
import { initPortraitCrop, loadPortrait, savePortrait } from './badge-portrait';

type Edits = Record<string, string>;
const width = 1200;
const height = 1688;

export function initBadgeEditor(): void {
  const dialog = document.querySelector<HTMLDialogElement>('[data-badge-editor]');
  const triggers = Array.from(document.querySelectorAll<HTMLButtonElement>('[data-edit-pass], [data-open-customize]'));
  const trigger = triggers[0];
  const setTriggersDisabled = (disabled: boolean) => triggers.forEach(button => { button.disabled = disabled; });
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
  const versionStorageKey = 'crew-pass-version-v1';
  type Version = 'original' | 'chibi' | 'tangbao' | 'liangsheng';
  const specialVersion = character === 'deepseek' ? 'liangsheng' : 'tangbao';
  const requestedParam = new URL(location.href).searchParams.get('version');
  const requestedVersion: Version | null = requestedParam === 'original' || requestedParam === 'chibi' || (requestedParam === 'tangbao' && character === 'doubao') || (requestedParam === 'liangsheng' && character === 'deepseek') ? requestedParam as Version : null;
  let version: Version = 'original';
  try { if (!requestedVersion && localStorage.getItem(versionStorageKey) === 'chibi') version = 'chibi'; } catch { /* Use the original when storage is unavailable. */ }
  let appliedVersion: Version = version;
  const versionButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('[data-badge-version]'));
  const versionStatus = document.querySelector<HTMLElement>('[data-version-status]');
  const portrait = artwork.querySelector<HTMLImageElement>('.badge-portrait img')!;
  const portraitReset = dialog.querySelector<HTMLButtonElement>('[data-portrait-reset]')!;
  const portraitStorageKey = `${character}:${locale}`;
  let customPortrait: string | null = null;
  let customActive = false;
  let appliedCustomPortrait: string | null = null;
  let appliedCustomActive = false;
  let portraitStoragePending = false;
  let assetsReady: Promise<void> | undefined;
  const setArtworkVersion = (value: Version) => {
    version = value;
    artwork.dataset.version = value;
    artwork.toggleAttribute('data-custom-portrait', (customActive && !!customPortrait) || value === 'tangbao' || value === 'liangsheng');
    portrait.dataset.printSrc = customActive && customPortrait ? customPortrait : value === 'tangbao' ? dialog.querySelector<HTMLElement>('[data-portrait-example]')!.dataset.exampleSrc : value === 'liangsheng' ? page.dataset.liangshengPortrait : value === 'chibi' ? portrait.dataset.chibiSrc : portrait.dataset.originalSrc;
    if (portrait.src) portrait.src = portrait.dataset.printSrc!;
    versionButtons.forEach(button => {
      const option = button.dataset.badgeVersion;
      if (option === 'custom') button.hidden = !customPortrait;
      button.setAttribute('aria-pressed', String(option === (customActive ? 'custom' : value)));
    });
    portraitReset.hidden = !customPortrait;
    assetsReady = undefined;
  };
  setArtworkVersion(version);
  const fields = new Map<string, HTMLElement>();
  const originals: Edits = {};
  let selected: HTMLElement | null = null;
  let edits: Edits = {};
  let normalEdits: Edits = {};
  let specialEdits: Edits = {};
  let applied = '{}';
  let busy = false;
  let urls: string[] = [];

  const portraitCrop = initPortraitCrop(dialog, en, image => {
    customPortrait = image;
    customActive = true;
    setArtworkVersion(version);
    status.textContent = en ? 'Portrait cropped. Finish editing to apply it.' : '角色图片已裁剪，完成编辑后生效。';
  }, () => busy);
  portraitReset.addEventListener('click', () => {
    customPortrait = null;
    customActive = false;
    setArtworkVersion(version);
    status.textContent = en ? 'Original portrait restored. Finish editing to apply.' : '已恢复原角色，完成编辑后生效。';
  });

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

  try {
    const stored: unknown = JSON.parse(localStorage.getItem(`${storageKey}:${specialVersion}`) || '{}');
    if (stored && typeof stored === 'object' && !Array.isArray(stored)) {
      for (const [key, value] of Object.entries(stored)) {
        if (fields.has(key) && typeof value === 'string') specialEdits[key] = value;
      }
    }
  } catch { /* Editing remains available for this visit. */ }

  const paintField = (field: HTMLElement, key: string, value: string) => {
    field.textContent = value;
    field.toggleAttribute('data-edit-empty', !!originals[key] && !value);
  };
  const tangbaoText: Edits = en ? {
    'front:brand': 'Doubao', 'front:name': 'Tangbao', 'front:alias': '', 'front:role': 'Joy Department / Red Scarf Envoy',
    'front:motto-0': 'Lots of ideas, and just a little drool...', 'front:motto-1': 'Let’s make today a happy one!',
    'back:brand': 'Doubao', 'back:title-0': 'Scarf on,', 'back:title-1': 'joy incoming.',
    'back:feature-0': 'Short brown hair · red scarf', 'back:feature-1': 'A dreamy look · a little drool', 'back:feature-2': 'Tangbao edition · unofficial fan art', 'back:catchphrase': '“Aba aba aba”',
  } : {
    'front:brand': '豆包', 'front:name': '糖包', 'front:alias': 'Tangbao', 'front:role': '快乐摸鱼部 / 红围巾特派员',
    'front:motto-0': '想法有点多，口水有一点点……', 'front:motto-1': '今天也请多多关照！',
    'back:brand': '豆包', 'back:title-0': '围巾围好，', 'back:title-1': '快乐报到。',
    'back:feature-0': '棕色短发 · 红色长围巾', 'back:feature-1': '呆萌表情 · 口水闪亮登场', 'back:feature-2': '糖包限定 · 非官方趣味形象', 'back:catchphrase': '“阿巴阿巴阿巴”',
  };
  const liangshengText: Edits = en ? {
    'front:name': 'Liang Sheng', 'front:alias': '', 'front:role': 'Deep Exploration / Whale Guardian',
    'front:motto-0': 'Open ideas travel far.', 'front:motto-1': 'Shh, deep thinking in progress.',
    'back:title-0': 'Liang Sheng arrives,', 'back:title-1': 'the whale rejoices.',
    'back:feature-0': 'Blue suit · a quiet entrance', 'back:feature-1': 'Deep exploration · open ideas', 'back:feature-2': 'Liang Sheng · unofficial fan art',
    'back:catchphrase-label': 'Community meme', 'back:catchphrase': '“Thank you, Liang Sheng!”',
  } : {
    'front:name': '梁圣', 'front:alias': 'Liang Sheng', 'front:role': '深度求索部 / 大肥鱼守护者',
    'front:motto-0': '开源的风吹向远方，', 'front:motto-1': '嘘，正在深度思考。',
    'back:title-0': '梁圣一出，', 'back:title-1': '大肥鱼有福了。',
    'back:feature-0': '蓝色西装 · 嘘声登场', 'back:feature-1': '深度求索 · 开源探索', 'back:feature-2': '肌肉梁圣 · 非官方趣味形象',
    'back:catchphrase-label': '社区梗', 'back:catchphrase': '“梁圣的恩情还不完！”',
  };
  const specialText = () => version === 'tangbao' ? tangbaoText : version === 'liangsheng' ? liangshengText : undefined;
  const paintText = () => fields.forEach((field, key) => paintField(field, key, edits[key] ?? specialText()?.[key] ?? originals[key]));
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
    if (value === (specialText()?.[key] ?? originals[key])) delete edits[key];
    else edits[key] = value;
    paintField(selected, key, value);
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
  const versionSuffix = () => customActive ? '-custom' : version === 'tangbao' ? '-tangbao' : version === 'liangsheng' ? '-liangsheng' : version === 'chibi' ? '-chibi' : '';
  const publish = (result: { front: string; back: string; zip: string } | null) => {
    const chibi = !customActive && version === 'chibi';
    const staticLink = (url: string, face: string) => chibi && face !== 'back'
      ? url.replace(face === 'front' ? '-front.png' : '-crew-pass.zip', face === 'front' ? '-chibi-front.png' : '-chibi-crew-pass.zip') : url;
    downloadLinks.forEach((link, index) => {
      const face = link.dataset.downloadFace || 'zip';
      link.href = result ? result[face as keyof typeof result] : staticLink(originalLinks[index], face);
      link.download = `${character}-${locale}${versionSuffix()}-${face === 'zip' ? 'crew-pass.zip' : `${face}.png`}`;
    });
    previews.forEach((image, index) => { image.src = result ? result[image.dataset.printPreview as 'front' | 'back'] : chibi && image.dataset.printPreview === 'front' ? originalPreviews[index].replace('-front.webp', '-chibi-front.webp') : originalPreviews[index]; });
    downloadTrigger.href = result?.zip || staticLink(originalLinks.find((_, index) => downloadLinks[index].hasAttribute('data-download-zip'))!, 'zip');
    const preview = document.querySelector<HTMLImageElement>('.badge-loading-preview img');
    if (preview) preview.src = result?.front || (chibi ? page.dataset.chibiFront! : originalPreviews[previews.findIndex(image => image.dataset.printPreview === 'front')]);
    setBadgeFaces(result ? { front: result.front, back: result.back } : chibi ? { front: page.dataset.chibiFront!, back: page.dataset.originalBack! } : null);
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
      field.removeAttribute('data-edit-empty');
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
        result[`${character}-${locale}${versionSuffix()}-${side}.png`] = new Uint8Array(await blob.arrayBuffer());
      }
      return { images, zip: new Blob([zipSync(result, { level: 0 })], { type: 'application/zip' }) };
    } finally { clone.remove(); }
  };

  const findOverflow = (): string | null => {
    const clone = scene.cloneNode(false) as HTMLElement;
    clone.append(artwork.cloneNode(true));
    clone.style.cssText = 'position:fixed!important;left:-10000px!important;top:0!important;transform:none!important';
    clone.querySelectorAll('[data-edit-empty]').forEach(field => field.removeAttribute('data-edit-empty'));
    document.body.append(clone);
    try {
      for (const side of ['front', 'back']) {
        clone.querySelectorAll<HTMLElement>('[data-badge-face]').forEach(face => { face.hidden = face.dataset.badgeFace !== side; });
        const face = clone.querySelector<HTMLElement>(`[data-badge-face="${side}"]`)!;
        const elements = Array.from(face.querySelectorAll<HTMLElement>('[data-edit-field]'));
        const measure = () => elements.map(element => {
          const range = document.createRange();
          range.selectNodeContents(element);
          return range.getBoundingClientRect();
        });
        const current = measure();
        elements.forEach(element => { element.textContent = originals[`${side}:${element.dataset.editField}`]; });
        const original = measure();
        const bounds = face.getBoundingClientRect();
        const overlaps = (a: DOMRect, b: DOMRect) => a.width > 0 && a.height > 0 && b.width > 0 && b.height > 0 &&
          Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1;
        for (let i = 0; i < elements.length; i++) {
          const key = `${side}:${elements[i].dataset.editField}`;
          if (!(key in edits) || !current[i].width) continue;
          const rect = current[i];
          if (rect.left < bounds.left - 1 || rect.right > bounds.right + 1 || rect.top < bounds.top - 1 || rect.bottom > bounds.bottom + 1) return key;
          for (let j = 0; j < elements.length; j++) {
            if (i !== j && overlaps(rect, current[j]) && !overlaps(original[i], original[j])) return key;
          }
        }
      }
      return null;
    } finally { clone.remove(); }
  };

  const apply = async (close: boolean) => {
    if (busy) return false;
    if (close && portraitCrop.isLoading()) {
      status.textContent = en ? 'Image is loading. Please wait and finish cropping.' : '图片正在读取，请稍候并完成裁剪。';
      return false;
    }
    if (close) portraitCrop.cancelPending();
    const unchanged = JSON.stringify(edits) === applied && version === appliedVersion && customPortrait === appliedCustomPortrait && customActive === appliedCustomActive;
    if (unchanged && !portraitStoragePending) { if (close) dialog.close(); return true; }
    const retryingSave = unchanged && portraitStoragePending;
    const overflow = findOverflow();
    if (overflow) {
      scene.append(artwork);
      if (!dialog.open) dialog.showModal();
      const [side] = overflow.split(':');
      dialog.querySelector<HTMLButtonElement>(`[data-edit-side="${side}"]`)?.click();
      fields.get(overflow)?.click();
      status.textContent = en ? 'Text overlaps or extends beyond the pass. Please shorten it before finishing.' : '文字超出卡面或与其他内容重叠，请缩短后再完成编辑。';
      return false;
    }
    busy = true;
    dialog.querySelectorAll<HTMLButtonElement>('button').forEach(button => { button.disabled = true; });
    input.disabled = true;
    setTriggersDisabled(true);
    downloadTrigger.setAttribute('aria-disabled', 'true');
    versionButtons.forEach(button => { button.disabled = true; });
    status.textContent = en ? 'Preparing your edited pass…' : '正在生成编辑后的工牌…';
    try {
      const previousUrls = urls;
      if (Object.keys(edits).length || customActive || version === specialVersion) {
        const result = await render();
        const front = URL.createObjectURL(result.images.front);
        const back = URL.createObjectURL(result.images.back);
        const zip = URL.createObjectURL(result.zip);
        urls = [front, back, zip];
        publish({ front, back, zip });
      } else { urls = []; publish(null); }
      // Let consumers release the previous texture before revoking its URL.
      window.setTimeout(() => previousUrls.forEach(url => URL.revokeObjectURL(url)), 1000);
      let portraitSaveFailed = false;
      if (customPortrait !== appliedCustomPortrait || customActive !== appliedCustomActive || portraitStoragePending) {
        try {
          await savePortrait(portraitStorageKey, customPortrait ? { image: customPortrait, active: customActive } : null);
          portraitStoragePending = false;
        } catch { portraitSaveFailed = true; portraitStoragePending = true; }
      }
      applied = JSON.stringify(edits);
      appliedVersion = version;
      appliedCustomPortrait = customPortrait;
      appliedCustomActive = customActive;
      try {
        const activeStorageKey = version === specialVersion ? `${storageKey}:${specialVersion}` : storageKey;
        if (Object.keys(edits).length) localStorage.setItem(activeStorageKey, applied);
        else localStorage.removeItem(activeStorageKey);
      } catch { /* The edited pass still works for this visit. */ }
      status.textContent = portraitSaveFailed
        ? (en ? 'The pass is ready, but the portrait could not be saved. Finish again to retry or continue for this visit.' : '工牌已生效，但角色图片未能保存在浏览器中；再次完成可重试或继续本次使用。')
        : (en ? 'Your edited pass is ready.' : '编辑后的工牌已生效。');
      if (versionStatus) versionStatus.textContent = portraitSaveFailed
        ? (en ? 'Selection was not saved. Open Customize and finish to retry.' : '选择未能保存，可打开自定义并完成来重试。') : '';
      if (close && (!portraitSaveFailed || retryingSave)) dialog.close();
      return true;
    } catch (error) {
      console.error('Could not generate edited crew pass', error);
      status.textContent = en ? 'Could not generate the pass. Please try again.' : '生成工牌失败，请重试；已输入的文字还在。';
      scene.append(artwork);
      if (!dialog.open) dialog.showModal();
      return false;
    } finally {
      busy = false;
      setTriggersDisabled(false);
      downloadTrigger.removeAttribute('aria-disabled');
      versionButtons.forEach(button => { button.disabled = false; });
      dialog.querySelectorAll<HTMLButtonElement>('button').forEach(button => { button.disabled = false; });
      input.disabled = !selected;
    }
  };

  const pageTitle = document.querySelector<HTMLElement>('.ocean-note__title');
  const pageCaption = document.querySelector<HTMLElement>('.ocean-note__caption');
  if (pageTitle) pageTitle.dataset.originalTitle = pageTitle.innerHTML;
  if (pageCaption) pageCaption.dataset.originalCaption = pageCaption.textContent || '';
  triggers.forEach(button => { button.hidden = false; });
  setTriggersDisabled(true);
  versionButtons.forEach(button => { button.disabled = true; });
  publish(null);
  versionButtons.forEach(button => button.addEventListener('click', async () => {
    const next = button.dataset.badgeVersion as Version | 'custom';
    if (busy || (next === 'custom' ? customActive || !customPortrait : !customActive && next === version)) return;
    const previous = version;
    const previouslyCustom = customActive;
    versionButtons.forEach(item => { item.disabled = true; });
    if (versionStatus) versionStatus.textContent = en ? 'Loading…' : '正在切换…';
    try {
      if (next === 'chibi') {
        const image = new Image();
        image.src = page.dataset.chibiFront!;
        await image.decode();
      }
      if (previous === specialVersion) specialEdits = edits; else normalEdits = edits;
      edits = next === specialVersion ? specialEdits : normalEdits;
      customActive = next === 'custom';
      setArtworkVersion(next === 'custom' ? (version === specialVersion ? 'original' : version) : next);
      paintText();
      if (!(await apply(false))) { customActive = previouslyCustom; setArtworkVersion(previous); edits = previous === specialVersion ? specialEdits : normalEdits; paintText(); if (versionStatus) versionStatus.textContent = ''; return; }
      if (next !== 'custom' && next !== specialVersion) {
        try { localStorage.setItem(versionStorageKey, next); } catch { /* Keep the selection for this visit. */ }
      }
      const currentUrl = new URL(location.href);
      currentUrl.searchParams.set('version', next === 'custom' ? 'original' : next);
      history.replaceState(history.state, '', currentUrl);
      if (versionStatus && !portraitStoragePending) versionStatus.textContent = '';
      const title = document.querySelector<HTMLElement>('.ocean-note__title');
      const caption = document.querySelector<HTMLElement>('.ocean-note__caption');
      if (title && caption) {
        title.innerHTML = version === 'tangbao' && !customActive ? (en ? 'Scarf on,<br>joy incoming.' : '围巾围好，<br>快乐报到。') : version === 'liangsheng' && !customActive ? (en ? 'Liang Sheng arrives,<br>the whale rejoices.' : '梁圣一出，<br>大肥鱼有福了。') : title.dataset.originalTitle!;
        caption.textContent = version === 'tangbao' && !customActive ? (en ? 'A red scarf for a brighter day.' : '红围巾一戴，今天也要开开心心。') : version === 'liangsheng' && !customActive ? (en ? 'Shh, let the whale think.' : '嘘，先让大肥鱼思考一下。') : caption.dataset.originalCaption!;
      }
    } catch (error) {
      console.error('Could not load Q-version pass', error);
      customActive = previouslyCustom;
      setArtworkVersion(previous);
      edits = previous === specialVersion ? specialEdits : normalEdits;
      paintText();
      if (versionStatus) versionStatus.textContent = en ? 'Could not load. Try again.' : '加载失败，请重试。';
    } finally { versionButtons.forEach(item => { item.disabled = false; }); }
  }));
  triggers.forEach(button => button.addEventListener('click', () => {
    const download = document.querySelector<HTMLDialogElement>('[data-download-dialog]');
    if (download?.open) download.close();
    scene.append(artwork);
    if (!dialog.open) dialog.showModal();
    void loadAssets().catch(() => { status.textContent = en ? 'Artwork failed to load. Finish editing to retry.' : '卡面素材加载失败，完成编辑时会重试。'; });
  }));
  dialog.querySelector('[data-edit-done]')?.addEventListener('click', () => { void apply(true); });
  dialog.querySelector('[data-edit-close]')?.addEventListener('click', () => { void apply(true); });
  dialog.addEventListener('cancel', event => { event.preventDefault(); void apply(true); });
  void (async () => {
    try {
      const stored = await loadPortrait(portraitStorageKey);
      if (stored) {
        customPortrait = stored.image;
        customActive = requestedVersion ? false : stored.active;
        appliedCustomPortrait = stored.image;
        setArtworkVersion(version);
      }
    } catch { /* Portrait editing remains available for this visit. */ }
    if (Object.keys(edits).length || customActive) await apply(false);
    else { setTriggersDisabled(false); versionButtons.forEach(button => { button.disabled = false; }); }
    if (requestedVersion && requestedVersion !== version) {
      versionButtons.find(button => button.dataset.badgeVersion === requestedVersion)?.click();
    }
  })();
}
