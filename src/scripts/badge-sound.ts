// Recorded plastic-card and metal-buckle foley; sources: public/audio/badge/NOTICE.md.
export function initBadgeSound(): void {
  const button = document.querySelector<HTMLButtonElement>('[data-badge-sound]');
  if (!button) return;
  let enabled = true;
  try { enabled = localStorage.getItem('crew-pass-sound') !== 'off'; } catch {}
  let context: AudioContext | undefined;
  let disposed = false;
  let generation = 0;
  const base = `${import.meta.env.BASE_URL.replace(/\/$/, '')}/audio/badge/`;
  const raw = new Map<string, Promise<ArrayBuffer>>();
  const decoded = new Map<string, Promise<AudioBuffer>>();
  const active = new Set<AudioBufferSourceNode>();
  const lastSound = new Map<string, number>();
  const switchKey = 'crew-pass-arrival-sound';
  let arrivalPending = false;
  try {
    const pending = JSON.parse(sessionStorage.getItem(switchKey) || 'null');
    sessionStorage.removeItem(switchKey);
    arrivalPending = pending?.path === location.pathname && Date.now() - pending.time < 15000;
  } catch {}
  const names = ['plastic-flip-audible', 'buckle-soft'];
  const file = (name: string) => {
    if (!raw.has(name)) {
      const task = fetch(`${base}${name}.wav`, { cache: 'force-cache' }).then(r => {
        if (!r.ok) throw new Error('Audio unavailable');
        return r.arrayBuffer();
      });
      raw.set(name, task);
      void task.catch(() => raw.delete(name));
    }
    return raw.get(name)!;
  };
  const buffer = (name: string, audio: AudioContext) => {
    if (!decoded.has(name)) {
      const task = file(name).then(data => audio.decodeAudioData(data.slice(0)));
      decoded.set(name, task);
      void task.catch(() => decoded.delete(name));
    }
    return decoded.get(name)!;
  };
  const warm = () => {
    if (!enabled || disposed) return;
    for (const name of names) void file(name).catch(() => {});
  };
  const unlock = () => {
    if (!enabled || disposed) return;
    try {
      context ||= new AudioContext();
      if (context.state !== 'running') void context.resume().catch(() => {});
      for (const name of names) void buffer(name, context).catch(() => {});
    } catch { /* Silent fallback keeps the card usable. */ }
  };
  const shot = async (name: string, volume: number, delay = 0) => {
    unlock();
    if (!context) return;
    const audio = context;
    const ticket = generation;
    const requested = performance.now();
    try {
      const [sample] = await Promise.all([buffer(name, audio), audio.resume()]);
      if (!enabled || disposed || document.hidden || ticket !== generation || performance.now() - requested > 350) return;
      const node = audio.createBufferSource();
      const gain = audio.createGain();
      node.buffer = sample;
      gain.gain.value = volume;
      node.connect(gain).connect(audio.destination);
      active.add(node);
      await new Promise<void>(resolve => {
        node.onended = () => { active.delete(node); node.disconnect(); gain.disconnect(); resolve(); };
        node.start(audio.currentTime + delay);
      });
    } catch { /* Sound failure must not block navigation. */ }
  };
  const play = async (kind: string) => {
    if (!enabled || disposed || document.hidden || performance.now() - (lastSound.get(kind) ?? -Infinity) < 160) return;
    lastSound.set(kind, performance.now());
    if (kind === 'flip') await shot('plastic-flip-audible', .40 * 2 / 3 / 2);
    if (kind === 'switch') {
      await shot('buckle-soft', .42);
    }
    if (kind === 'release') {
      await shot('buckle-soft', .42);
    }
  };
  const update = () => {
    button.setAttribute('aria-pressed', String(enabled));
    button.dataset.enabled = String(enabled);
    button.title = (enabled ? button.dataset.onLabel : button.dataset.offLabel) || '';
    button.setAttribute('aria-label', button.title);
  };
  update();
  const idle = window.requestIdleCallback || ((fn: () => void) => window.setTimeout(fn, 500));
  idle(warm);
  // Same-origin navigation carries the user's activation in supported browsers.
  if (arrivalPending) unlock();
  document.addEventListener('badge-arrive', () => {
    if (!arrivalPending) return;
    arrivalPending = false;
    void play('switch');
  }, { once: true });
  button.addEventListener('click', () => {
    enabled = !enabled;
    generation++;
    if (!enabled) {
      for (const node of active) node.stop();
    }
    try { localStorage.setItem('crew-pass-sound', enabled ? 'on' : 'off'); } catch {}
    update();
    if (enabled) unlock();
  });
  document.addEventListener('pointerdown', unlock, { passive: true });
  document.addEventListener('keydown', unlock);
  document.addEventListener('badge-sound', event => { void play((event as CustomEvent<string>).detail); });
  document.addEventListener('click', event => {
    if ((event.target as Element).closest('[data-static-flip]')) void play('flip');
    const link = (event.target as Element).closest<HTMLAnchorElement>('[data-role-previous], [data-role-next], .crew-roster a');
    if (!link || !enabled || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || link.getAttribute('aria-current') === 'true') return;
    try {
      sessionStorage.setItem(switchKey, JSON.stringify({ path: new URL(link.href).pathname, time: Date.now() }));
    } catch {}
    // Let navigation happen immediately; the new card announces its physical drop.
  });
  window.addEventListener('pagehide', () => {
    disposed = true; generation++;
    void context?.close().catch(() => {});
  });
  window.addEventListener('pageshow', event => {
    if (event.persisted) { disposed = false; context = undefined; decoded.clear(); }
  });
}
