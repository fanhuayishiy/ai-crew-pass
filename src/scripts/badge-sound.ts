// Quiet, locally synthesized foley: no audio downloads or background playback.
export function initBadgeSound(): void {
  const button = document.querySelector<HTMLButtonElement>('[data-badge-sound]');
  if (!button) return;
  let enabled = true;
  try { enabled = localStorage.getItem('crew-pass-sound') !== 'off'; } catch {}
  let context: AudioContext | undefined;
  let lastSound = -Infinity;
  const update = () => {
    button.setAttribute('aria-pressed', String(enabled));
    button.dataset.enabled = String(enabled);
    button.title = (enabled ? button.dataset.onLabel : button.dataset.offLabel) || '';
    button.setAttribute('aria-label', button.title);
  };
  const unlock = () => {
    if (!enabled) return;
    try {
      context ||= new AudioContext();
      if (context.state === 'suspended') void context.resume().catch(() => {});
    } catch { /* Interaction remains available without Web Audio. */ }
  };
  const play = (kind: string) => {
    if (!enabled || document.hidden || performance.now() - lastSound < 180) return;
    unlock();
    if (!context || context.state !== 'running') return;
    lastSound = performance.now();
    const audio = context;
    const time = audio.currentTime;
    if (kind === 'flip') {
      const duration = .13;
      const buffer = audio.createBuffer(1, Math.ceil(audio.sampleRate * duration), audio.sampleRate);
      const samples = buffer.getChannelData(0);
      for (let i = 0; i < samples.length; i++) samples[i] = Math.random() * 2 - 1;
      const source = audio.createBufferSource();
      const filter = audio.createBiquadFilter();
      const gain = audio.createGain();
      source.buffer = buffer;
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(1800, time);
      filter.frequency.exponentialRampToValueAtTime(650, time + duration);
      filter.Q.value = .65;
      gain.gain.setValueAtTime(0, time);
      gain.gain.linearRampToValueAtTime(.035, time + .018);
      gain.gain.exponentialRampToValueAtTime(.0001, time + duration);
      source.connect(filter).connect(gain).connect(audio.destination);
      source.onended = () => { source.disconnect(); filter.disconnect(); gain.disconnect(); };
      source.start(time); source.stop(time + duration);
    } else {
      for (const frequency of [1720, 2630]) {
        const source = audio.createOscillator();
        const gain = audio.createGain();
        source.frequency.value = frequency;
        gain.gain.setValueAtTime(0, time);
        gain.gain.linearRampToValueAtTime(.009, time + .003);
        gain.gain.exponentialRampToValueAtTime(.0001, time + .10);
        source.connect(gain).connect(audio.destination);
        source.onended = () => { source.disconnect(); gain.disconnect(); };
        source.start(time); source.stop(time + .11);
      }
    }
  };
  update();
  button.addEventListener('click', () => {
    enabled = !enabled;
    try { localStorage.setItem('crew-pass-sound', enabled ? 'on' : 'off'); } catch {}
    update();
    if (enabled) { unlock(); }
  });
  document.addEventListener('pointerdown', unlock, { passive: true });
  document.addEventListener('keydown', unlock);
  document.addEventListener('badge-sound', event => play((event as CustomEvent<string>).detail));
  document.addEventListener('click', event => {
    if ((event.target as Element).closest('[data-static-flip]')) play('flip');
  });
  window.addEventListener('pagehide', () => { void context?.close().catch(() => {}); }, { once: true });
}
