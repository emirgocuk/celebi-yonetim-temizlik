# Project Brief: Çelebi Yönetim ve Temizlik

> Son Güncelleme: **22 Kasım 2026**

## 1. Project Overview & Client Profile
- **Company Name**: Çelebi Yönetim ve Temizlik Hizmet İşleri Ltd. Şti.
- **Location & Service Area**: `Mahfesığmaz Mah. 78033 Sk. No: 3 Zemin Kat, Çukurova / Adana` — Hizmet bölgesi **Adana** (Çukurova, Seyhan, Sarıçam, Yüreğir).
- **Live Production URL**: `https://celebiyonetim.com.tr/`
- **Industry**: Profesyonel Tesis & Site/Apartman Yönetimi (634 sayılı KMK uyum, şeffaf aidat/icra takibi, işletme projesi) + SGK Güvenceli Kurumsal & Bireysel Temizlik Hizmetleri (Ofis, merdiven, inşaat/tadilat sonrası, dış cephe temizliği).
- **Core Mission**: Adana'daki toplu yaşam alanlarında (siteler, apartmanlar, iş merkezleri) kurumsal, şeffaf, dijital takip edilebilir yönetim hizmeti ve yüksek hijyen standartlarında profesyonel temizlik çözümleri sunmak.

---

## 2. Core Technical Requirements
- **Primary Tech Stack**: 
  - **Frontend Framework**: **Astro** (`7.x`, `trailingSlash: 'always'`) – Islands architecture, generating minimal/0kB JavaScript by default for pure static content, providing unmatched speed and SEO crawlability.
  - **Backend / Database**: **PocketBase** (`v0.41.1`) – Lightweight SQLite-powered backend on Ubuntu VDS behind Nginx + Cloudflare CDN, providing REST API, auth, `pb_hooks` instant notifications, automated AI content scheduling, and dynamic lead/settings management.
- **Performance Benchmark**:
  - **PageSpeed Insights**: **100/100** score target on both **Mobile** and **Desktop**.
  - **Core Web Vitals**:
    - **LCP (Largest Contentful Paint)**: < 1.2s
    - **CLS (Cumulative Layout Shift)**: 0.00
    - **INP (Interaction to Next Paint)**: < 100ms
    - **FCP (First Contentful Paint)**: < 0.8s
- **SEO & Search Dominance**:
  - Semantic HTML5 structure throughout, `trailingSlash: 'always'` ve sıfır `301` yönlendirmeli canonical URL disiplini.
  - Comprehensive Schema.org JSON-LD structured data (`LocalBusiness`, `ProfessionalService`, `CleaningService`, `FAQPage`, `BreadcrumbList`).
  - OpenGraph, Twitter Card, dinamik `sitemap.xml`, `robots.txt`, `llms.txt`, `ard.json` ve otomatik GSC / IndexNow entegrasyonu.

---

## 3. Design & User Experience Directives
- **Visual Theme & Atmosphere**:
  - **Ferah ve Beyaz Temalı (Airy, Fresh, White-dominant)**: Clean white backgrounds (`#FFFFFF`, `#F8FAFC`, `#F1F5F9`), ample negative space, breathing room, subtle hairline borders, and sophisticated soft shadows.
  - **Apple-Inspired Dynamic Feel**:
    - Floating, translucent frosted glass header (`backdrop-blur-md bg-white/75 border border-white/40`) that dynamically reacts to scroll.
    - Silky smooth, GPU-accelerated micro-interactions (pure CSS transforms, zero layout thrashing).
  - **Implemented Brand Identity**:
    - Yatay çerçevesiz vektörel SVG marka logosu (`celebi-logo.svg`), önbellek kırmalı favicon seti ve CSS değişken token'ları (`--color-brand-primary`, `--color-brand-accent`) ile tam marka bütünlüğü sağlanmıştır.
- **Design Philosophy**:
  - Adherence to **`pbakaus/impeccable`**: Zero generic AI slop, no clichéd purple gradient cards, intentional typography scale, robust responsive hierarchy, bespoke UI craft.
- **Content Philosophy**:
  - Adherence to **`petergyang/no-ai-slop`**: Authentic, confident, crisp Turkish copywriting. Concrete promises: SGK belgeli personel, şeffaf banka hesabı ve aidat raporlaması, KMK uyumlu icra takibi, 5 dakikada ücretsiz keşif dönüşü.

---

## 4. Key Deliverables & Milestones
1. **Vault & Memory Bank Architecture** (`Tamamlandı`): Kurallar ve yaşayan proje dokümantasyonu.
2. **Astro + PocketBase + VDS Production Setup** (`Tamamlandı`): Ubuntu VDS, Nginx HTTPS, PocketBase `v0.41.1` ve Cloudflare CDN canlı yayını.
3. **Adana Local SEO, District Landing Pages & Interactive Lead Magnets** (`Tamamlandı`): `/site-yonetimi/`, `/temizlik/`, ilçe iniş sayfaları (`/cukurova-site-yonetimi/`, `/seyhan-apartman-yonetimi/`, `/saricam-site-yonetimi/`), `/site-yonetimi-fiyat-hesapla/` ve `/apartman-karar-defteri-ornekleri/`.
4. **Autonomous AI Content Engine & Instant `pb_hooks` Notifications** (`Tamamlandı`): 4 modelli OpenRouter makale motoru (`48h`), `ntfy.sh` telefona anlık bildirim ve `/merkez` yönetim konsolu.
5. **GTM + GA4 + GSC API & Google Ads Readiness** (`Tamamlandı`): `GTM-M7CC26B5` + `G-74ZHMJ1VEJ` dönüşümleri/kitleleri, servis hesabı raporlama CLI'ı (`google-baglan.cmd`), 137 kelimelik Adana negatif kelime paketi ve kontrollü test stratejisi.
6. **Cold-Start Activation & Paid Search Validation** (`Sıradaki Adım`): KMK gecikme tazminatı/kapıcı maliyeti aracı, 0 ₺ Adana yerel paylaşım/dizin paketi, Haritalar yorumları ve 14 günlük kontrollü Google Ads Arama Ağı testi.
