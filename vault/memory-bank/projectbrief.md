# Project Brief: Çelebi Yönetim ve Temizlik

## 1. Project Overview & Client Profile
- **Company Name**: Çelebi Yönetim ve Temizlik (Çelebi Management & Cleaning Services)
- **Industry**: Profesyonel Tesis & Site/Apartman Yönetimi (Facility & Property Management) + Profesyonel Kurumsal & Bireysel Temizlik Hizmetleri (Commercial & Residential Cleaning Services).
- **Core Mission**: Toplu yaşam alanlarında (siteler, apartmanlar, iş merkezleri) kurumsal, şeffaf, dijital takip edilebilir yönetim hizmeti ve A+ hijyen standartlarında profesyonel temizlik çözümleri sunmak.

---

## 2. Core Technical Requirements
- **Primary Tech Stack**: 
  - **Frontend Framework**: **Astro** (v5) – Islands architecture, generating 0kB JavaScript by default for pure static content, providing unmatched speed and SEO crawlability.
  - **Backend / Database**: **PocketBase** – Lightweight, blazingly fast SQLite-powered backend with real-time subscriptions, auth, file storage, and REST API for dynamic forms (teklif al / iletişim), duyurular, ve hizmet yönetimi.
- **Performance Benchmark**:
  - **PageSpeed Insights**: **100/100** score on both **Mobile** and **Desktop**.
  - **Core Web Vitals**:
    - **LCP (Largest Contentful Paint)**: < 1.2s
    - **CLS (Cumulative Layout Shift)**: 0.00
    - **INP (Interaction to Next Paint)**: < 100ms
    - **FCP (First Contentful Paint)**: < 0.8s
- **SEO & Search Dominance**:
  - Semantic HTML5 structure throughout.
  - Comprehensive Schema.org JSON-LD structured data (`LocalBusiness`, `ProfessionalService`, `CleaningService`, `FAQPage`, `BreadcrumbList`).
  - Perfect OpenGraph, Twitter Card, canonical URLs, automated dynamic sitemap.xml, and robots.txt.

---

## 3. Design & User Experience Directives
- **Visual Theme & Atmosphere**:
  - **Ferah ve Beyaz Temalı (Airy, Fresh, White-dominant)**: Clean white backgrounds (`#FFFFFF`, `#F8FAFC`, `#F1F5F9`), ample negative space, breathing room, subtle hairline borders, and sophisticated soft shadows.
  - **Apple-Inspired Dynamic Feel**:
    - Floating, translucent frosted glass header (`backdrop-blur-md bg-white/75 border border-white/40`) that dynamically reacts to scroll (compressing slightly on scroll down, expanding gently on top).
    - Silky smooth, GPU-accelerated micro-interactions (pure CSS transforms, zero layout thrashing, 60fps/120fps refresh).
  - **Brand Tokens Ready for Logo Integration**:
    - Logo is currently pending. The system will use CSS variable tokens (`--color-brand-primary`, `--color-brand-accent`) defaulting to an elegant deep slate/sapphire base that can be customized in seconds when official branding assets arrive.
- **Design Philosophy**:
  - Adherence to **`pbakaus/impeccable`**: Zero generic AI slop, no clichéd purple gradient cards, intentional typography scale, robust responsive hierarchy, bespoke UI craft.
- **Content Philosophy**:
  - Adherence to **`petergyang/no-ai-slop`**: Authentic, confident, crisp Turkish copywriting. Avoid robotic AI phrases ("Hızla değişen dünyada...", "Sadece bir temizlik firması değil..."). Instead, deliver clear, concrete promises: sigortalı personel, denetim garantisi, şeffaf aidat raporlaması, anında teklif.

---

## 4. Key Deliverables & Milestones
1. **Vault & Memory Bank Architecture** (Completed): Establishing the knowledge base and rule sets.
2. **Astro + PocketBase Baseline Setup**: Zero-bloat Astro scaffolding with Tailwind CSS and PocketBase client integration.
3. **Apple-Grade Floating Header & Global Layout**: High-performance CSS frosted-glass header with zero PageSpeed penalty.
4. **Core Pages & Sections**:
   - Anasayfa (Hero, Hizmetlerimiz, Neden Çelebi, Sayılarla Başarı, Süreç, Müşteri Yorumları, Hızlı Teklif Al CTA)
   - Site & Apartman Yönetimi (Detaylı hizmet kırılımı: Aidat takibi, bakım, hukuki danışmanlık)
   - Profesyonel Temizlik (Ofis, inşaat sonrası, dış cephe, merdiven temizliği)
   - Şeffaflık & Süreçlerimiz (Dijital denetim, raporlama, güvenlik standartları)
   - İletişim & Teklif Formu (PocketBase form entegrasyonu, WhatsApp direkt hat)
5. **SEO & Performance Audit**: Automated PageSpeed Insights verification, JSON-LD testing, responsive audit across all screen widths.

