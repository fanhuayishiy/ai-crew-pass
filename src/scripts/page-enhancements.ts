import { initBadgeSound } from './badge-sound';
import { initVisitCounter } from './visit-counter';

export function initPageEnhancements(): void {
  initBadgeSound();
  initVisitCounter();
  const connection = (navigator as Navigator & { connection?: {saveData?: boolean;effectiveType?: string} }).connection;
  const canWarm = !connection?.saveData && !['slow-2g','2g'].includes(connection?.effectiveType || '');
  const warmed = new Set<string>();
  const warm = (link: HTMLElement, faces: string[] = ['front','back']) => {
    if (!canWarm || document.hidden) return;
    const base = link.dataset.textureBase;
    if (!base) return;
    for (const face of faces) {
      const url = `${base}-${face}.webp`;
      if (warmed.has(url)) continue;
      warmed.add(url);
      fetch(url, {cache:'force-cache',mode:'cors',credentials:'same-origin'})
        .then(response => { if (!response.ok) throw new Error('Prefetch failed'); return response.arrayBuffer(); })
        .catch(() => warmed.delete(url));
    }
  };
  document.querySelectorAll<HTMLElement>('[data-texture-base]').forEach(link => {
    link.addEventListener('pointerenter', () => warm(link), {passive:true});
    link.addEventListener('focus', () => warm(link));
    link.addEventListener('touchstart', () => warm(link), {passive:true});
  });
  // Only warm adjacent roles after the current face is already painted.
  const stage = document.querySelector('.react-bits-stage');
  if (stage && canWarm) {
    const afterFront = () => {
      if (!stage.querySelector('[data-front-ready="true"]')) return;
      observer.disconnect();
      const schedule = window.requestIdleCallback || ((callback: () => void) => window.setTimeout(callback,300));
      // Warm only neighboring fronts; reverse faces wait for deliberate hover/focus.
      schedule(() => document.querySelectorAll<HTMLElement>('[data-role-previous],[data-role-next]').forEach(link => warm(link, ['front'])));
    };
    const observer = new MutationObserver(afterFront);
    observer.observe(stage,{subtree:true,attributes:true,attributeFilter:['data-front-ready']});
    afterFront();
    window.addEventListener('pagehide',()=>observer.disconnect(),{once:true});
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
