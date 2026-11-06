# Technical Standards & Code Architecture

Standards for engineering, component structure, PocketBase integration, and styling in **Çelebi Yönetim ve Temizlik**.

---

## 1. Directory Structure

```
d:\Projects\celebi-yonetim-temizlik\
├── vault/
│   ├── memory-bank/          # Cline Memory Bank (6 core markdown files)
│   └── rules/                # Project rules and engineering guidelines
├── public/
│   ├── favicon.svg
│   ├── robots.txt
│   └── assets/               # Static assets, fallback logos, illustrations
├── src/
│   ├── components/
│   │   ├── layout/           # Header.astro, Footer.astro, MobileMenu.astro
│   │   ├── ui/               # Button.astro, Badge.astro, Card.astro, Modal.astro
│   │   ├── sections/         # Hero.astro, Services.astro, WhyUs.astro, Stats.astro, Reviews.astro, Faq.astro
│   │   └── seo/              # SEO.astro, SchemaOrg.astro
│   ├── layouts/
│   │   └── BaseLayout.astro  # Primary layout with HTML envelope, Head, SEO, and Header/Footer
│   ├── lib/
│   │   ├── pocketbase.ts     # PocketBase client singleton and collection queries
│   │   ├── fallback-data.ts  # Resilient static data fallback for build-time safety
│   │   └── utils.ts          # Formatters, class merge helpers, phone link formatters
│   ├── styles/
│   │   └── global.css        # Global CSS variables, custom utilities, backdrop blur tokens
│   └── pages/
│       ├── index.astro       # High-converting homepage
│       ├── site-yonetimi.astro # Facility & Property Management deep dive
│       ├── temizlik.astro    # Cleaning Services deep dive
│       ├── hakkimizda.astro  # About Us & Company Credentials
│       ├── iletisim.astro    # Contact page + PocketBase Quote form
│       └── sitemap.xml.ts    # Dynamic sitemap generator
├── astro.config.mjs          # Astro configuration
├── tailwind.config.mjs       # Tailwind CSS configuration with design tokens
├── tsconfig.json             # TypeScript configuration
└── package.json              # Project dependencies and build scripts
```

---

## 2. PocketBase Integration Standards

### A. Singleton Pattern (`src/lib/pocketbase.ts`)
- Never instantiate multiple `new PocketBase()` instances. Export a shared singleton client.
- Configure automatic token refresh and safe timeout handling.

### B. Build-Time Resilience (Fallback Adapter)
When running `npm run build` or developing without an active PocketBase binary:
- All data-fetching functions in `src/lib/pocketbase.ts` MUST implement a `try/catch` wrapper that falls back to `src/lib/fallback-data.ts`.
- The static site build must **NEVER fail** because the database server is offline or unreachable.

### C. Progressive Enhancement for Forms
- Forms (e.g., "Teklif Al" / "İletişim") must use standard HTML form semantics with `method="POST"`.
- Enhance on the client with a lightweight `fetch()` call to submit data directly to PocketBase's REST API (`/api/collections/teklif_talepleri/records`).
- If client JS is disabled or fails, the form still submits reliably or triggers a native `mailto:` / WhatsApp fallback URL.

---

## 3. Component Authoring Standards

1. **Astro Props Type Safety**:
   - Every reusable `.astro` component must declare an explicit `Props` TypeScript interface:
     ```typescript
     interface Props {
       title: string;
       badge?: string;
       class?: string;
     }
     const { title, badge, class: className } = Astro.props;
     ```
2. **Accessibility First (a11y)**:
   - All interactive elements must be focusable via keyboard (`focus-visible:ring-2`).
   - SVG icons must have `aria-hidden="true"` when accompanied by text, or an `aria-label` when standalone.
   - Screen-reader labels (`sr-only`) must be provided for icon-only action buttons.
3. **Semantic Markup**:
   - Navigation links inside `<nav>`.
   - Distinct page sections inside `<section id="...">`.
   - Article/service cards inside `<article>`.

---

## 4. Styling & CSS Standards

1. **Design Tokens First**:
   - Use CSS custom properties defined in `src/styles/global.css` mapped through Tailwind:
     - `bg-[var(--color-surface-base)]` or semantic Tailwind utilities.
     - `text-[var(--color-text-primary)]`.
     - `accent-[var(--color-brand-accent)]`.
2. **Fluid Typography & Spacing**:
   - Use clamp-based fluid sizing or Tailwind's responsive prefixes (`text-3xl md:text-5xl lg:text-6xl`) for perfect scaling across mobile, tablet, and desktop screens.
3. **GPU-Accelerated Transitions**:
   - Use `transition-transform duration-200 ease-out` and `transition-opacity`.
   - Avoid animating expensive geometric properties (`width`, `height`, `top`, `left`, `margin`, `padding`) during scroll or rapid hover.

