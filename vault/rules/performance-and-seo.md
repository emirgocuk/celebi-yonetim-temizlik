# Performance & SEO Rules: The 100/100 PageSpeed Blueprint

Target: **100/100 PageSpeed Insights score on both Mobile and Desktop**, zero render-blocking resources, and comprehensive Schema.org structured data to maximize Google local organic discovery.

---

## 1. Core Web Vitals Targets

| Metric | Target (Mobile) | Target (Desktop) | Critical Tactic |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | **< 1.2s** | **< 0.6s** | Preload hero image / critical typography, zero blocking scripts |
| **CLS** (Cumulative Layout Shift) | **0.00** | **0.00** | Explicit `width` and `height` on all media; reserved header height |
| **INP** (Interaction to Next Paint) | **< 100ms** | **< 50ms** | Astro Islands architecture; 0kB client JS on static content |
| **FCP** (First Contentful Paint) | **< 0.8s** | **< 0.4s** | Critical CSS inlined by Astro automatically; no external blocking CSS |
| **TBT** (Total Blocking Time) | **0ms** | **0ms** | No heavy client-side hydrate loops or client-side routers |

---

## 2. Astro Islands & Script Loading Rules

1. **Static First**: By default, `.astro` components compile to 100% pure static HTML.
2. **Never hydrate static content**: Do not use `client:load` unless an element is strictly interactive above the fold (and even then, prefer CSS or vanilla micro-scripts).
3. **Lazy Hydration Directives**:
   - For below-the-fold interactive components (e.g., interactive calculators, testimonials slider): use `client:visible`.
   - For non-critical interactive widgets: use `client:idle`.
4. **Third-Party Scripts**:
   - Google Analytics / Tag Manager (when added) MUST be deferred or loaded via Partytown / web worker to prevent blocking the main thread.

---

## 3. Image & Media Optimization Rules

1. **Astro `<Image />` Component**:
   - Never use raw `<img>` tags for local raster images. Always use `import { Image } from 'astro:assets'`.
   - Always specify explicit `width` and `height` attributes to preserve layout aspect ratio and guarantee **CLS = 0**.
   - Output format must default to `format="avif"` with fallback to `webp`.
2. **Hero Section Image**:
   - If the hero contains an image, add `loading="eager"` and `fetchpriority="high"`.
   - Preload the hero image in the `<head>` tag.
3. **Below-the-Fold Images**:
   - Use `loading="lazy"` and `decoding="async"`.

---

## 4. Typography & Font Loading Rules

1. **No External `@import` or Google Fonts `<link>` Chains**:
   - External Google Fonts introduce DNS lookups, TLS handshakes, and render-blocking CSS delays that drop Mobile PageSpeed by 15-30 points.
2. **Recommended Font Stack**:
   - **Option A (Zero-overhead, 100% native)**: System font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`). Instant 0ms render, native OS feel, 0kB download.
   - **Option B (Self-hosted Inter/Plus Jakarta Sans)**: Local `.woff2` files stored in `/public/fonts/`, preloaded in `<head>` with `crossorigin` and `font-display: swap`.

---

## 5. SEO & Google Discoverability Architecture

### A. Semantic HTML Hierarchy
- Strictly one `<h1>` per page, clearly defining the page's core entity and location (e.g. *"Çelebi Yönetim & Temizlik | Profesyonel Site Yönetimi ve Kurumsal Temizlik Hizmetleri"*).
- Logical hierarchy: `<h1>` -> `<h2>` for major sections -> `<h3>` for cards/sub-services. Never skip levels for visual sizing (use Tailwind utility classes for sizing, e.g. `text-lg font-bold`).

### B. Structured Data (JSON-LD)
Every page must output Google-compliant JSON-LD:
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "LocalBusiness",
      "@id": "https://www.celebiyonetim.com/#organization",
      "name": "Çelebi Yönetim ve Temizlik",
      "url": "https://www.celebiyonetim.com",
      "logo": "https://www.celebiyonetim.com/assets/logo.png",
      "telephone": "+905550000000",
      "priceRange": "$$",
      "address": {
        "@type": "PostalAddress",
        "addressCountry": "TR"
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "opens": "08:30",
        "closes": "19:00"
      }
    },
    {
      "@type": "CleaningService",
      "name": "Profesyonel Temizlik Hizmetleri",
      "provider": { "@id": "https://www.celebiyonetim.com/#organization" }
    }
  ]
}
```

### C. Meta & Social Sharing
- Optimized `meta description` (140-160 characters, with high search intent keywords and clear call to action).
- OpenGraph tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:locale="tr_TR"`).
- Twitter Card tags (`summary_large_image`).
- Self-referencing canonical URLs on every page.
- Auto-generated `sitemap.xml` and `robots.txt` allowing full indexing.

