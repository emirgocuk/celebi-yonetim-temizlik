# Product Context: Çelebi Yönetim ve Temizlik

> Son Güncelleme: **22 Kasım 2026**

## 1. Why This Project Exists
Toplu yaşam alanlarının (apartmanlar, siteler, iş merkezleri) yönetimi ve ticari/bireysel temizlik sektörü, **Adana** yerel pazarında yüksek rekabetin olduğu ancak güven ve şeffaflık açığının en yoğun yaşandığı sektörlerin başında gelir.

Çelebi Yönetim ve Temizlik (Mahfesığmaz, Çukurova / Adana merkezli; Çukurova, Seyhan, Sarıçam ve Yüreğir hizmet ağı), bu sektördeki *"güvensizlik, kayıt dışı personel ve şeffaf olmayan aidat takibi"* sorununu kurumsal disiplin, **634 sayılı Kat Mülkiyeti Kanunu'na tam uyum** ve **SGK belgeli** profesyonel temizlik ekipleriyle çözmektedir.

Bu web sitesinin temel varlık sebebi:
1. **Güven ve Otorite İnşa Etmek**: Potansiyel müşteriye ilk 3 saniyede *"İşte Adana'da aradığımız kurumsal, yasal mevzuata hakim ve güvenilir çözüm ortağı"* hissini vermek.
2. **Google'da Keşfedilebilirliği & Aktifleştirme Enerjisini Başlatmak**: 44 temiz URL'li sıfır-301 teknik SEO mimarisi, ilçe bazlı açılış sayfaları ve yöneticilerin WhatsApp gruplarında paylaşabileceği interaktif ücretsiz araçlarla (*Fiyat Hesaplayıcı*, *KMK Karar Defteri Örnekleri*, planlanan *Gecikme Tazminatı & Kapıcı Maliyeti Hesaplayıcı*) yerel arama trafiğini ve marka bilinirliğini büyütmek.
3. **Sürtünmesiz Dönüşüm ve 5 Dakikada Geri Dönüş Sağlamak**: Ziyaretçiyi uzun formlarla yormadan *"5 Dakikada Arayalım"*, WhatsApp direkt hat ve PocketBase sıfır-kayıplı teklif köprüsü üzerinden `ntfy.sh` anlık telefon bildirimiyle talepleri dakikalar içinde sıcak görüşmeye çevirmek.

---

## 2. Target Audience & Personas

### Persona A: Site / Apartman Karar Vericisi (Kemal Bey, 52 — Çukurova / Seyhan)
- **Rolü**: 40–60 dairelik bir sitenin denetçisi veya yönetim değişikliği arayan kat maliki.
- **Acı Noktaları**: Aidat toplamada komşuluk ilişkilerinin zedelenmesi, geciken ödemeler, asansör/kazan bakımının aksaması, şeffaf olmayan harcamalar, yönetim devir prosedürünü bilmeme.
- **İhtiyacı**: KMK'ya hakim, hazır genel kurul karar şablonları sunan, aidatı banka ve icra takibiyle şeffaf yöneten kurumsal bir yönetim firması.

### Persona B: Kurumsal Ofis / Tesis Müdürü (Selin Hanım, 36 — Adana İş Merkezleri)
- **Rolü**: Bir iş merkezinde çok katlı ofisin İdari İşler Müdürü.
- **Acı Noktaları**: Kayıt dışı/sigortasız temizlik personeli iş güvenliği riski, personelin habersiz gelmemesi, fatura ve sözleşme düzensizliği.
- **İhtiyacı**: Sözleşmeli, SGK belgeli ve sabit eğitimli personeli olan, denetlenen ve faturalı düzenli kurumsal temizlik hizmeti.

### Persona C: Mülk Sahibi / İnşaat Müteahhidi (Murat Bey, 44 — Çukurova / Sarıçam)
- **Rolü**: Yeni tamamlanan konut projesinin müteahhidi veya ilk yönetim kurulumunu yapacak site yöneticisi.
- **Acı Noktaları**: Teslim öncesi inşaat artıklarının (derz, boya, kireç) yüzeylere zarar vermeden temizlenmesi ve bina ilk genel kurul/aidat bütçesinin eksiksiz kurulması.
- **İhtiyacı**: Ağır inşaat temizliğine uygun endüstriyel ekipmanlı temizlik ekibi + bina teslim sonrası doğrudan profesyonel site yönetimi devri.

---

## 3. Core Experience, UX & Growth Flywheel ("Aktifleştirme Enerjisi")

1. **"Ferah ve Tertemiz" Görsel Atmosfer**:
   - Havadar beyaz alanlar, keskin kontrast, mobil öncelikli okunabilir tipografi ve Apple tarzı buzlu cam başlık (`backdrop-blur`).
2. **Fayda Odaklı İnteraktif Araçlar (Organik Trafik Mıknatısı)**:
   - `/site-yonetimi-fiyat-hesapla/`: Daire sayısına göre tahmini yönetim maliyeti ve görevli kıyaslaması.
   - `/apartman-karar-defteri-ornekleri/`: KMK uyumlu, canlı site adıyla doldurulabilen, kopyalanabilir ve WhatsApp'tan paylaşılabilir hazır karar ve ihtarname metinleri.
   - *(Planlanan)* **Aidat Gecikme Tazminatı (%5 KMK md. 20) & Kapıcı Maliyeti Hesaplayıcı**: Yönetici ve apartman gruplarında yüksek aranma/paylaşılma potansiyelli araç.
3. **Anlık Bildirim + 5 Dakika Geri Dönüş + Kontrollü Arama Reklamı**:
   - Form, WhatsApp (`whatsapp_click`) veya telefon (`phone_call_click`) etkileşimleri `GTM-M7CC26B5` → `GA4 (G-74ZHMJ1VEJ)` ile ölçülürken aynı anda `pb_hooks` + `ntfy.sh` üzerinden yönetici telefonuna düşer.
   - Haritalar (Google İşletme Profili) yorumları tamamlandığında 14 günlük kontrollü Adana Arama Ağı testi (yalnızca mesai saatleri ve 137 negatif kelime kalkanıyla) ilk sıcak müşteri ve marka araması kıvılcımını hızlandırır.
