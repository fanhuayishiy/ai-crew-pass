import { initBadgeSound } from './badge-sound';
import { initVisitCounter } from './visit-counter';

export function initPageEnhancements(): void {
  initBadgeSound();
  initVisitCounter();
  const motionButton = document.querySelector<HTMLButtonElement>('[data-motion-toggle]');
  const orientation = window.DeviceOrientationEvent as typeof DeviceOrientationEvent & {requestPermission?: () => Promise<string>};
  const motionAvailable = window.isSecureContext && matchMedia('(pointer: coarse)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (motionButton && motionAvailable && typeof orientation?.requestPermission === 'function') {
    motionButton.hidden = false;
    motionButton.addEventListener('click', async () => {
      try {
        if (await orientation.requestPermission!() === 'granted') motionButton.hidden = true;
        else {
          const hint = document.documentElement.lang === 'en' ? 'Check motion settings' : '请在设置中开启';
          motionButton.title = hint;
          motionButton.setAttribute('aria-label', hint);
          const label = motionButton.querySelector('span');
          if (label) label.textContent = hint;
        }
      } catch {
        const hint = document.documentElement.lang === 'en' ? 'Motion unavailable' : '运动权限不可用';
        motionButton.title = hint;
        motionButton.setAttribute('aria-label', hint);
        const label = motionButton.querySelector('span');
        if (label) label.textContent = hint;
      }
    });
  }
  const connection = (navigator as Navigator & { connection?: {saveData?: boolean;effectiveType?: string} }).connection;
  const canWarm = !connection?.saveData;
  const warmed = new Set<string>();
  const warm = async (link: HTMLElement, faces: string[] = ['front','back']) => {
    if (!canWarm || document.hidden) return;
    const base = link.dataset.textureBase;
    if (!base) return;
    for (const face of faces) {
      const url = `${base}-${face}.webp`;
      if (warmed.has(url)) continue;
      warmed.add(url);
      try {
        const response = await fetch(url, {cache:'force-cache',mode:'cors',credentials:'same-origin'});
        if (!response.ok) throw new Error('Prefetch failed');
        await response.arrayBuffer();
      } catch { warmed.delete(url); }
    }
  };
  document.querySelectorAll<HTMLElement>('[data-texture-base]').forEach(link => {
    link.addEventListener('pointerenter', () => warm(link), {passive:true});
    link.addEventListener('focus', () => warm(link));
    link.addEventListener('touchstart', () => warm(link), {passive:true});
  });
  // Open the first visit only after the current print has been painted.
  const stage = document.querySelector('.react-bits-stage');
  if (stage) {
    const backStatus = stage.querySelector<HTMLElement>('[data-badge-back-status]');
    let statusTimer = 0;
    let statusVisibleAt = 0;
    stage.addEventListener('badge-back-status', event => {
      if (!backStatus) return;
      const status = (event as CustomEvent<string>).detail;
      const en = document.documentElement.lang === 'en';
      clearTimeout(statusTimer);
      if (status === 'ready') {
        if (!backStatus.hidden) {
          backStatus.textContent = en ? 'Back ready' : '背面已就绪';
          statusTimer = window.setTimeout(() => { backStatus.hidden = true; }, Math.max(500, 800 - (performance.now() - statusVisibleAt)));
        }
      } else if (status === 'error') {
        backStatus.hidden = false;
        backStatus.textContent = en ? 'Back failed to load. Tap the pass to retry.' : '背面加载失败，点击工牌重试';
      } else {
        backStatus.hidden = true;
        statusTimer = window.setTimeout(() => {
          backStatus.textContent = en ? 'Loading the back…' : '正在加载工牌背面…';
          backStatus.hidden = false;
          statusVisibleAt = performance.now();
        }, 180);
      }
    });
    const loading = document.querySelector<HTMLElement>('[data-crew-loading]');
    const showFailure = () => {
      if (!document.documentElement.classList.contains('crew-first-loading')) return;
      const en = document.documentElement.lang === 'en';
      const title = loading?.querySelector<HTMLElement>('[data-loading-title]');
      const hint = loading?.querySelector<HTMLElement>('[data-loading-hint]');
      const retry = loading?.querySelector<HTMLButtonElement>('[data-loading-retry]');
      if (title) title.textContent = en ? 'Could not load your crew pass' : '工牌加载遇到问题';
      if (hint) hint.textContent = en ? 'Check your connection and try again.' : '请检查网络后重试。';
      if (retry) retry.hidden = false;
    };
    loading?.querySelector('[data-loading-retry]')?.addEventListener('click', () => location.reload());
    const timeout = window.setTimeout(showFailure, 20000);
    let started = false;
    let revealed = false;
    let previewDecoding = false;
    const queueOthers = async () => {
      if (!canWarm) return;
      const current = document.querySelector<HTMLElement>('.home-experience')?.dataset.characterId;
      const links = [
        ...document.querySelectorAll<HTMLElement>('[data-role-next]'),
        ...document.querySelectorAll<HTMLElement>('[data-role-previous]'),
        ...document.querySelectorAll<HTMLElement>('.crew-roster [data-texture-base]'),
      ];
      const unique = links.filter((link, index) => {
        const base = link.dataset.textureBase;
        return base && !base.endsWith('/' + current) && links.findIndex(item => item.dataset.textureBase === base) === index;
      });
      // Warm both sides of the next and previous roles first, then the rest.
      const adjacent = unique.filter(link => link.hasAttribute('data-role-next') || link.hasAttribute('data-role-previous'));
      const remaining = unique.filter(link => !adjacent.includes(link));
      const queue = [
        ...adjacent.flatMap(link => [{link, face:'front'}, {link, face:'back'}]),
        ...remaining.map(link => ({link, face:'front'})),
        ...remaining.map(link => ({link, face:'back'})),
      ];
      for (const {link, face} of queue) {
        if (document.hidden) await new Promise<void>(resolve => {
          const resume = () => { if (!document.hidden) { document.removeEventListener('visibilitychange', resume); resolve(); } };
          document.addEventListener('visibilitychange', resume);
        });
        await warm(link, [face]);
      }
    };
    const reveal = () => {
      if (revealed) return;
      revealed = true;
      clearTimeout(timeout);
      requestAnimationFrame(() => requestAnimationFrame(() => {
        document.documentElement.classList.remove('crew-first-loading');
        try { sessionStorage.setItem('crew-first-ready', '1'); } catch { /* storage may be blocked */ }
      }));
    };
    const afterFront = () => {
      if (stage.querySelector('[data-front-ready="error"]')) { showFailure(); return; }
      const fallback = stage.querySelector<HTMLImageElement>('.badge-fallback img');
      const ready = !!stage.querySelector('[data-front-ready="true"]') || !!(fallback?.complete && fallback.naturalWidth);
      const preview = stage.querySelector<HTMLImageElement>('.badge-loading-preview img');
      if (!revealed && !previewDecoding && preview?.complete && preview.naturalWidth) {
        previewDecoding = true;
        preview.decode().then(reveal).catch(() => { previewDecoding = false; });
      }
      if (ready) reveal();
      if (!ready || started) return;
      started = true;
      observer.disconnect();
      requestAnimationFrame(() => requestAnimationFrame(() => {
        const schedule = window.requestIdleCallback || ((callback: () => void) => window.setTimeout(callback,300));
        schedule(() => { void queueOthers(); });
      }));
    };
    const observer = new MutationObserver(afterFront);
    observer.observe(stage,{subtree:true,childList:true,attributes:true,attributeFilter:['data-front-ready']});
    stage.addEventListener('load', afterFront, true);
    stage.addEventListener('error', showFailure, true);
    afterFront();
    window.addEventListener('pagehide',()=>{ observer.disconnect(); clearTimeout(timeout); },{once:true});
  }
  const community = document.querySelector<HTMLDialogElement>('#community');
  document.querySelector('[data-open-community]')?.addEventListener('click', () => community?.showModal());
  document.querySelector('[data-close-community]')?.addEventListener('click', () => community?.close());
  community?.addEventListener('click', event => {
    const rect = community.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) community.close();
  });
  const picker = document.querySelector<HTMLDetailsElement>('[data-crew-picker]');
  document.addEventListener('pointerdown', event => {
    if (picker?.open && !picker.contains(event.target as Node)) picker.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && picker?.open) {
      picker.open = false;
      picker.querySelector<HTMLElement>('summary')?.focus();
    }
  });
  const dialog = document.querySelector<HTMLDialogElement>('#credits');
  document.querySelectorAll<HTMLElement>('[data-open-credits]').forEach(button => {
    button.addEventListener('click', () => dialog?.showModal());
  });
  document.querySelector('[data-close-credits]')?.addEventListener('click', () => dialog?.close());
  dialog?.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
}
