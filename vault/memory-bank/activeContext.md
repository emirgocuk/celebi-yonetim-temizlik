# Active Context: Çelebi Yönetim ve Temizlik

## 1. Current Work Focus
- **Phase**: `/merkez` Admin Portal, Lead Inbox, Settings Synchronization & Google Maps Page Completed and Pushed.
- **Recent Actions**:
  1. **`/merkez` Yönetim Paneli**:
     - Giriş Kimlik Bilgileri: `admin@celebi.com` / `celebi.12` doğrulandı, tek tıkla demo doldur butonu eklendi.
     - **İletişim Formları & Gelen Talepler Modülü**: Gerçek zamanlı gelen teklif kayıtları listeleniyor. Her kayıt için doğrudan WhatsApp yanıtla, telefonla ara, durum değiştir (Yeni / İncelendi / Teklif Verildi) ve silme işlevleri eklendi.
     - **CEO & Otomatik Haber Oluşturucu (SEO) Modülü**: İleride gelecek olan yapay zeka haber motoru ve hazır tasarım entegrasyonu için mimari soketler, Trends takibi ve taslak simülasyon alanı hazırlandı.
     - **İletişim Bilgileri & Konum Ayarları Modülü**: WhatsApp numarası, telefon, e-posta, açık adres ve Google Maps harita embed URL düzenleme alanları eklendi. Yapılan değişiklikler `BaseLayout` üzerinden tüm sitede anında senkronize ediliyor.
  2. **İletişim & Konum Sayfası (`/iletisim`)**:
     - İnteraktif Google Haritalar iframe yerleşimi, açık adres, otopark/ulaşım rehberi, iletişim butonları ve teklif formu tek sayfada toplandı.
     - `QuoteForm.astro` üzerinde haritayı açan ve doğrudan forma bağlayan çift yönlü köprüler eklendi.
  3. **Güvenlik & SEO**:
     - `public/robots.txt` içine `Disallow: /merkez` eklenerek arama motorlarının paneli taraması engellendi.
     - `sitemap.xml.ts` güncellendi (`/iletisim` dahil edildi).
  4. **GitHub Senkronizasyonu**:
     - 11 dosya commit edilerek `https://github.com/emirgocuk/celebi-yonetim-temizlik` reposuna gönderildi.

---

## 2. Next Steps
- Kullanıcıya giriş bilgileri ve panel özelliklerinin detaylı tanıtılması.
