# Technical Context: Çelebi Yönetim ve Temizlik

> Son Güncelleme: **22 Kasım 2026**

## 1. Technology Stack Details

| Katman | Teknoloji | Sürüm / Yapılandırma | Açıklama |
|---|---|---|---|
| **Runtime** | Node.js | v22 LTS | Yerel geliştirme ve Astro statik build çalışma zamanı |
| **Paket Yöneticisi** | npm | Standart | Bağımlılık yönetimi (`package-lock.json`) |
| **Ön Yüz (Frontend)** | **Astro** | `^7.4.7` (`trailingSlash: 'always'`) | Sıfır JS varsayılanlı SSG + Islands mimarisi (`48` sayfa) |
| **Stil** | **Tailwind CSS** | `^4.0.0` (`@tailwindcss/vite`) | Hızlı CSS utility üretimi ve tasarım token'ları |
| **Tip Güvenliği** | TypeScript & `@astrojs/check` | `^5.7.3` / `^0.9.12` | Bileşen ve API istemcisi tip kontrolü |
| **Arka Uç (Backend)** | **PocketBase** | Sunucu `v0.41.1` / JS SDK `^0.25.0` | SQLite tabanlı REST API, Auth, `pb_hooks` (Goja) ve yönetim |
| **Üretim Sunucusu** | Ubuntu VDS + Nginx + Cloudflare CDN | VDS IP `2.27.101.128` | Nginx (`127.0.0.1:8090` reverse proxy + `/var/www/celebiyonetim/html`) |
| **Otomasyon & API** | Python 3 | `scripts/*.py` | VDS dağıtım, AI içerik zamanlayıcısı, GSC/GA4/IndexNow API araçları |
| **İkonlar & Tipografi** | Inline Lucide SVG + Sistem / Yerel Font | Sıfır harici font engeli | Hızlı boyama (FCP/LCP) ve sıfır kayma (`CLS = 0.00`) |

---

## 2. Development, Deployment & Operations Commands

### Yerel Geliştirme ve Build
```powershell
# PocketBase (127.0.0.1:8090) + Astro dev sunucusunu tek komutla başlat
npm run dev:all

# Sadece Astro dev sunucusu
npm run dev

# Üretim statik çıktısını (dist/) oluştur
npm run build
```

### VDS Dağıtım ve Sunucu Otomasyonu
```powershell
# Astro build + dist/, pb_hooks ve yardımcı betikleri Ubuntu VDS'e aktar
python scripts/deploy-to-vds.py

# GA4 pazarlama ayarlarını (Signals, key events, dimensions, audiences) doğrula/uygula
python scripts/setup-ga4-marketing.py

# PocketBase bildirim koleksiyonunu (bildirim_ayarlari) kur/doğrula
python scripts/setup-notifications-pb.py
```

### Google Analytics 4 & Search Console Raporlama / İndeksleme
```powershell
# Bağlantı durumunu kontrol et (GSC + GA4)
scripts\google-baglan.cmd --check

# Son dönem GSC arama sorguları + GA4 trafik ve dönüşüm raporunu çek
scripts\google-baglan.cmd --report

# Güncel sitemap ve sayfaları GSC + IndexNow üzerinden yeniden indekslemeye gönder
scripts\google-baglan.cmd --index-now
```

---

## 3. Credentials & Security Architecture

- **Git Dışı Tutulan Hassas Dosyalar (`.gitignore`):**
  - `.env` ve `.env.*` (`.env.example` hariç),
  - `*service-account*.json`, `credentials/`, `google-json/`, `*.pem`, `*.key`.
- **Google Cloud Servis Hesabı:**
  - Proje: `celebi-yonetim` | Hesap: `celebi-api@celebi-yonetim.iam.gserviceaccount.com`
  - Yetkiler: GA4 (`properties/565409453`) **Düzenleyici** + Google Search Console **Tam Yetkili**.
  - Yerel Konum: `vault/credentials/gsc-service-account.json` (git-dışı).
  - VDS Konumu: `/var/www/credentials/gsc-service-account.json` (`chmod 600`).
- **PocketBase Güvenliği:**
  - Süper kullanıcı hesabı: `emrggck@gmail.com` (`/merkez` ve `/_/`).
  - `bildirim_ayarlari` koleksiyonu tüm anonim/normal kullanıcı isteklerine kapalıdır (`null` API kuralları); test uç noktası `/api/celebi/test-notify` `$apis.requireSuperuserAuth()` korumalıdır.
- **Güvenlik İlkesi:** Vault, dokümantasyon ve betik şablonlarına **asla** gerçek şifre, API anahtarı veya özel anahtar yazılmaz.

---

## 4. Technical Constraints & Performance Budgets

1. **Zero-301 & Canonical Disiplini:** Tüm iç bağlantılar, canonical etiketleri ve `sitemap.xml` URL'leri sonu `/` ile bitmelidir (`trailingSlash: 'always'`).
2. **Core Web Vitals & PageSpeed Hedefleri:**
   - Açılış sayfalarında hafif/sıfır gereksiz JS (ağır animasyon kütüphanesi yok; GPU hızlandırmalı CSS geçişleri).
   - Görsellerde açık boyut / aspect-ratio (`CLS = 0.00`) ve harici engelleyici `@import` olmadan hızlı font sunumu.
3. **Analytics Çift Sayım Yasağı:** `GTM-M7CC26B5` ve `G-74ZHMJ1VEJ` halihazırda `<head>` üzerinden yönetildiğinden dinamik takip yükleyicisi bu kimlikleri tekrar `gtag()` ile yüklemez.

---

## 5. Environment Variables Specification (Güvenli Şablon)

Gerçek değerler yalnızca git-dışı `.env` dosyasında ve VDS ortamında tutulur:

```env
# 1. PocketBase Yapılandırması
POCKETBASE_URL="http://127.0.0.1:8090"
PUBLIC_POCKETBASE_URL="https://celebiyonetim.com.tr/api"
POCKETBASE_ADMIN_EMAIL="emrggck@gmail.com"
POCKETBASE_ADMIN_PASSWORD="<POCKETBASE_ADMIN_PASSWORD>"

# 2. Yapay Zeka / LLM Makale Motoru (OpenRouter) & Görsel (ImgBB)
OPENROUTER_API_KEY="<OPENROUTER_API_KEY>"
PUBLIC_OPENROUTER_API_KEY="<OPENROUTER_API_KEY>"
IMGBB_API_KEY="<IMGBB_API_KEY>"
PUBLIC_IMGBB_API_KEY="<IMGBB_API_KEY>"

# 3. Reklam & Dönüşüm İzleme (Boş bırakılırsa PocketBase reklam_ayarlari koleksiyonundan okunur)
PUBLIC_GA4_ID=""
PUBLIC_GADS_ID=""
PUBLIC_GADS_CONV_LEAD=""
PUBLIC_GADS_CONV_WHATSAPP=""
PUBLIC_GADS_CONV_CALL=""
PUBLIC_META_PIXEL_ID=""
```
