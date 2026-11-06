import Lanyard from './react-bits/Lanyard';

// Keep the upstream interaction intact; customize only its public props.
export default function ReactBitsBadge({ characterId, color, cardColor, base, locale = 'zh' }) {
  const path = `${base.replace(/\/$/, '')}/img/badges/${locale}/${characterId}`;
  return <Lanyard
    frontImage={`${path}-front.png`}
    backImage={`${path}-back.png`}
    strapImage={`${base.replace(/\/$/, '')}/img/badges/${characterId}-strap.svg`}
    strapColor={color}
    cardColor={cardColor}
    imageFit="cover"
    size={0.51}
    finish="glossy"
  />;
}
