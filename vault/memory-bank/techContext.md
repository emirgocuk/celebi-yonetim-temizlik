# Technical Context: Çelebi Yönetim ve Temizlik

## 1. Technology Stack Details

| Layer | Technology | Version / Spec | Rationale |
|---|---|---|---|
| **Runtime** | Node.js | v22.18.0 | Long-Term Support, fast V8 execution |
| **Package Manager** | npm | v10.9.3 | Standard native package manager |
| **Frontend Core** | **Astro** | 5.x | Islands architecture, zero JS by default, extreme speed |
| **Backend & Database** | **PocketBase** | v0.22+ / latest | Single-binary SQLite + Auth + Realtime + Admin UI |
| **Backend SDK** | `pocketbase` | Latest npm package | Direct REST/SSE client with full TypeScript support |
| **Styling** | Tailwind CSS / CSS Variables | v3/v4 + Tailwind Typography | Micro-purged utility styling + semantic design tokens |
| **Icons** | Lucide Icons (Inline SVG) | Latest | Zero external font overhead, tree-shaken SVGs |
| **Typography** | Inter / System Font Fallback | Native web fonts with preload | Instant font rendering, zero CLS, maximum crispness |

---

## 2. Development Setup & Commands

### Prerequisites
- Node.js >= 20 (Current: v22.18.0)
- PocketBase binary (downloadable or run via local executable)

### Standard Project Commands
```bash
# Start Astro development server
npm run dev

# Build production static bundle
npm run build

# Preview production build locally
npm run preview

# Run PocketBase local development instance
./pocketbase serve --http="127.0.0.1:8090"
```

---

## 3. Technical Constraints & Performance Budgets

To achieve and strictly maintain **100/100 PageSpeed Insights** on Mobile and Desktop:

1. **JavaScript Budget**:
   - Total uncompressed client JS on landing page: **< 15 kB**.
   - No heavy animation frameworks (No GSAP, No Framer Motion). All header blur and hover effects are implemented with native GPU-accelerated CSS.
2. **CSS Budget**:
   - Total CSS: **< 25 kB** gzipped. Astro automatically purges and inlines critical CSS.
3. **Image Optimization**:
   - All raster images must use Astro's native `<Image />` component with `format="avif"` or `format="webp"`.
   - Every single image must have explicit `width` and `height` (or aspect-ratio) to prevent Cumulative Layout Shift (CLS).
4. **Font Delivery**:
   - Zero external Google Fonts `@import` inside CSS (which blocks the render pipeline).
   - Local font files preloaded or modern system font stack used (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`).
5. **DOM Depth**:
   - Maximum DOM depth < 32 levels, total DOM nodes < 800 to maintain instant rendering on low-tier mobile devices.

---

## 4. Environment Variables Specification

```env
# PocketBase Connection
PUBLIC_POCKETBASE_URL="http://127.0.0.1:8090" # Local dev or production URL
POCKETBASE_ADMIN_EMAIL="admin@celebi.com"
POCKETBASE_ADMIN_PASSWORD="super-secret-password"

# Site Configuration
PUBLIC_SITE_URL="https://www.celebiyonetim.com"
PUBLIC_COMPANY_NAME="Çelebi Yönetim ve Temizlik"
PUBLIC_COMPANY_PHONE="+90 555 000 00 00"
PUBLIC_COMPANY_WHATSAPP="905550000000"
PUBLIC_COMPANY_EMAIL="info@celebiyonetim.com"
```

