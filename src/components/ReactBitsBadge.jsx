import Lanyard from './react-bits/Lanyard';
import { useEffect, useState } from 'react';

// Keep the upstream interaction intact; customize only its public props.
export default function ReactBitsBadge({ characterId, color, cardColor, base, locale = 'zh' }) {
  const [compact, setCompact] = useState(false);
  useEffect(() => {
    const query = matchMedia('(max-width: 760px) and (max-height: 700px)');
    const update = () => setCompact(query.matches);
    update(); query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);
  const path = `${base.replace(/\/$/, '')}/img/badges/${locale}/${characterId}`;
  return <Lanyard
    frontImage={`${path}-front.png`}
    backImage={`${path}-back.png`}
    strapImage={`${base.replace(/\/$/, '')}/img/badges/${characterId}-strap.svg`}
    strapColor={color}
    cardColor={cardColor}
    imageFit="cover"
    size={compact ? 0.44 : 0.51}
    finish="glossy"
  />;
}
