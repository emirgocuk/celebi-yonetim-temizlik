# Active Context: Çelebi Yönetim ve Temizlik

> Son Güncelleme: **22 Kasım 2026**

## 1. Current Work Focus & Production Snapshot
- **Canlı Sistem:** Site `https://celebiyonetim.com.tr/` adresinde **Ubuntu VDS (`2.27.101.128`)** üzerinde **Nginx + PocketBase `v0.41.1` (`127.0.0.1:8090`) + Cloudflare CDN** mimarisiyle yayındadır.
- **Statik Çıktı & Teknik SEO Durumu:** **48** statik Astro sayfası, **44** adet eğik çizgi (`trailingSlash: 'always'`) uyumlu canonical URL içeren `sitemap.xml` ve canlı URL'lerde **0 adet `301` yönlendirmesi** ile tam indekslemeye hazırdır.
- **Kurumsal Kimlik & İletişim (Adana Odaklı):**
  - **Adres:** `Mahfesığmaz Mah. 78033 Sk. No: 3 Zemin Kat, Çukurova / Adana`
  - **Sabit Hat:** `0 (322) 235 15 88`
  - **Temizlik Hattı:** `0 (533) 597 59 81`
  - **Yönetim & WhatsApp Hattı:** `0 (535) 873 03 24` (`905358730324`)
  - **E-Posta:** `iletisim@celebiyonetim.com.tr`
  - **Hedef İlçeler:** Çukurova, Seyhan, Sarıçam, Yüreğir (Adana).

---

## 2. Recent Completed Actions (Kasım 2026 Sprintleri)

1. **GSC Sitemap Temizliği & Otomatik İndeksleme Senkronizasyonu:**
   - Hatalı eklenen XML dışı sitemap (`site-yonetimi-fiyat-hesapla/`) GSC API üzerinden kaldırıldı; yalnızca `https://celebiyonetim.com.tr/sitemap.xml` bırakıldı.
   - `astro.config.mjs` içine `trailingSlash: 'always'` eklendi; `SEO.astro`, `yazilar/[slug].astro`, `sitemap.xml.ts` ve `scripts/gsc-auto-index.py` canonical/sitemap URL'leri sıfır `301` olacak şekilde hizalandı.
   - 44 URL'lik temiz sitemap hem GSC API (`PUT`) hem de IndexNow (`HTTP 200`) üzerinden gönderildi.

2. **Otonom AI İçerik Motoru Düzeltmesi, Tekil Temizlik & 48 Saatlik Döngü:**
   - `scripts/timer-runner.py`, `src/pages/merkez.astro` ve `src/pages/yazilar/[slug].astro` güncellendi.
   - Sessiz hata veren tek modelli yapı yerine 4 aşamalı OpenRouter ücretsiz yedekleme zinciri kuruldu: `nvidia/nemotron-3-ultra-550b-a55b:free` (`reasoning: {"enabled": False}`), `baidu/ernie-5.5-flash-preview:free`, `openrouter/free` ve `nvidia/nemotron-3.5-lightning:free` (`max_tokens: 4000`, `timeout=60`).
   - Sıkı HTML kalite kapısı (`>= 3` `<h2>`, `<p>`, `>= 260` kelime), 30 dakikalık hata bekleme mekanizması (`/tmp/celebi-ai-backoff.ts`) ve **"AI başarısız olursa şablon/boilerplate makale asla yayımlama"** kuralı eklendi.
   - `scripts/cleanup-and-enrich-articles.py` ile 5 kopya makale silindi, kalan **23** tekil PocketBase makalesinin tamamı yeniden yazıldı (`Temizlik: 14`, `Hukuk & Mevzuat: 6`, `Site Yönetimi: 3`) ve `otomatik_yayin_ayarlari` sıklığı `48h` (`aktif: true`, `hedefIlce: "auto"`) olarak ayarlandı.

3. **Anlık Talep Bildirim Motoru (`pb_hooks` + `ntfy.sh` / SMTP / Telegram):**
   - `scripts/pb_hooks/lead_notify_lib.js`, `scripts/pb_hooks/lead_notify.pb.js` ve `scripts/setup-notifications-pb.py` oluşturuldu; `scripts/deploy-to-vds.py` içine `pb_hooks` senkronizasyonu eklendi.
   - Sadece süper kullanıcı erişimli (`null` kural) `bildirim_ayarlari` koleksiyonu (`1afdyxr5l4cpk5q`) ve korumalı `POST /api/celebi/test-notify` uç noktası açıldı; `/merkez` paneline `#notification-settings-card` eklendi.
   - **`ntfy.sh` telefona anlık push bildirimleri kullanıcı tarafından test edilip onaylandı**; E-posta/SMTP ve Telegram kanalları da hazır durumda.

4. **GTM + GA4 + Google Search Console API Tam Entegrasyonu:**
   - `GTM-M7CC26B5` etiketi `src/layouts/BaseLayout.astro` `<head>` bölümüne gömüldü ve `G-74ZHMJ1VEJ` (`properties/565409453`) ile çift sayımı önleyen `preloadedGoogleIds` koruması devreye alındı.
   - Özel Google Cloud projesi `celebi-yonetim` için servis hesabı (`celebi-api@celebi-yonetim.iam.gserviceaccount.com`) oluşturuldu (kimlik dosyası git-dışı `vault/credentials/gsc-service-account.json` ve VDS `/var/www/credentials/gsc-service-account.json` `chmod 600` üzerinde tutulmaktadır).
   - Tekrar kullanılabilir CLI raporlama aracı `scripts/google-analytics-gsc-report.py` ve Windows başlatıcısı `scripts/google-baglan.cmd` (`--check`, `--report`, `--index-now`) kuruldu.
   - `scripts/setup-ga4-marketing.py` ile GA4 (`properties/565409453`) üzerinde **Google Signals** aktifleştirildi, veri saklama **14 aya** çıkarıldı, 3 temel olaydaki (`generate_lead`, `whatsapp_click`, `phone_call_click`, `ONCE_PER_SESSION`) sahte `1 USD` varsayılan değer temizlendi, 3 özel boyut (`service_type`, `method`, `landing_page`) ve kalıcı dönüşüm yapanları hariç tutan 3 adet **90 günlük yeniden pazarlama kitlesi** (`Fiyat Hesaplayıp Form Bırakmayanlar`, `Site Yönetimi İnceleyenler (Adana)`, `Temizlik Hizmeti İnceleyenler (Adana)`) oluşturuldu.

5. **KMK İnteraktif Araçlar & Google Ads Ön Hazırlığı:**
   - Canlı kişiselleştirici çubuklu, 5 hazır KMK şablonlu (Yönetim Değişikliği, Fesih & Devir, Genel Kurul Temizlik, Çağrı İlanı, Aidat İhtarname KMK md. 20), kopyala/WhatsApp/yazdır özellikli ve `FAQPage` şemalı `/apartman-karar-defteri-ornekleri/` sayfası yayınlandı.
   - `docs/adana-google-ads-negatif-kelimeler.txt` (`137` Türkçe negatif kelime) ve kampanya kurulum rehberi (`adana_reklam_ve_negatif_kelime_paketi.md`) hazırlandı.

---

## 3. Active Strategic Decisions

- **Meta Business / Meta Pixel (Instagram & Facebook):** Kullanıcının kararıyla **"şimdilik dursun"** statüsünde ertelendi.
- **Google Ads Başlangıç Stratejisi (Mutabık Kalınan Plan):**
  - **Ön Koşul:** Önce **Google İşletme Profili (Haritalar)** eksiksiz doldurulacak ve en az **5–10 gerçek 5 yıldızlı yorum + gerçek fotoğraf** eklenecek.
  - **Başlangıç Zamanı:** Haritalar profili tamamlandığı **hemen sonraki Pazartesi sabahı 08:30**.
  - **Test Bütçesi:** **14 günlük kontrollü test — günlük 350–500 ₺ (toplam 5.000–7.000 ₺)**. 15. günden itibaren yalnızca dönüşüm getiren kelimelerde günlük 600–1.000 ₺ bandına ölçekleme.
  - **Para Yakmayan Kurallar:** Yalnızca **Arama Ağı** (Görüntülü Reklam Ağı ve Arama Ortakları kapalı); Konum = Çukurova, Seyhan, Sarıçam, Yüreğir + **"Varlık" (Presence)**; ilk 15 gün yalnızca `[tam eşleme]` + `"sıralı eşleme"` ve **137 negatif kelime**; ilk 10–14 gün **Tıklamaları Artırma (Maks. TBM 35–40 ₺ tavan)**, 15–20+ GA4 dönüşümü birikince **Dönüşümleri Artırma**; Reklam Zaman Planlaması **Pzt–Cmt 08:30–19:30** (`ntfy.sh` + 5 dakikada geri dönüş kuralıyla eşzamanlı); Arama/Yer/Site Bağlantısı uzantıları + ilk 72 saat akşam **Arama Terimleri** temizliği.
  - **Kurulum Yöntemi:** Kullanıcı Google Ads oturumu ve faturalandırmayı açtığında, ajan tarayıcı üzerinden veya Google Ads Editor `.csv` paketiyle kampanyaları **duraklatılmış** şekilde kurabilir ve `AW-...` ID'lerini `/merkez` paneline işleyebilir.
- **Soğuk Başlangıç "Aktifleştirme Enerjisi" Yol Haritası (Sıradaki Oturum Odağı):**
  1. Yeni yüksek arama hacimli/paylaşılabilir araç sayfası: **Aidat Gecikme Tazminatı (%5 KMK md. 20) & Kapıcı Aylık İşveren Maliyeti Hesaplayıcı** (WhatsApp'ta paylaşılabilir sonuç kartı + dönüşüm CTA'sı ile).
  2. **0 ₺ Aktifleştirme Paketi:** Adana apartman WhatsApp grupları, mahalle Facebook grupları ve haftalık Google Haritalar gönderileri için hazır değer odaklı paylaşım metinleri + ücretsiz yerel NAP/dizin kayıt kontrol listesi (Apple Maps, Yandex Haritalar, LinkedIn, YouTube Shorts vb.).
  3. Haritalar ve yorumlar hazır olduğunda duraklatılmış Google Ads 14 günlük testini başlatıp `scripts/google-baglan.cmd` ile 7. ve 14. gün optimizasyonu yapmak.

---

## 4. Operational Reminders & Dirty Working Tree Notları
- Çalışma klasöründe önceki süreçlerden kalma sahiplenilmemiş/commit edilmemiş yerel logo ve görsel üretim artıkları bulunmaktadır (`.gitignore`, `public/assets/logo/celebi-logo.svg`, `public/assets/images/0d41a88a-d091-4eca-8616-f1234ff03f67.jpg`, `scripts/generate-refined-ca-logos.py`, `scripts/generate-svg-logos.py`, `scripts/__pycache__/`). Kullanıcı açıkça istemedikçe bu dosyaları **asla stage etmeyin, commit etmeyin veya silmeyin**.
- Herhangi bir dokümantasyon veya kod dosyasına **asla** gerçek şifre, API anahtarı veya özel anahtar yazmayın.
