# Active Context: Çelebi Yönetim ve Temizlik

## 1. Current Work Focus
- **Phase**: Mobile Hamburger Menu Fix Deployed & Nuper Ortho Architecture Evaluated.
- **Recent Actions**:
  1. **Mobil Hamburger Menü Onarımı (`Header.astro`)**:
     - Kök Neden: `initScrollCoordinator()` fonksiyonunun hem `DOMContentLoaded` hem `window.load` üzerinde birden fazla kez tetiklenmesi sonucu `mobile-menu-toggle` butonuna çift tıklama dinleyicisi (listener) ekleniyordu. İlk dinleyici menüyü açarken, aynı tıklama kuyruğundaki ikinci dinleyici anında kapatıyordu.
     - Çözüm: `setupMobileMenu()` ve `initScrollCoordinator()` modülleri idempotency (tekil çalıştırma) korumasına alındı.
     - Dışarı tıklayınca kapatma (click-outside), Escape tuşuyla kapatma ve mobilde menü içi linke basınca otomatik kapanma eklendi.
     - Mobilde taşmaları önlemek için `max-h-[calc(100vh-5.5rem)] overflow-y-auto` ve dokunmatik alanı rahatlatan 44px dairesel buton stili uygulandı.
  2. **Dağıtım & Canlı Doğrulama**:
     - `npm run build` başarıyla tamamlandı.
     - Git commit: `55c1341` push edildi.
     - Vercel production deploy: `https://celebi-yonetim-temizlik.vercel.app` anında güncellendi.

---

## 2. Next Steps
- Kullanıcıya giriş bilgileri ve panel özelliklerinin detaylı tanıtılması.
