export interface LegalSection {
  id: string;
  title: string;
  content: string;
}

export interface LegalDocument {
  slug: string;
  shortTitle: string;
  title: string;
  badge: string;
  description: string;
  lastUpdated: string;
  effectiveDate: string;
  sections: LegalSection[];
}

export const LEGAL_DOCUMENTS: LegalDocument[] = [
  {
    slug: 'kvkk-aydinlatma-metni',
    shortTitle: 'KVKK Aydınlatma Metni',
    title: '6698 Sayılı Kişisel Verilerin Korunması Kanunu (KVKK) Aydınlatma Metni',
    badge: '6698 Sayılı Kanun Madde 10 Uyarınca',
    description: 'Çelebi Yönetim ve Temizlik olarak kişisel verilerinizin güvenliği ve gizliliğine azami hassasiyet gösteriyoruz. Kişisel verilerinizin işlenme amaçları, hukuki sebepleri ve haklarınız hakkında bilgilendirme.',
    lastUpdated: '10 Kasım 2026',
    effectiveDate: '10 Kasım 2026',
    sections: [
      {
        id: 'veri-sorumlusu',
        title: '1. Veri Sorumlusunun Kimliği',
        content: `6698 sayılı Kişisel Verilerin Korunması Kanunu (“KVKK”) uyarınca, **Çelebi Yönetim ve Temizlik** (“Şirket” veya “Veri Sorumlusu”) olarak, veri sorumlusu sıfatıyla, kişisel verilerinizi aşağıda açıklanan çerçevede ve mevzuat tarafından emredilen sınırlar dahilinde işlemekte, kaydetmekte ve korumaktayız.

* **Firma / Unvan:** Çelebi Yönetim ve Temizlik
* **Adres:** Mahfesığmaz Mah. 78033 Sk. No: 3 Zemin Kat, Çukurova / Adana
* **Telefon:** 0 (322) 235 15 88
* **E-Posta:** iletisim@celebiyonetim.com.tr
* **Web Sitesi:** https://celebiyonetim.com.tr`,
      },
      {
        id: 'islenen-veriler',
        title: '2. İşlenen Kişisel Veri Kategorileri',
        content: `Web sitemizi ziyaret etmeniz, teklif formlarını doldurmanız, telefon veya WhatsApp hatlarımız üzerinden bizimle iletişime geçmeniz veya hizmet sözleşmesi akdetmeniz hallerinde aşağıdaki verileriniz işlenebilmektedir:

* **Kimlik Bilgileri:** Ad, soyad, unvan (yönetici/malik/firma yetkilisi).
* **İletişim Bilgileri:** Telefon numarası, e-posta adresi, hizmet talep edilen apartman/site veya iş yeri adresi (ilçe, mahalle, sokak).
* **Müşteri İşlem Bilgileri:** Talep edilen hizmet türü (site yönetimi, apartman temizliği, ofis temizliği, inşaat sonrası temizlik vb.), daire veya blok sayısı, talep edilen özel şartlar ve teklif detayları.
* **İşlem Güvenliği ve Dijital İz Bilgileri:** IP adresi, internet sitesi giriş-çıkış saatleri, tarayıcı bilgileri ve çerez (cookie) kayıtları.`,
      },
      {
        id: 'islenme-amaclari',
        title: '3. Kişisel Verilerin İşlenme Amaçları',
        content: `Toplanan kişisel verileriniz, KVKK’nın 5. ve 6. maddelerinde belirtilen şartlara uygun olarak aşağıdaki amaçlarla işlenmektedir:

* Tarafınızca talep edilen site/apartman yönetimi ve temizlik hizmetlerine ilişkin fiyat tekliflerinin hazırlanması ve tarafınıza iletilmesi,
* Kat Mülkiyeti Kanunu (KMK) çerçevesinde site yönetimi işletme projelerinin hazırlanması ve yasal süreçlerin yürütülmesi,
* Kurumsal temizlik operasyonlarının planlanması, keşif randevularının organize edilmesi ve personel görevlendirmesi,
* Müşteri ilişkileri yönetimi, talep ve şikayetlerin değerlendirilmesi ve çözüme kavuşturulması,
* Yasal mevzuattan kaynaklanan bilgi saklama, raporlama ve bildirim yükümlülüklerinin yerine getirilmesi,
* Faturalandırma, muhasebe ve tahsilat süreçlerinin yürütülmesi,
* Web sitemizin güvenliğinin sağlanması ve teknik hataların giderilmesi.`,
      },
      {
        id: 'hukuki-sebepler',
        title: '4. Kişisel Veri Toplamanın Yöntemi ve Hukuki Sebebi',
        content: `Kişisel verileriniz; web sitemiz üzerindeki teklif ve iletişim formları, telefon görüşmeleri, WhatsApp yazışmaları, e-posta iletileri ve yüz yüze yapılan keşif/görüşmeler aracılığıyla otomatik veya otomatik olmayan yöntemlerle toplanmaktadır.

Bu veriler KVKK Madde 5/2 kapsamında şu hukuki sebeplere dayanılarak işlenmektedir:
* **Sözleşmenin Kurulması veya İfası (c bendi):** Bir sözleşmenin kurulması veya ifasıyla doğrudan doğruya ilgili olması kaydıyla, sözleşmenin taraflarına ait kişisel verilerin işlenmesinin gerekli olması.
* **Hukuki Yükümlülük (ç bendi):** Veri sorumlusunun hukuki yükümlülüğünü yerine getirebilmesi için zorunlu olması (KMK, Vergi Usul Kanunu, SGK mevzuatı).
* **Meşru Menfaat (f bendi):** İlgili kişinin temel hak ve özgürlüklerine zarar vermemek kaydıyla, veri sorumlusunun meşru menfaatleri için veri işlenmesinin zorunlu olması (müşteri memnuniyeti, hizmet kalitesi denetimi).`,
      },
      {
        id: 'aktarim',
        title: '5. Kişisel Verilerin Aktarılması',
        content: `Toplanan kişisel verileriniz; kesinlikle üçüncü şahıslara ticari amaçla satılmaz, kiralanmaz veya yetkisiz olarak paylaşılmaz. Kişisel verileriniz yalnızca;
* Kanunen yetkili kamu kurum ve kuruluşlarına (Mahkemeler, İcra Daireleri, SGK, Vergi Daireleri) yasal zorunluluklar sınırında,
* Bankacılık ve online aidat/fatura ödeme altyapısını sağlayan lisanslı finansal kuruluşlara,
* Hizmetin ifası için zorunlu olan teknik, hukuki veya mali danışmanlarımıza gizlilik sözleşmeleri tahtında aktarılabilir.

Yurt dışına herhangi bir veri aktarımı gerçekleştirilmemektedir.`,
      },
      {
        id: 'haklar',
        title: '6. İlgili Kişinin KVKK Madde 11 Kapsamındaki Hakları',
        content: `Kişisel veri sahibi olarak KVKK’nın 11. maddesi uyarınca aşağıdaki haklara sahipsiniz:
* Kişisel verilerinizin işlenip işlenmediğini öğrenme,
* Kişisel verileriniz işlenmişse buna ilişkin bilgi talep etme,
* Kişisel verilerinizin işlenme amacını ve bunların amacına uygun kullanılıp kullanılmadığını öğrenme,
* Yurt içinde veya yurt dışında kişisel verilerin aktarıldığı üçüncü kişileri bilme,
* Kişisel verilerin eksik veya yanlış işlenmiş olması hâlinde bunların düzeltilmesini isteme,
* KVKK 7. maddede öngörülen şartlar çerçevesinde kişisel verilerin silinmesini veya yok edilmesini isteme,
* Yapılan işlemlerin verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme,
* İşlenen verilerin münhasıran otomatik sistemler vasıtasıyla analiz edilmesi suretiyle aleyhinize bir sonucun ortaya çıkmasına itiraz etme,
* Kişisel verilerin kanuna aykırı olarak işlenmesi sebebiyle zarara uğramanız hâlinde zararın giderilmesini talep etme.`,
      },
      {
        id: 'basvuru',
        title: '7. Başvuru Usul ve Şekli',
        content: `Yukarıda belirtilen haklarınızı kullanmak için kimliğinizi tespit edici belgeler ile birlikte:
1. Islak imzalı bir dilekçe ile **Mahfesığmaz Mah. 78033 Sk. No: 3 Zemin Kat, Çukurova / Adana** adresimize bizzat teslim edebilir veya noter kanalıyla gönderebilir,
2. Güvenli elektronik imza veya mobil imza kullanarak **iletisim@celebiyonetim.com.tr** adresine e-posta ile iletebilirsiniz.

Talebiniz niteliğine göre en geç 30 (otuz) gün içerisinde ücretsiz olarak sonuçlandırılacaktır.`,
      },
    ],
  },
  {
    slug: 'gizlilik-politikasi',
    shortTitle: 'Gizlilik ve Veri Güvenliği',
    title: 'Gizlilik ve Veri Güvenliği Politikası',
    badge: 'Bilgi Güvenliği Standartları',
    description: 'Çelebi Yönetim ve Temizlik olarak internet sitemizi ziyaret eden tüm kullanıcılarımızın, müşterilerimizin ve iş ortaklarımızın gizlilik haklarını korumayı temel ilke kabul ediyoruz.',
    lastUpdated: '10 Kasım 2026',
    effectiveDate: '10 Kasım 2026',
    sections: [
      {
        id: 'gizlilik-taahhut',
        title: '1. Gizlilik Taahhüdümüz',
        content: `Çelebi Yönetim ve Temizlik, çevrim içi kanallarımız (web sitesi, iletişim formları, WhatsApp destek hatları) ve saha operasyonlarımız üzerinden paylaştığınız tüm kişisel ve kurumsal bilgilerin gizliliğini korumayı yasal ve etik bir sorumluluk olarak kabul eder. Sitemizi ziyaret eden kullanıcıların bilgileri, kullanıcının açık onayı veya yasal zorunluluk olmaksızın üçüncü taraflarla paylaşılmaz.`,
      },
      {
        id: 'bilgi-guvenligi',
        title: '2. Bilgi Güvenliği ve Altyapı Önlemleri',
        content: `Kişisel verilerinizin kaybolmasını, kötüye kullanılmasını veya yetkisiz erişimini engellemek için sektör standardı teknik ve idari güvenlik önlemleri uygulanmaktadır:
* **SSL / TLS Şifreleme:** Web sitemizdeki tüm veri akışı 256-bit SSL güvenlik sertifikası ile şifrelenmektedir. Formlar aracılığıyla gönderdiğiniz veriler uçtan uca koruma altındadır.
* **Yetki Sınırlaması:** Müşteri ve bina verilerine yalnızca görevi gereği bu verilere erişmesi zorunlu olan yetkili personel erişebilmektedir.
* **Gizlilik Sözleşmeleri:** Sahada görev yapan bina yöneticilerimiz ve temizlik personelimiz, hizmet verilen mülklerdeki her türlü ticari ve özel bilginin gizliliğini koruyacaklarına dair yasal gizlilik taahhütnamesi imzalamaktadır.`,
      },
      {
        id: 'ucuncu-taraflar',
        title: '3. Üçüncü Taraf Bağlantıları',
        content: `Web sitemiz; harita gösterimi (Google Maps), anlık iletişim (WhatsApp) veya sektörel bilgi bağlantıları içerebilir. Bu harici platformların kendilerine ait gizlilik ve güvenlik politikaları bulunmakta olup, bu sitelerin uygulamalarından veya içeriklerinden firmamız sorumlu tutulamaz. Harici bağlantıları kullanırken ilgili platformların gizlilik metinlerini incelemeniz önerilir.`,
      },
      {
        id: 'veri-imha',
        title: '4. Veri Saklama ve İmha Politikası',
        content: `Toplanan kişisel veriler, ilgili mevzuatta öngörülen saklama süreleri boyunca veya işleme amacının gerektirdiği süre zarfında muhafaza edilir. Amacın ortadan kalkması veya yasal saklama sürelerinin dolması durumunda kişisel veriler, Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi Hakkında Yönetmelik hükümlerine uygun olarak imha edilir.`,
      },
      {
        id: 'degisiklikler',
        title: '5. Politikada Yapılacak Güncellemeler',
        content: `Firmamız, yürürlükteki mevzuatta meydana gelebilecek değişiklikler veya şirket içi operasyonel gereksinimler doğrultusunda işbu Gizlilik Politikası'nda değişiklik yapma hakkını saklı tutar. Güncellenen politika metni web sitesinde yayımlandığı tarihten itibaren geçerlilik kazanır.`,
      },
    ],
  },
  {
    slug: 'cerez-politikasi',
    shortTitle: 'Çerez (Cookie) Politikası',
    title: 'Çerez (Cookie) Politikası ve Çerez Yönetimi',
    badge: 'Şeffaf Çerez Yönetimi',
    description: 'Web sitemizde ziyaretçi deneyimini iyileştirmek, site güvenliğini sağlamak ve site performansını analiz etmek amacıyla kullanılan çerezler hakkında bilgilendirme.',
    lastUpdated: '10 Kasım 2026',
    effectiveDate: '10 Kasım 2026',
    sections: [
      {
        id: 'cerez-nedir',
        title: '1. Çerez (Cookie) Nedir?',
        content: `Çerezler, bir web sitesini ziyaret ettiğinizde tarayıcınız aracılığıyla bilgisayarınıza, tabletinize veya akıllı telefonunuza kaydedilen küçük metin dosyalarıdır. Çerezler, web sitesinin düzgün ve güvenli çalışmasını sağlamak, kullanıcı tercihlerini hatırlamak ve site performansını ölçümlemek amacıyla yaygın olarak kullanılmaktadır.`,
      },
      {
        id: 'cerez-turleri',
        title: '2. Sitemizde Kullanılan Çerez Türleri',
        content: `Web sitemizde yalnızca sitenin temel işlevselliğini ve ziyaretçi güvenliğini sağlayan çerezler kullanılmaktadır:

1. **Zorunlu / Teknik Çerezler:** Sitenin güvenli şekilde yüklenmesi, gezinme fonksiyonları ve form gönderim güvenliği için zorunlu olan çerezlerdir. Bu çerezler kapatılamaz; kapatılması halinde web sitesinin temel fonksiyonları çalışmayabilir.
2. **İşlevsellik Çerezleri:** Kullanıcının tercihlerini (örneğin dil seçimi veya bildirim kapatma durumunu) hatırlayarak daha kişiselleştirilmiş bir deneyim sunulmasını sağlar.
3. **Performans ve Analitik Çerezler:** Sitemizin hangi sayfalarının daha çok ziyaret edildiğini, ziyaret sürelerini ve olası teknik hataları anonim olarak analiz etmemize yardımcı olan istatistiksel çerezlerdir. Bu veriler kimliğinizi doğrudan belirlemez.`,
      },
      {
        id: 'cerez-tablosu',
        title: '3. Web Sitemizde Yer Alan Başlıca Çerezler',
        content: `| Çerez Adı | Türü | Kullanım Amacı | Saklama Süresi |
| :--- | :--- | :--- | :--- |
| **cookie_consent** | İşlevsellik | Çerez onay tercihinizin kaydedilmesi | 1 Yıl |
| **__cf_bm / _cfuvid** | Güvenlik | Bot ve kötü niyetli saldırı koruması | Oturum / 30 Gün |
| **_ga / _gid** | Analitik | Sayfa görüntüleme ve anonim trafik istatistikleri | 24 Saat - 2 Yıl |`,
      },
      {
        id: 'cerez-kontrolu',
        title: '4. Çerez Tercihlerinizi Nasıl Yönetebilirsiniz?',
        content: `Tarayıcınızın ayarlarını değiştirerek çerez tercihlerinizi dilediğiniz zaman özelleştirebilir, mevcut çerezleri silebilir veya yeni çerezlerin kaydedilmesini engelleyebilirsiniz:

* **Google Chrome:** Ayarlar > Gizlilik ve Güvenlik > Üçüncü Taraf Çerezleri
* **Apple Safari:** Ayarlar > Safari > Gizlilik ve Güvenlik > Tüm Çerezleri Engelle
* **Mozilla Firefox:** Ayarlar > Gizlilik ve Güvenlik > Çerezler ve Site Verileri
* **Microsoft Edge:** Ayarlar > Çerezler ve Site İzinleri

Çerezleri devre dışı bırakmanız durumunda web sitemizin bazı dinamik özelliklerinin (örneğin teklif formu doğrulama) kısıtlanabileceğini hatırlatırız.`,
      },
    ],
  },
  {
    slug: 'kullanim-kosullari',
    shortTitle: 'Kullanım Koşulları',
    title: 'Web Sitesi Kullanım Koşulları ve Fikri Mülkiyet Bildirimi',
    badge: '5846 Sayılı FSEK Kapsamında Yasal Uyarı',
    description: 'celebiyonetim.com.tr alan adlı internet sitesini ziyaret eden tüm kullanıcılar için geçerli genel kullanım şartları, fikri mülkiyet hakları ve yasal sorumluluk sınırları.',
    lastUpdated: '10 Kasım 2026',
    effectiveDate: '10 Kasım 2026',
    sections: [
      {
        id: 'genel-hukumler',
        title: '1. Genel Hükümler ve Kabul',
        content: `Bu web sitesini (**celebiyonetim.com.tr**) ziyaret eden, sitede yer alan içerikleri inceleyen veya teklif/iletişim kanallarını kullanan tüm ziyaretçiler işbu Kullanım Koşulları'nı, Gizlilik Politikası'nı ve KVKK Aydınlatma Metni'ni peşinen kabul etmiş sayılır. Şartları kabul etmeyen kullanıcıların siteyi kullanmayı derhal sonlandırması gerekmektedir.`,
      },
      {
        id: 'fikri-mulkiyet',
        title: '2. Fikri ve Sınai Mülkiyet Hakları (Telif Uyarısı)',
        content: `* Web sitemizde yer alan tüm metinler, makaleler, rehberler, hizmet açıklamaları, grafikler, logolar, buton tasarımları, sayfa düzenleri ve yazılım kodları **5846 sayılı Fikir ve Sanat Eserleri Kanunu (FSEK)** ve Türk Ceza Kanunu kapsamında tescilli ve koruma altındadır.
* Çelebi Yönetim ve Temizlik'in yazılı ve açık ön izni olmaksızın; sitedeki hiçbir içerik kısmen veya tamamen kopyalanamaz, başka bir web sitesinde veya mecrada yayımlanamaz, tahrif edilemez, otomatik veri kazıma (scraping) yöntemleriyle çekilemez.
* İhlal tespit edildiğinde, noter tespiti yaptırılarak ilgili taraflar aleyhinde FSEK Madde 68, 70 uyarınca tazminat davaları ve cumhuriyet savcılıklarına cezai şikayetler gecikmeksizin işletilecektir.`,
      },
      {
        id: 'sorumluluk-sinirlari',
        title: '3. Bilgilendirme Niteliği ve Sorumluluk Sınırları',
        content: `* Sitemizde yayımlanan Kat Mülkiyeti Kanunu (KMK) rehberleri, aidat takibi makaleleri ve temizlik standartları genel bilgilendirme amacıyla hazırlanmıştır. Bu içerikler doğrudan bireysel bir hukuki mütalaa veya resmi vekalet ilişkisi teşkil etmez.
* Web sitesindeki bilgilerin güncel tutulması için azami özen gösterilmekle birlikte, mevzuat değişiklikleri veya teknik güncellemeler nedeniyle oluşabilecek olası gecikmelerden dolayı Şirketimiz hukuki veya cezai olarak sorumlu tutulamaz.`,
      },
      {
        id: 'guvenlik-ihlalleri',
        title: '4. Kullanıcı Güvenlik Yükümlülükleri',
        content: `Ziyaretçiler; web sitesinin altyapısına, sunucularına veya veritabanına zarar verecek, aşırı yük bindirecek, tersine mühendislik içerecek veya siber güvenlik açıklarını istismar edecek hiçbir eylemde bulunamaz. Bu tür eylemlerde bulunan şahıslar hakkında 5237 sayılı Türk Ceza Kanunu’nun bilişim suçlarına ilişkin hükümleri uyarınca adli işlem başlatılacaktır.`,
      },
      {
        id: 'yetkili-mahkeme',
        title: '5. Yetkili Hukuk ve Mahkemeler',
        content: `İşbu Kullanım Koşulları Türk Hukuku'na tabidir. Web sitesinin kullanımından veya işbu koşullardan doğabilecek her türlü ihtilaf ve uyuşmazlığın çözümünde **Adana Mahkemeleri ve İcra Daireleri** münhasıran yetkilidir.`,
      },
    ],
  },
  {
    slug: 'hizmet-ve-teklif-kosullari',
    shortTitle: 'Hizmet & Teklif Koşulları',
    title: 'Hizmet & Teklif Ön Bilgilendirme ve Genel Şartlar',
    badge: 'Mevzuata Uygunluk Garantisi',
    description: 'Site yönetimi ve kurumsal temizlik hizmetlerimize ilişkin teklif alma, sözleşme akdetme, personel güvencesi ve hizmet ifa standartlarımızı içeren genel şartlar.',
    lastUpdated: '10 Kasım 2026',
    effectiveDate: '10 Kasım 2026',
    sections: [
      {
        id: 'hizmet-kapsami',
        title: '1. Hizmetin Kapsamı ve Taraflar',
        content: `İşbu şartlar; **Çelebi Yönetim ve Temizlik** tarafından sunulan Profesyonel Site ve Apartman Yönetimi, Ortak Alan Temizliği, Sözleşmeli Ofis Temizliği, İnşaat/Tadilat Sonrası Temizlik ve Dış Cephe Cam Temizliği hizmetlerinden yararlanan veya teklif alan müşteriler (Apartman/Site Yönetimleri, Kat Malikleri Kurulları, Ticari İşletmeler ve Bireysel Müşteriler) için geçerlidir.`,
      },
      {
        id: 'yonetim-esaslari',
        title: '2. Site ve Apartman Yönetimi Esasları (KMK Uyumu)',
        content: `* Site ve apartman yönetimi hizmeti, 634 sayılı Kat Mülkiyeti Kanunu (KMK) hükümleri, bina yönetim planı ve Kat Malikleri Kurulu kararları doğrultusunda icra edilir.
* Yönetim devri için Kat Malikleri Kurulu’nun sayı ve arsa payı çoğunluğuyla karar alması ve yönetim sözleşmesinin imzalanması esastır.
* Şeffaf kasa ilkesi gereğince, toplanan tüm aidatlar apartman/site adına açılan resmi banka hesabında tutulur; gelir-gider dökümleri her ay panoda ve dijital portalda ilan edilir.`,
      },
      {
        id: 'temizlik-ve-sgk',
        title: '3. Temizlik Hizmetleri ve SGK Güvencesi',
        content: `* Çelebi bünyesinde görevlendirilen tüm temizlik personelleri yasal **SGK güvencesi** altındadır. Kesinlikle kayıtsız, kaçak veya taşeron işçi çalıştırılmaz.
* İş Sağlığı ve Güvenliği (İSG) kanunlarına uygunluk firmamızın sorumluluğunda olup, personellerin periyodik sağlık raporları, yüksekte çalışma sertifikaları ve hijyen eğitimleri eksiksizdir.
* Hizmet verilen mülklerde kullanılan tüm endüstriyel kimyasallar ve hijyen ekipmanları TSE / Sağlık Bakanlığı onaylıdır; mülk yüzeylerine zarar vermeyecek ph nötr solüsyonlar tercih edilir.`,
      },
      {
        id: 'teklif-ve-ucret',
        title: '4. Teklif Süreci, Ücretlendirme ve İptal Şartları',
        content: `* Web sitemiz veya telefon üzerinden oluşturulan teklifler, keşif ve taşınmaz incelemesi yapılana kadar ön bilgilendirme niteliğindedir. Kesin fiyatlandırma yerinde keşif veya daire/blok sayısı doğrulanarak yazılı sözleşmeye bağlanır.
* Sözleşmeli hizmetlerde taraflar, sözleşmede belirtilen bildirim süresi (genellikle 30 gün) öncesinde yazılı bildirimde bulunarak sözleşmeyi feshetme hakkına sahiptir.
* Hizmet kalitesinden kaynaklanan kusur veya eksiklik durumlarında, müşterimizin bildirimi üzerine 24 saat içerisinde ücretsiz telafi ve yerinde kontrol sağlanır.`,
      },
      {
        id: 'sikayet-kanallari',
        title: '5. Müşteri İletişim ve Şikayet Kanalları',
        content: `Hizmet süreçlerimize ilişkin her türlü öneri, talep veya şikayetlerinizi doğrudan aşağıdaki resmi kanallarımız üzerinden iletebilirsiniz:
* **Yönetim Destek Hattı:** 0 (535) 873 03 24
* **Temizlik Operasyon Hattı:** 0 (533) 597 59 81
* **Sabit Santral:** 0 (322) 235 15 88
* **Resmi E-Posta:** iletisim@celebiyonetim.com.tr
* **Fiziki Adres:** Mahfesığmaz Mah. 78033 Sk. No: 3 Zemin Kat, Çukurova / Adana`,
      },
    ],
  },
];

