// Busuanzi site PV: refreshes and character/language page changes count as views.
// Never send local development or preview traffic to the public counter.
export function initVisitCounter(hostname = window.location.hostname) {
  const counter = document.querySelector('[data-visit-counter]');
  const value = document.querySelector('#busuanzi_value_site_pv');
  if (!counter || !value || hostname !== 'badge.fhysy.com') return;
  if (document.querySelector('[data-busuanzi-script]')) return;
  const observer = new MutationObserver(() => {
    if (/^\d+$/.test(value.textContent?.trim() || '')) {
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
  const fail = () => { counter.setAttribute('hidden', ''); observer.disconnect(); };
  const timeout = window.setTimeout(fail, 15000);
  script.addEventListener('error', () => { clearTimeout(timeout); fail(); }, { once: true });
  document.head.append(script);
}
