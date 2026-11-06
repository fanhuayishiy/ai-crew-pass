export function initPageEnhancements(): void {
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
