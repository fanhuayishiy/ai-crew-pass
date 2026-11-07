import Lanyard from './react-bits/Lanyard';
import { Component, useEffect, useRef, useState } from 'react';

function StaticBadge({ base, characterId, locale }) {
  const [back, setBack] = useState(false);
  const path = `${base.replace(/\/$/, '')}/img/badges/${locale}/${characterId}`;
  return <div className="badge-fallback" role="group" aria-label={locale === 'en' ? 'Crew pass preview' : '工牌预览'}>
    <img src={`${path}-${back ? 'back' : 'front'}.webp`} alt={locale === 'en' ? `${characterId} crew pass, ${back ? 'back' : 'front'}` : `${characterId} 工牌${back ? '背面' : '正面'}`} />
    <button type="button" data-static-flip onClick={() => setBack(value => !value)}>{locale === 'en' ? 'Flip pass' : '翻转工牌'} ↻</button>
    <p>{locale === 'en' ? '3D is unavailable. You can still flip and download your pass.' : '当前浏览器无法显示 3D，仍可翻面和下载工牌。'}</p>
  </div>;
}

class BadgeBoundary extends Component {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  render() { return this.state.failed ? this.props.fallback : this.props.children; }
}

// Keep the upstream interaction intact; customize only its public props.
export default function ReactBitsBadge({ characterId, color, cardColor, base, locale = 'zh' }) {
  const [compact, setCompact] = useState(false);
  const [unavailable, setUnavailable] = useState(false);
  const host = useRef(null);
  useEffect(() => {
    let active = true;
    // Upstream silently returns when renderer creation fails. Check after effects
    // have mounted instead of changing its rendering or simulation code.
    queueMicrotask(() => {
      if (active && !host.current?.querySelector('.lanyard-canvas')) setUnavailable(true);
    });
    return () => { active = false; };
  }, []);
  useEffect(() => {
    const query = matchMedia('(max-width: 760px) and (max-height: 700px)');
    const update = () => setCompact(query.matches);
    update(); query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);
  const path = `${base.replace(/\/$/, '')}/img/badges/${locale}/${characterId}`;
  const fallback = <StaticBadge base={base} characterId={characterId} locale={locale} />;
  return <div ref={host} style={{width:'100%',height:'100%'}}>{unavailable ? fallback : <BadgeBoundary fallback={fallback}><Lanyard
    frontImage={`${path}-front.webp`}
    backImage={`${path}-back.webp`}
    strapImage={`${base.replace(/\/$/, '')}/img/badges/${characterId}-strap.svg`}
    strapColor={color}
    cardColor={cardColor}
    imageFit="cover"
    size={compact ? 0.44 : 0.51}
    finish="glossy"
    crispFront={true}
  /></BadgeBoundary>}</div>;
}
