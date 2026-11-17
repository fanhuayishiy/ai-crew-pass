// Busuanzi site PV: refreshes and character/language page changes count as views.
// Never send local development or preview traffic to the public counter.
export function initVisitCounter(hostname = window.location.hostname) {
  const counter = document.querySelector('[data-visit-counter]');
  const value = document.querySelector('#busuanzi_value_site_pv');
  const status = counter?.querySelector('[data-visit-status]');
  if (!counter || !value || hostname !== 'badge.fhysy.com') return;
  if (document.querySelector('[data-busuanzi-script]')) return;
  const observer = new MutationObserver(() => {
    if (/^\d+$/.test(value.textContent?.trim() || '')) {
      status?.setAttribute('hidden', '');
      counter.removeAttribute('hidden');
      observer.disconnect();
      clearTimeout(timeout);
    }
  });
  observer.observe(value, { childList: true, subtree: true, characterData: true });
  const script = document.createElement('script');
  script.async = true;
  script.dataset.busuanziScript = '';
  script.src = 'https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js';
  const showUnavailable = () => {
    status?.removeAttribute('hidden');
    counter.removeAttribute('hidden');
  };
  // Keep listening after the timeout: the original request can still succeed late.
  const timeout = window.setTimeout(showUnavailable, 15000);
  script.addEventListener('error', () => {
    clearTimeout(timeout);
    showUnavailable();
    observer.disconnect();
  }, { once: true });
  document.head.append(script);
}
