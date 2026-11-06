# Design Principles: pbakaus/impeccable Core Standards & Apple Dynamic UX

Directly extracted and adapted from [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable) (including `craft-floor.md`, `DESIGN.md`, and deterministic anti-pattern checks) for **Çelebi Yönetim ve Temizlik**.

---

## 1. The Impeccable Craft Floor (Mandatory Verifications)

Every interface surface must satisfy these deterministic mechanical checks:

- **Contrast (`rule:skill-color-verify-contrast`)**: Body and placeholder text $\ge 4.5:1$, large text $\ge 3:1$. On colored surfaces, tint secondary text from that hue or the foreground; **never pure gray**.
- **Depth (`rule:skill-color-no-glow-halo`)**: Shadows carry a distinct physical offset and a soft blur. A zero-offset colored halo is lazy decoration.
- **Elevation System (`rule:skill-codex-elevation-radius`, `rule:skill-ban-codex-ghost-card`)**: Declare elevation once: **border OR shadow**, never both at the same time ("ghost card" = 1px border under wide soft shadow). Card radii stay strictly between `12px` and `16px`; pill shapes are reserved exclusively for small controls.
- **Spacing Rhythm (`rule:skill-layout-spacing-rhythm`)**: Tight related groups, generous structural separation. Always place significantly more whitespace above a heading than below it (e.g., `mt-16 mb-4`).
- **Typography Floor (`rule:skill-typo-floor`, `rule:skill-ban-text-overflow`)**:
  - Body measure: strictly 65–75 characters per line (`max-w-prose` / `max-w-2xl`).
  - Tracking floor: max `-0.04em`. `-0.02em` to `-0.03em` reads best on display text; never collapse body tracking.
  - Balanced headings without awkward orphan words.
- **Motion Floor (`rule:skill-motion-floor`, `rule:skill-motion-no-section-fade`)**:
  - Exactly **one authored moment** per interaction, not scattered effects and not an identical fade-in on every section.
  - Exponential ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`) from an already-visible default.
  - Transitions stay strictly smooth (GPU accelerated: `transform`, `opacity`, `backdrop-filter`).
- **Browser Surfaces (`rule:skill-craft-browser-surfaces`)**:
  - Text selection (`::selection`), the caret (`caret-color`), custom scrollbars, keyboard focus rings (`focus-visible`), and tabular numerals (`font-variant-numeric: tabular-nums`) must all be themed from the palette. Browser defaults are an immediate tell that a site was assembled rather than crafted.
- **Copy as Material (`rule:skill-copy-design-material`)**:
  - Controls name their exact action; errors name the exact problem and recovery path.

---

## 2. Impeccable Hard Refusals (Deterministic Anti-Patterns Banned)

These are banned outright by `pbakaus/impeccable`:

1. **NO Gradient Text (`rule:skill-ban-gradient-text`)**:
   - *Banned*: `text-transparent bg-clip-text bg-gradient-to-r...`
   - *Rule*: Emphasis comes from weight, contrast, or size. Gradient text is the primary signature of cheap AI templates.
2. **NO Eyebrow / Kicker Labels on Every Section (`rule:skill-ban-eyebrow-on-every-section`)**:
   - *Banned*: Small pill or uppercase subtitle badges hovering above every single `<h2>` ("Kapsamlı Çözümler", "Kurumsal Güvence").
   - *Rule*: "This is a ban, not a default: no brief earns it back. The heading carries its own weight; delete the label and let the heading speak."
3. **NO Section Numbers (`rule:skill-ban-numbered-section-markers`)**:
   - *Banned*: Numbered section badges like `01`, `02`, `03` unless the sequence itself represents an ordered process the reader must follow step-by-step.
4. **NO Identical Card Grids (`rule:skill-ban-identical-card-grids`, `rule:skill-layout-cards-lazy`)**:
   - *Banned*: The default layout where a whole page is just 3 identical boxes with an icon, a bold title, and two sentences. Cards are the lazy container; nested cards are always wrong.
   - *Rule*: Structure layouts according to the nature of the information (e.g., timeline, split comparison, documentation hierarchy, table, or editorial split).
5. **NO Hero-Metric Strip Templates (`rule:skill-ban-hero-metric`)**:
   - *Banned*: The predictable row of 4 giant numbers with tiny labels underneath slapped right below the hero.
   - *Rule*: Integrate credentials and proof directly into the narrative and context.
6. **NO Fake Grid/Dot Background Overlays (`rule:skill-ban-codex-grid-backgrounds`)**:
   - *Banned*: `bg-[radial-gradient(#fff_1px,transparent_1px)]` dot matrix or blueprint grids on normal corporate pages. A background is a surface, textured only when representing a genuine blueprint/canvas.
7. **NO Unicode Glyphs or Emoji for Icons (`rule:skill-ban-glyph-icons`)**:
   - *Banned*: Using `★` or emoji as bullet points or card badges. Use authored, consistent SVGs with single stroke weights.
8. **NO Glassmorphism as Generic Decoration (`rule:skill-ban-glassmorphism-default`)**:
   - *Rule*: Blur and translucency are reserved for functional surfaces that float over real scrolling content (such as the Apple floating header). Never use glass blur on static page cards.

---

## 3. Apple-Grade Dynamic Polish

- **Floating Frosted Header**:
  - `backdrop-blur-xl bg-white/75 border border-white/60 shadow-[0_8px_30px_rgb(0,0,0,0.04)]`.
  - Compresses smoothly on scroll (> 20px) to dock state without layout shift.
  - Spring-eased slide in on upward scroll.
  - Zero performance tax (passive listener, 0ms TBT).
- **Tactile Physics**:
  - Active tap response: `active:scale-[0.985] transition-transform duration-150`.
  - Clean focus rings: `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-slate-900`.
- **Palette**:
  - Clean, spacious white theme (`#FFFFFF`, `#F8FAFC`).
  - Swappable brand variables (`--brand-primary`, `--brand-accent`).
