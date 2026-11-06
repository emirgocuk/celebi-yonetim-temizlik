# Çelebi Yönetim ve Temizlik

Modern, ferah, beyaz temalı ve Apple benzeri akışkan mikro-etkileşimlere sahip; **Astro v7 + Tailwind CSS v4 + PocketBase** altyapısıyla geliştirilmiş, **PageSpeed Insights 100/100** ve en yüksek Google SEO uyumluluğu hedeflenmiş kurumsal web platformu.

---

## 🏛️ Vault ve Mimari Dokümantasyon

Projenin tüm kararları, hafıza bankası ve kuralları `vault/` dizininde eksiksiz olarak tutulmaktadır:

- **`vault/memory-bank/`** (Cline Memory Bank):
  - [`projectbrief.md`](file:///vault/memory-bank/projectbrief.md): Proje kapsamı, temel hedefler ve PageSpeed 100 kriterleri.
  - [`productContext.md`](file:///vault/memory-bank/productContext.md): Çözülen sektör sorunları, hedef kitle ve kullanıcı deneyimi.
  - [`activeContext.md`](file:///vault/memory-bank/activeContext.md): Aktif kararlar, tasarım esnekliği ve sonraki adımlar.
  - [`systemPatterns.md`](file:///vault/memory-bank/systemPatterns.md): Astro Islands mimarisi, Apple stili header deseni, PocketBase şeması.
  - [`techContext.md`](file:///vault/memory-bank/techContext.md): Teknoloji sürümleri ve performans bütçeleri.
  - [`progress.md`](file:///vault/memory-bank/progress.md): Canlı ilerleme ve kontrol tablosu.

- **`vault/rules/`** (Proje Kuralları):
  - [`design-principles.md`](file:///vault/rules/design-principles.md): `pbakaus/impeccable` ve Apple estetiği (ferah beyaz tema, dinamik yarı saydam su damlası header, 60/120fps CSS animasyonlar).
  - [`copywriting-anti-slop.md`](file:///vault/rules/copywriting-anti-slop.md): `petergyang/no-ai-slop` prensipleri (robotik AI metinleri yerine samimi, net ve güven veren kurumsal Türkçe metinler).
  - [`performance-and-seo.md`](file:///vault/rules/performance-and-seo.md): PageSpeed 100/100 ve Google keşif kılavuzu (Schema.org JSON-LD, 0-JS adaları).
  - [`tech-standards.md`](file:///vault/rules/tech-standards.md): Kodlama standartları ve PocketBase entegrasyonu.
  - [`memory-bank-rules.md`](file:///vault/rules/memory-bank-rules.md): Cline Memory Bank işletim protokolleri.

---

## ⚡ Landing Page Sıralaması & Temel Özellikler

1. **Site Yönetimi** (`#site-yonetimi`):
   - Apple benzeri su damlası şeffaf header altında modern bina görseli ve KMK şeffaf yönetim vurgusu.
   - **Artan Apartman & Daire Sayacı** (`StatsCounter.astro`): `185+ Apartman & Site`, `3.450+ Daire`, `%98.4 Tahsilat`, `28+ SGK'lı Personel`.
   - **4 Temel Güvence**: Mali ve Finansal Şeffaflık, KMK Hukuki Takip & İcra, Teknik & Tesisat Bakımı, SGK Bordrolama.
2. **Temizlik Hizmetleri** (`#temizlik`):
   - Gerçek fotoğraflı 4 kurumsal kart: Ofis temizliği, vinçli dış cephe cam yıkama, inşaat sonrası temizlik, apartman merdiven hijyeni.
3. **Neden Çelebi?** (`#neden-biz`):
   - Geleneksel/amatör riskler ile Çelebi kurumsal standartlarının 4 maddelik birebir karşılaştırma tablosu & Sıfır Risk Garantisi.
4. **Referanslar** (`#yorumlar`):
   - 5 yıldızlı doğrulanmış site yöneticisi ve şirket yetkilisi değerlendirmeleri.
5. **Son Yazılar** (`#yazilar`):
   - Google SEO organik arama otoritesi için 6 adet kapsamlı teknik makale ve arama etiketleri.
6. **İletişim & Teklif Formu** (`#iletisim`):
   - Hızlı fiyat teklifi formu, PocketBase veri entegrasyonu, doğrudan telefon ve WhatsApp hatları.
7. **Sıkça Sorulan Sorular** (`#sss`):
   - İletişim formunun hemen altında akordeon ve Google `FAQPage` Schema.org JSON-LD.
8. **Blog & Rehber Sistemi**:
   - `/yazilar` (ve `/blog` yönlendirmesi): Kategori filtreli rehber makaleleri.
   - `/yazilar/[slug]`: Apple Newsroom / Medium kalitesinde editoryal detay sayfaları ve `Article` JSON-LD zengin sonuçları.

---

## 🚀 Çalıştırma

```bash
# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev

# Canlı dağıtım için statik derle
npm run build

# Canlı derlemeyi yerelde önizle
npm run preview
```
