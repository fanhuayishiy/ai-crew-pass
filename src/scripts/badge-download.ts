/** Static download URLs work without Blob support, client rendering or hydration. */
export function initBadgeDownload(): void {
  const dialog = document.querySelector<HTMLDialogElement>('[data-download-dialog]');
  const trigger = document.querySelector<HTMLAnchorElement>('[data-download-pass]');
  trigger?.addEventListener('click', event => {
    if (!dialog || typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    if (!dialog.open) dialog.showModal();
  });
  dialog?.querySelector('[data-download-close]')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
}
