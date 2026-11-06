# React Bits Lanyard

Vendored from https://github.com/DavidHDev/react-bits/blob/main/src/content/Components/Lanyard/Lanyard.jsx on 2026-11-06, together with its Lanyard.css and repository license.

The Chinese mirror was unavailable during integration. This is the official upstream React component, using Three.js and its built-in simulation. The earlier custom simulation files remain in the repository but are no longer imported by the page.

Local loading-only adaptation (2026-11-07): front, back, and strap image promises paint independently instead of waiting on Promise.all. A `data-front-ready` attribute reports when the front has been painted, allowing neighbor prefetch after the current face is ready. Physics, geometry, materials and drag behavior are unchanged. The wrapper supplies full-resolution WebP display textures; original PNG downloads are retained.

License: MIT + Commons Clause License Condition v1.0; see LICENSE.md. This component is included as part of the AI Crew Pass application.

## ShinyText

ShinyText.jsx and ShinyText.css were vendored unchanged on 2026-11-06 from https://github.com/DavidHDev/react-bits/tree/main/src/content/TextAnimations/ShinyText under the same repository license retained here. Used for low-contrast background typography; respects reduced motion and visibility. The employee roster is an original native details/summary control with CSS hover motion, not a copy of GooeyNav.
