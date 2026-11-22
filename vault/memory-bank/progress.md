# Project Progress: Çelebi Yönetim ve Temizlik

> Son Güncelleme: **22 Kasım 2026**

## Work Completed

### A. Temel Mimari, Marka Kimliği & Kurumsal Güven
- [x] Vault ve Memory Bank mimarisi kuruldu (`vault/memory-bank`, `vault/rules`).
- [x] Astro (`^7.4.7`), Tailwind CSS v4 (`@tailwindcss/vite`), TypeScript ve PocketBase (`v0.41.1`) altyapısı kuruldu.
- [x] `pbakaus/impeccable` ve `petergyang/no-ai-slop` kurallarına uygun beyaz/ferah tasarım sistemi, su damlası şeffaf header ve kayan kapsül navigasyon tamamlandı.
- [x] Yatay çerçevesiz vektörel SVG marka logosu (`celebi-logo.svg`) ve önbellek kırmalı (`cache-bust`) favicon seti entegre edildi.
- [x] Gerçek Adana kurumsal iletişim bilgileri (Mahfesığmaz Mah. 78033 Sk. No: 3, Çukurova/Adana; `0 322 235 15 88`, `0 533 597 59 81`, `0 535 873 03 24`), Google Maps iframe ve **Çukurova / Seyhan / Sarıçam / Yüreğir** Schema.org `LocalBusiness` verileri işlendi.
- [x] KVKK aydınlatma metni, çerez onayı, sözleşmeler ve altbilgi yasal merkezi (`/hukuk`) eklendi; müşteri yorumları KVKK uyumlu anonimleştirildi.
- [x] Agentic Browsing & Lighthouse denetim iyileştirmeleri tamamlandı (`llms.txt`, `ard.json`, yıldız derecelendirme `role="img"` ARIA etiketleri).

### B. Dönüşüm (CRO) & Adana Yerel SEO Sayfaları
- [x] Özel hizmet ve ilçe iniş sayfaları yayına alındı: `/site-yonetimi/`, `/temizlik/`, `/cukurova-site-yonetimi/`, `/seyhan-apartman-yonetimi/`, `/saricam-site-yonetimi/`.
- [x] İnteraktif **Site Yönetimi Fiyat & KMK Maliyet Hesaplayıcı** (`/site-yonetimi-fiyat-hesapla/`) ve **"5 Dakikada Arayalım" (`QuickCallbackBar`)** bileşenleri eklendi.
- [x] İnteraktif **Apartman Karar Defteri & KMK İhtarname Örnekleri** sayfası (`/apartman-karar-defteri-ornekleri/`) canlı metin kişiselleştirme, tek tıkla kopyala/WhatsApp/yazdır ve `FAQPage` şemasıyla yayına alındı.
- [x] Masaüstü sağ alt dairesel su damlası iletişim butonları ve mobil sabit alt arama/WhatsApp çubuğu eklendi.
- [x] WhatsApp + sıfır kayıplı teklif köprüsü (`teklif_talepleri` koleksiyonuna UTM/`gclid`/`fbclid` atıf verileriyle anında kayıt) tamamlandı.

### C. Üretim Sunucusu (VDS), Teknik SEO & Otomasyon
- [x] **Canlı VDS Yayını Aktif:** Ubuntu VDS (`2.27.101.128`) üzerinde Nginx (HTTP → HTTPS `301` ve statik sunum), systemd altında PocketBase `v0.41.1` (`127.0.0.1:8090`) ve Cloudflare CDN ile **`https://celebiyonetim.com.tr/`** canlıda (`48` statik sayfa).
- [x] `/merkez` yönetim paneli güvenli yönetici girişiyle (`emrggck@gmail.com`) devrede: gelen talepler, makale yönetimi, iletişim & reklam ID ayarları (`reklam_ayarlari`), otonom yayın zamanlayıcısı (`otomatik_yayin_ayarlari`) ve bildirim ayarları (`bildirim_ayarlari`).
- [x] `astro.config.mjs` içine `trailingSlash: 'always'` tanımlandı; tüm canonical etiketleri ve `sitemap.xml` (`44` URL) canlıda **0 adet `301` yönlendirmesi** verecek şekilde hizalandı.
- [x] GSC API (`PUT`) ve IndexNow (`HTTP 200`) otomatik indeksleme akışı (`scripts/gsc-auto-index.py`) ile tek komutluk dağıtım (`scripts/deploy-to-vds.py`) kuruldu.

### D. Otonom AI İçerik Motoru & Anlık Lead Bildirimleri
- [x] OpenRouter 4 modelli yedekli AI içerik motoru (`scripts/timer-runner.py`) kuruldu; kalite kapısı ve 30 dk hata bekleme ile şablon/boilerplate yayın ihtimali sıfırlandı.
- [x] `scripts/cleanup-and-enrich-articles.py` ile 5 kopya kayıt silindi, tüm **23** tekil makale sıfırdan zenginleştirildi ve 48 saatlik otomatik yayın döngüsü (`48h`, `aktif: true`) devreye alındı.
- [x] PocketBase `pb_hooks` tabanlı anlık talep bildirimi (`lead_notify_lib.js`, `lead_notify.pb.js`, süper kullanıcı korumalı `/api/celebi/test-notify` ve `bildirim_ayarlari`) kuruldu; **`ntfy.sh` telefona anlık push bildirimleri kullanıcı tarafından test edilip doğrulandı**.

### E. Ölçümleme (GTM / GA4 / GSC API) & Reklam Hazırlığı
- [x] `GTM-M7CC26B5` konteyneri ve `G-74ZHMJ1VEJ` (`properties/565409453`) çift sayım koruma mantığıyla (`preloadedGoogleIds`) canlıya alındı.
- [x] Google Cloud `celebi-yonetim` servis hesabı (`celebi-api@celebi-yonetim.iam.gserviceaccount.com`) hem GSC hem GA4 API'ye bağlandı; `scripts/google-analytics-gsc-report.py` ve `scripts/google-baglan.cmd` oluşturuldu.
- [x] `scripts/setup-ga4-marketing.py` ile Google Signals, 14 aylık veri saklama, temizlenmiş 3 dönüşüm olayı (`generate_lead`, `whatsapp_click`, `phone_call_click` — `ONCE_PER_SESSION`), 3 özel boyut (`service_type`, `method`, `landing_page`) ve 3 adet 90 günlük yeniden pazarlama kitlesi kuruldu.
- [x] Google Ads için 137 kelimelik Adana negatif anahtar kelime paketi (`docs/adana-google-ads-negatif-kelimeler.txt`) ve arama ağı kampanya taslağı (`adana_reklam_ve_negatif_kelime_paketi.md`) hazırlandı.

---

## Backlog / Next Up
- [ ] İnteraktif **Aidat Gecikme Tazminatı (%5 KMK md. 20) & Kapıcı Aylık İşveren Maliyeti Hesaplayıcı** sayfası + WhatsApp'ta paylaşılabilir sonuç kartı
- [ ] **0 ₺ Aktifleştirme Paketi** (Adana apartman WhatsApp grupları, mahalle Facebook grupları ve haftalık Google Haritalar gönderileri için paylaşım metinleri + yerel NAP/dizin kayıt kontrol listesi)
- [ ] **Google İşletme Profili (Haritalar)** eksiksiz tamamlama + ilk 5–10 gerçek 5 yıldızlı yorum & ofis/ekip fotoğrafı *(kullanıcı aksiyonu)*
- [ ] **Google Ads 14 Günlük Kontrollü Arama Ağı Testi** (günlük 350–500 ₺, yalnızca Çukurova/Seyhan/Sarıçam/Yüreğir "Varlık", `[tam]` + `"sıralı"` eşleme, 137 negatif kelime, Pzt–Cmt 08:30–19:30; tarayıcı veya Google Ads Editor `.csv` ile duraklatılmış kurulum + `/merkez` `AW-...` girişi)
- [ ] Reklam yayını sonrası 7. ve 14. gün GA4 / GSC / Arama Terimleri optimizasyon analizi
- [ ] Meta Business / Meta Pixel (`Instagram & Facebook`) entegrasyonu *(kullanıcı kararıyla şimdilik ertelendi)*

## Current Status
- `https://celebiyonetim.com.tr/` Ubuntu VDS + Cloudflare CDN üzerinde **%100 yayında**, otonom 48 saatlik makale motoru aktif, `ntfy.sh` anlık bildirimleri canlı ve GTM/GA4/GSC API veri toplama düzeni çalışır durumdadır. Sıradaki adım, organik "aktifleştirme enerjisi" araçlarını ekleyip Google Haritalar + kontrollü Google Ads testini başlatmaktır.
