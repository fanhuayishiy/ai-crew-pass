# Remaining crew layered artwork v1

Date: 2026-11-07. Generated with built-in image_gen, 21 separate outputs. Portrait, front background and back background are independent images, with live typography composed in Astro. Original PNGs preserved. WebP source siblings used only during export, not requested on the normal page. The final full-resolution WebP card textures are used by the 3D renderer.

Original character designs: ZipZipPipe for GLM, Qwen, Gemini, Claude, Kimi and Grok, adapted from existing public/img/characters references. Doubao derives from the existing AI-generated anime reference supplied by the user. Original attribution and fan-art usage restrictions remain; these derivatives are unofficial and are not automatically MIT licensed. Layout references: project DeepSeek/GPT composed card images.

## Delivery and verification

- All nine characters use the approved separated-layer composition in Chinese and English. The seven new characters have 21 independently generated source layers.
- Front prints use unlit original-color rendering; no illumination, coating or grain blurs the portrait or type. Physics and hardware stay unchanged.
- 36 display textures retain 1296 x 1824 pixels, quality-94 WebP. Total 8,239,014 bytes versus 42,747,724 bytes PNG (80.7% smaller). Front range 235-389 KiB, reverse 103-126 KiB. Transparent PNG downloads remain 1200 x 1688.
- Current front preloads in the HTML and also serves as a static preview before 3D is ready. Reverse loading follows front readiness. Only adjacent fronts are idle-prefetched; explicit hover/focus can warm both sides. Data Saver / 2G skip speculative requests.
- Normal page traffic never requests original portrait/background layers. Build packaging excludes the unused source art, retaining originals in the repository and retaining credit notices in the output.
- Verification: production build; verify-layered-crew.py (18 language/role renders, original-image traffic audit, 36 downloads with transparent corners/slot, 18 ZIP CRCs); verify-published.py (mobile, navigation, download flow); verify-texture-loading.py (front visible with reverse/strap blocked, one preload, pixel dimensions and compression budgets).
- Network experiment: Chromium, 3 Mbps, 80 ms latency, local uncompressed static server. Qwen cold front request 359,934 bytes / 2.935 seconds, full 3D ready 7.435 seconds. After neighboring preload, Gemini front read from cache in 1 ms; full 3D ready 4.964 seconds. These are local measurements, not a guarantee for production or every device; the static preview covers engine initialization. No-JavaScript preview visibility and transition to ready 3D were verified.
- Local only; this task does not publish or push the changes.

## glm

Files: public/img/glm/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. GLM fennec girl: same adult black-haired black/white maid, oversized furry fox ears, eyelash sleep-mask on head, bells, blue-black ribbons. One hand by chin, other holding the black book across her chest, preserving original calm smile. Keep the book and both hands fully in frame, no new costume.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. GLM fennec/library theme: pearl silver, misty blue-grey, slate accents (#575f75), very pale cool paper. Small embossed fox-ear/open-book emblem at lower-right, no whale or dragon. Keep all fine background detail very subtle and compressible, no random grain.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. GLM theme: deep slate-blue charcoal (#222a3b), silver-grey flowing bands; a small silver fennec fox beside an open book at lower-right. Quiet scholarly mood, no purple cast, no whales or dragons, no high frequency grain.

## qwen

Files: public/img/qwen/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. Qwen: same adult blue-violet long-haired woman with side braid, small tilted dark hat, purple eyes, elegant navy/white Eastern-inspired dress and cape with gold embroidery. Keep open folding fan in left of image, other gloved hand and small ornate handbag on right, smiling face, fine earrings and tassels. Waist-up crop but all fan and hands visible. No new ears or horns.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. Qwen theme: pale pearl indigo/periwinkle, muted blue-violet #6669b3 and tiny warm-gold accents, delicate Eastern cloud curves. Lower-right small translucent folding-fan emblem, not animal. No dense noise or grain.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. Qwen theme: deep indigo #272647, soft periwinkle flowing cloud bands, tiny gold highlights, small elegant open folding fan at lower-right with a trailing tassel. Calm Eastern scholarly look. No whale, dragon, person or grain.

## gemini

Files: public/img/gemini/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. Gemini star-cat girl: same adult long blue-purple/pink gradient hair, cat ears, heterochromatic eyes (one rosy pink, one gold), star hair ornament, navy/violet star-trimmed outfit and detached draped sleeves. One finger near lips, other hand points out to image right, same playful face; small floating prismatic stars may accompany. Preserve outfit and hands, not maid outfit.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. Gemini theme: pale lilac #e8defb, violet-blue accents #9161c6, restrained pink/cyan prismatic highlights. Small lower-right constellation/star-cat emblem, delicate four-point stars; no dragon or whale. Smooth quiet print, no noise or grain.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. Gemini theme: deep midnight violet #25173d, violet-blue flowing bands, small seated cat constellation at lower-right with a subtle curled tail, sparse four-point stars. No whale or dragon. Keep lettering region absolutely calm and avoid random grain.

## claude

Files: public/img/claude/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. Claude: same adult orange/copper long-haired woman, amber eyes, ivory high-neck long-sleeved dress, black waist and ribbons, warm orange floral ornaments. Preserve calm serious expression, one hand holding the brown book to chest, other lowered gracefully and visible. Waist-up with book fully visible. No added ears, horns or animal features.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. Warm ivory and pale apricot pearl palette, copper thin circular line, tiny floral sunburst and quill at lower-right. Balanced quiet surface matching Claude orange-haired book reader. Fine restrained details, no text.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. Claude palette: deep cocoa brown upper and copper/apricot flowing bands. Small restrained copper floral sunburst and quill/book emblem on right. Clean low-noise gradients.

## kimi

Files: public/img/kimi/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. Kimi: adult moon-white long wavy hair, lavender eyes, navy and ivory celestial maid dress, crescent and prism musical head accessory, silver musical charms, calm expression. Preserve the original lowered hands but bring hands to waist-level gently holding a silver flute so both fit waist-up composition. No added scenery.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. Kimi palette pale moon-silver, muted lavender, midnight-blue fine halo. Subtle crescent and musical staff motif in lower-right. Very quiet clean gradients, no rainbow wash.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. Kimi palette deep midnight indigo with silver-lavender flowing bands. Small crescent moon and few delicate musical notes on right. Clean restrained starry night, no dense star field.

## grok

Files: public/img/grok/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. Grok adult golden twin-tail woman with blue eyes, pointed ears, little fangs, black/burgundy regal gothic gown and gold trim, black bows, small crown and bat hair accessories. Preserve playful confident smile. Fit a scaled ceremonial black/gold double axe in left hand within the canvas, head of axe alongside shoulder rather than towering above head. Right hand holding skirt near hip. Include whole crown, hair tips, hands and axe without edge clipping.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. Grok palette champagne ivory, soft pale gold, muted antique gold thin halo. Lower right tiny orbital comet and crown silhouette. No black area on front, readable pale surface with very restrained sheen.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. Grok palette matte charcoal black with understated warm gold flowing bands, subtle burgundy undertone at bottom. Small antique-gold crown and orbiting comet on right. Smooth low-noise gradients.

## doubao

Files: public/img/doubao/{portrait-cutout-v1,front-background-v1,back-background-v1}.png and .webp.

### portrait

Generate a genuine alpha-transparent isolated waist-up anime portrait of the SAME ADULT character in the reference. Preserve exact identity, outfit, hairstyle, accessories, expression and hand pose. Refined crisp linework and clear eyes/hair, restrained cel shading, no blur or glow. Nearly square canvas, include full ears/horns, both hands and upper hips, keep 4% transparent breathing room around head and fingertips. No chibi or exaggerated anatomy. NO background, card, circle, type, frame, shadow or baked white/checkerboard matte. True transparency between hair strands/fingers. For separate placement in a readable badge. Doubao adult woman short chestnut bob and warm brown eyes, gentle smile, bright red knitted scarf, tailored black blazer over black turtleneck, black pleated skirt and silver waist chain. Clean anime cel shading matching other AI crew, not photorealistic. For square waist-up composition bring left hand gently touching scarf near chest, right hand holding compact black handbag at waist; full scarf fold, fingers and bag visible. Keep identity and original clothing.

### front

Only an independent FRONT BACKGROUND for a collector employee badge. Flat full-bleed portrait rectangle, 324:456 aspect, square canvas corners, no perspective. Match the reference card's inside layout: calm top 10% for a real brand header, thin circular halo and dotted inner arc in y=13%-65% for a separate character, sparse tiny technical etch accents and star glints, quiet bottom 34% for readable text with fine white flowing contours sweeping into the lower-right. A small subtle emblem at lower-right. Restrained pearlescent light surface, not strong glare. NO PERSON, FACE, HAIR, WORDS, LETTERS, LOGO, BARCODE, HOLE, STRAP, OUTER BORDER, FRAME, RIM OR SHADOW. Only the reusable background fills the image. Doubao palette warm porcelain white, very pale rose, thin muted crimson circular halo. Tiny folded red scarf ribbon with soft cloud contour emblem at lower-right, understated. No hearts or cute cartoon faces. Calm refined warm surface.

### back

Only an independent BACK BACKGROUND for the same employee badge. Flat full-bleed 324:456 portrait rectangle. Match the reference reverse layout: plain dark upper 58% for white type later, two or three broad gentle overlapping tone-on-tone flowing bands across y=64%-80%, rising to the right, small recognizable motif at x=77%,y=60%. One fine curved trajectory to a tiny four-point glint at x=92%,y=31%; bottom18% plain for quotation. Matte subtle gradients. NO human, words, letters, logo, barcode, separator line, badge hole, hardware, outer frame/border/rim, perspective, shadow, rounded card edge or outside scene. Doubao palette deep charcoal burgundy upper, muted crimson rose flowing bands. A small folded red scarf and simple cloud contour emblem on right, refined and warm, no heart or face. Smooth low-noise gradients.
