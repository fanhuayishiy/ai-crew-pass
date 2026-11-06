import { type Character } from "./characters";
import { localizedCharacters, localeCharacterUrl, characterCatchphrase, copy, type Locale } from './i18n';

/**
 * Character gallery adapted to the original Hanging Pass card contract.
 *
 * Structure:
 *   · index 0 + tier 'cover' is the badge (the screen-1 card); its content is written
 *     in BadgeExperience.astro; the cover entry supplies index/label fields.
 *   · The remaining entries are the cards in the screen-2 carousel.
 *   · Each gallery card links to its statically generated character badge page.
 */

export type SiteCard = {
  /** Matches data-chapter-index in the DOM; 0 = cover (the badge) */
  index: number;
  id: string;
  label: string;
  /** Small label at the top left of the front face */
  kicker: string;
  /** Short tag at the top right of the front face */
  tag: string;
  href: string;
  /** Accent colour (for small highlight touches) */
  accent: string;
  tier: 'cover' | 'business' | 'personal';
  /** Cards whose content is not ready yet are not rendered */
  draft?: boolean;
  front: {
    /** Front hero image; empty means title only */
    image?: string;
    alt: string;
  };
  back: {
    catchphrase: string;
    summary: string;
    bullets: string[];
    cta: string;
  };
};

export function makeCards(selected: Character, locale: Locale = 'zh'): SiteCard[] {
  const card = (c: Character, index: number): SiteCard => ({
    index, id: c.id, label: c.brand, kicker: c.name, tag: c.alias,
    href: localeCharacterUrl(c, locale), accent: c.color, tier: index === 0 ? "cover" : "personal",
    front: { image: `img/characters/${c.image}`, alt: `${c.brand} · ${c.name}` },
    back: { catchphrase: characterCatchphrase(c.id, locale), summary: c.summary, bullets: c.features, cta: copy(locale).open },
  });
  return [card(selected,0), ...localizedCharacters(locale).map((c,i)=>card(c,i+1))];
}
