export interface ArticleItem {
  slug: string;
  title: string;
  category: string;
  tag: string;
  tagColor: string;
  readTime: string;
  publishDate: string;
  isoDate: string;
  summary: string;
  image: string;
  author: {
    name: string;
    role: string;
  };
  keyTakeaways: string[];
  content: {
    lead: string;
    sections: {
      heading: string;
      paragraphs: string[];
      listItems?: string[];
    }[];
  };
}

export const ARTICLES_DATA: ArticleItem[] = [
  {
    slug: 'kat-mulkiyeti-kanunu-site-yonetimi',
    title: 'Kat Mülkiyeti Kanunu Kapsamında Profesyonel Apartman ve Site Yönetimi Nasıl Yürütülür?',
    category: 'Site Yönetimi',
    tag: 'KMK Hukuki Mevzuat',
    tagColor: 'bg-sky-100 text-sky-800 border-sky-200',
    readTime: '4 dk okuma',
    publishDate: '12 Ekim 2026',
    isoDate: '2026-10-12',
    summary: '634 sayılı Kat Mülkiyeti Kanunu uyarınca yönetici seçimi, karar defteri noter tasdiki, işletme projesi tebliği ve hukuki sorumlulukların eksiksiz rehberi.',
    image: '/assets/images/hero-building.jpg',
    author: {
      name: 'Av. Kemal Erdem & Çelebi Hukuk Ekibi',
      role: 'Gayrimenkul & KMK Danışmanı',
    },
    keyTakeaways: [
      '8 ve üzeri bağımsız bölümü olan binalarda yönetici atanması kanunen zorunludur.',
      'Yıllık tahmini işletme projesi tüm kat maliklerine noter veya taahhütlü tebliğ edilmelidir.',
      'Karar defterinin her takvim yılı başında noter tarafından kapanış ve açılış tasdiki şarttır.',
      'Profesyonel yönetim tüzel kişiliğiyle komşular arası şahsi husumetlerin önüne geçilir.',
    ],
    content: {
      lead: 'Türkiye’de toplu yaşam alanlarının hızla büyümesiyle birlikte, apartman ve site yönetimleri amatör komşuluk inisiyatifinden çıkarak Kat Mülkiyeti Kanunu (KMK) çerçevesinde katı hukuki disiplin gerektiren bir uzmanlık haline gelmiştir.',
      sections: [
        {
          heading: '1. Yönetici Atanması ve Kat Malikleri Kurulu Süreci',
          paragraphs: [
            '634 sayılı Kat Mülkiyeti Kanunu’nun 34. maddesine göre, sekiz veya daha fazla bağımsız bölümü olan binalarda yönetici seçimi yapılması yasal bir zorunluluktur. Kat malikleri kurulu, yılda en az bir defa yönetim planında gösterilen zamanda toplanır.',
            'Yönetici, kat maliklerinin hem sayı hem de arsa payı bakımından çoğunluğuyla seçilir. İlk toplantıda yeterli çoğunluk sağlanamazsa, ikinci toplantıda salt çoğunlukla karar verilebilir. Ancak profesyonel bir tüzel kişilikle sözleşme yapılması durumunda sözleşme şartları kurul divanınca karara bağlanır.',
          ],
        },
        {
          heading: '2. İşletme Projesinin Hazırlanması ve Tebliğ Zorunluluğu',
          paragraphs: [
            'Yöneticinin en kritik görevlerinden biri KMK 37. maddesi uyarınca işletme projesinin hazırlanmasıdır. Bu proje, sitenin bir yıllık tahmini gelir ve giderlerini, her bağımsız bölümün payına düşen aidat miktarını ve olası bakım-onarım fonlarını kapsar.',
            'Hazırlanan proje, tüm kat maliklerine veya bağımsız bölümden fiilen yararlananlara imza karşılığı ya da taahhütlü mektupla tebliğ edilmek zorundadır. Yasal 7 günlük itiraz süresi içinde itiraz edilmeyen proje kesinleşir ve doğrudan icra takibine esas teşkil eden belge hüviyeti kazanır.',
          ],
          listItems: [
            'Personel SGK, kıdem tazminatı karşılığı ve maaş bütçesi',
            'Asansör, hidrofor, yangın sistemi ve jeneratör periyodik bakım payları',
            'Ortak alan aydınlatma, su ve ısınma genel giderleri',
            'Beklenmedik acil onarım ve yenileme avans fonu',
          ],
        },
        {
          heading: '3. Çelebi Yönetim Güvencesiyle Yasal Risklerin Sıfırlanması',
          paragraphs: [
            'Amatör yöneticiler, vergi dairesi cezaları, SGK işyeri bildirgelerindeki gecikmeler veya karar defterinin noter onayının unutulması sebebiyle şahsi mal varlıklarıyla sorumlu tutulabilmektedir.',
            'Çelebi Yönetim olarak, tüm bu yasal takvimi lisanslı yönetim yazılımlarımız, banka onaylı özel hesap yapımız ve kadrolu hukuk ekibimizle üstlenerek kat maliklerinin huzurunu ve mülk değerini güvence altına alıyoruz.',
          ],
        },
      ],
    },
  },
  {
    slug: 'aidat-tahsilati-icra-takibi',
    title: 'Aidat Tahsilatı, Gecikme Tazminatı ve Hukuki İlamsız İcra Takip Süreçleri',
    category: 'Hukuk & İcra',
    tag: 'İcra & Finans',
    tagColor: 'bg-red-100 text-red-800 border-red-200',
    readTime: '4 dk okuma',
    publishDate: '18 Ekim 2026',
    isoDate: '2026-10-18',
    summary: 'Ödenmeyen aidatlarda aylık %5 gecikme faizi uygulaması, noter ihtarı ve avukat destekli ilamsız icra takip adımları.',
    image: '/assets/images/hero-building.jpg',
    author: {
      name: 'Çelebi İcra & Finans Departmanı',
      role: 'Tahsilat Koordinatörlüğü',
    },
    keyTakeaways: [
      'Gününde ödenmeyen aidat borçları için KMK md. 20 gereği aylık %5 yasal gecikme tazminatı işler.',
      'Borçluya noter ihtarnamesi çekildikten sonra İcra Müdürlükleri nezdinde ilamsız icra takibi başlatılır.',
      'Borca itiraz durumunda Sulh Hukuk Mahkemesi’nde %20 icra inkar tazminatlı dava açılır.',
      'Banka entegrasyonlu online tahsilat sistemimizle tahsilat başarı oranı %98.4’e ulaşmaktadır.',
    ],
    content: {
      lead: 'Apartman ve sitelerde en sık yaşanan huzursuzluk, bir kısım komşuların aidat ödemelerini aksatması ve bu sebeple ortak asansör, güvenlik, yakıt veya temizlik ödemelerinin kilitlenmesidir.',
      sections: [
        {
          heading: '1. Yasal Gecikme Tazminatı: Aylık %5 Oran',
          paragraphs: [
            'Kat Mülkiyeti Kanunu’nun 20. maddesi amir hükümdür: Ortak gider ve avans payını zamanında ödemeyen kat maliki, gecikilen günler için aylık yüzde beş (%5) hesabıyla gecikme tazminatı ödemekle yükümlüdür.',
            'Bu faiz cezai bir şart olmayıp kanundan doğan zorunlu bir haktır. Yönetim kurulunun bu faizi keyfi olarak affetme veya silme yetkisi dahi bulunmamaktadır.',
          ],
        },
        {
          heading: '2. İlamsız İcra Takibi Süreci Nasıl İşler?',
          paragraphs: [
            'Çelebi Yönetim otomasyonu, vade günü geçen borçlar için önce SMS ve e-posta ile dostane hatırlatma gönderir. 15 gün içinde ödenmeyen bakiyeler için noterden yasal ödeme ihtarı çekilir.',
            'İhtara rağmen ödeme yapılmaması halinde, kesinleşmiş işletme projesine dayanılarak İcra Müdürlüğü nezdinde Örnek No: 7 ilamsız icra takibi başlatılır. Tebligat borçluya ulaştıktan sonra 7 gün içinde itiraz edilmezse takip kesinleşir ve banka hesapları ile taşınmaz haciz işlemleri tatbik edilir.',
          ],
        },
      ],
    },
  },
  {
    slug: 'kurumsal-ofis-temizligi-hijyen-protokolleri',
    title: 'Kurumsal Ofis ve İş Yeri Temizliğinde Hijyen Protokolleri ve Çapraz Bulaşma Önleme',
    category: 'Kurumsal Temizlik',
    tag: 'Kurumsal Hijyen',
    tagColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    readTime: '3 dk okuma',
    publishDate: '24 Ekim 2026',
    isoDate: '2026-10-24',
    summary: 'Uluslararası renk kodlu mikrofiber bez protokolü, mesai saatleri dışı operasyon ve ofis ekipmanı güvenliği.',
    image: '/assets/images/office-cleaning.jpg',
    author: {
      name: 'Murat Doğan',
      role: 'Endüstriyel Temizlik Operasyon Müdürü',
    },
    keyTakeaways: [
      'Renk kodlama sistemi (Kırmızı/Sarı/Mavi/Yeşil) ile tuvalet bakterilerinin masalara taşınması engellenir.',
      'Teknolojik ekipmanlar alkol bazlı hassas solüsyonlar ve antistatik mikrofiberlerle silinir.',
      'Sözleşmeli tüm personelimiz SGK güvenceli ve adli sicil kayıtlıdır.',
      'Sabah 06:30 - 08:30 veya akşam 18:30 sonrası mesai aksatmayan çalışma modeli uygulanır.',
    ],
    content: {
      lead: 'Modern kurumsal şirketlerde temizlik, yalnızca görünür tozun alınması değil; çalışanların hastalanmasını önleyen ve marka prestijini yükselten epidemiyolojik bir hijyen zinciridir.',
      sections: [
        {
          heading: '1. Çapraz Bulaşmayı Önleyen 4 Renk Kuralı',
          paragraphs: [
            'Amatör temizlikte en büyük tehlike, lavabo veya tuvalette kullanılan bezin çalışma masalarında ya da mutfak tezgahında kullanılmasıdır. Çelebi Temizlik kadrosu uluslararası renk koduna harfiyen uyar:',
          ],
          listItems: [
            '🔴 Kırmızı Bez: Klozet, pisuvar ve yüksek riskli ıslak hacimler',
            '🟡 Sarı Bez: Lavabo aynası, fayans yüzeyler ve armatürler',
            '🔵 Mavi Bez: Ofis masaları, sandalyeler, dosya dolapları ve monitörler',
            '🟢 Yeşil Bez: Personel mutfağı, su sebilleri ve kahve alanı yüzeyleri',
          ],
        },
        {
          heading: '2. Sözleşmeli ve Güvenlik Denetimli Personel Standartları',
          paragraphs: [
            'Ofislerde gizli ticari evraklar, bilgisayarlar ve kıymetli eşyalar bulunur. Çelebi bünyesindeki tüm temizlik uzmanları güvenlik soruşturmasından geçmiş, adli sicil kayıtları temiz ve SGK kadrosuyla çalışan sabit personellerdir.',
          ],
        },
      ],
    },
  },
  {
    slug: 'insaat-sonrasi-anahtar-teslim-temizlik',
    title: 'İnşaat ve Tadilat Sonrası Anahtar Teslim Daire Temizliği Rehberi',
    category: 'İnşaat Temizliği',
    tag: 'Anahtar Teslim',
    tagColor: 'bg-amber-100 text-amber-800 border-amber-200',
    readTime: '3 dk okuma',
    publishDate: '28 Ekim 2026',
    isoDate: '2026-10-28',
    summary: 'Mermer ve parkeleri çizmeden derz dolgu, harç, boya lekesi ve PVC bantlarının endüstriyel arındırılması.',
    image: '/assets/images/construction-clean.jpg',
    author: {
      name: 'Kemal Aksoy',
      role: 'Şantiye & Proje Temizlik Şefi',
    },
    keyTakeaways: [
      'Asidik kimyasallar mermer ve granitleri matlaştırır; pH nötr özel harç sökücüler kullanılmalıdır.',
      'Güneşte beklemiş PVC pencere bantları buharlı termal sökücülerle yüzeye sıfır hasarla çıkarılır.',
      'Endüstriyel ıslak-kuru vakum makineleri havadaki ince alçı tozunu hapseder.',
      'Daireler aynı gün içinde oturuma ve taşınmaya hazır anahtar teslim edilir.',
    ],
    content: {
      lead: 'Yeni tamamlanan inşaat projeleri ya da ev tadilatları sonrası kalan kireç, derz dolgusu ve yapışkan bantlar sıradan ev temizliği ürünleriyle temizlenemez; yanlış kimyasal kullanımı mermer ve laminat parkelerde telafisi imkansız çiziklere yol açar.',
      sections: [
        {
          heading: '1. Yüzey Korumalı Endüstriyel Kimyasal Seçimi',
          paragraphs: [
            'İnşaat temizliğinde en sık yapılan hata tuz ruhu veya sert asitlerin mermere sürülmesidir. Bu durum cilayı anında yakar. Çelebi Temizlik uzmanları yüzey analizine göre özel pH dengeli harç yumuşatıcılar ve mermer koruyucu solüsyonlar kullanır.',
          ],
        },
        {
          heading: '2. Buhar ve Vakum Entegrasyonu',
          paragraphs: [
            'Buharlı dezenfeksiyon makinelerimiz, petek aralarına, süpürgelik arkalarına ve cam fitillerine yapışan inşaat tozunu yüksek ısıyla çözerek endüstriyel vakumla çeker. İş tesliminde yönetici onay tutanağı imzalatılır.',
          ],
        },
      ],
    },
  },
  {
    slug: 'dis-cephe-cam-temizligi-is-guvenligi',
    title: 'Dış Cephe Cam Temizliğinde Sepetli Vinç ve İş Güvenliği (İSG) Standartları',
    category: 'Dış Cephe & Vinç',
    tag: 'İş Güvenliği & Vinç',
    tagColor: 'bg-cyan-100 text-cyan-800 border-cyan-200',
    readTime: '4 dk okuma',
    publishDate: '02 Kasım 2026',
    isoDate: '2026-11-02',
    summary: 'Yüksek binalarda 6331 sayılı İSG mevzuatı, saf su (osmos) lekesiz yıkama teknolojisi ve 3. şahıs sigorta güvencesi.',
    image: '/assets/images/window-cleaning.jpg',
    author: {
      name: 'Engin Varol',
      role: 'A Sınıfı İSG Uzmanı & Vinç Operatörü',
    },
    keyTakeaways: [
      'Yüksekte çalışma belgeli ve periyodik sağlık muayeneli uzman kadro.',
      'Sepetli vinç ve asma iskelelerde çift emniyet halatı ve paraşüt tipi emniyet kemeri zorunludur.',
      'Osmos teknolojisiyle üretilen saf su, camda leke bırakmaz ve toz tutma süresini 3 kat geciktirir.',
      'Operasyon süresince 3. Şahıs Mali Mesuliyet Sigortası tam kapsamlı geçerlidir.',
    ],
    content: {
      lead: 'Rezidans, plaza ve iş merkezlerinin mimari vitrini olan dış cephe camlarının temizliği, yüksek risk sınıfında yer alan ve en ufak bir emniyet zafiyetine tahammülü olmayan kritik bir operasyondur.',
      sections: [
        {
          heading: '1. 6331 Sayılı Kanuna Tam Uyum ve Sertifikasyon',
          paragraphs: [
            'Dış cephe cam temizliğinde çalışacak personelin Yüksekte Çalışma Sertifikasına (IRATA veya ulusal akrediteli) ve güncel yüksekte çalışabilir sağlık raporuna sahip olması zorunludur. Çelebi ekipleri operasyon sahasını güvenlik şeritleriyle çevirir ve zemin yaya emniyetini sağlar.',
          ],
        },
        {
          heading: '2. Osmos Teknolojisiyle Mineralden Arındırılmış Saf Su',
          paragraphs: [
            'Şebeke suyundaki kireç ve klor camda beyaz lekeler bırakır. Firmamızın kullandığı deiyonize osmos filtrasyon sistemi suyu saflaştırır. Saf su kuruduğunda camda hiçbir leke bırakmaz ve statik elektriklenmeyi önleyerek cephenin aylarca temiz kalmasını sağlar.',
          ],
        },
      ],
    },
  },
  {
    slug: 'apartman-merdiven-temizligi-sozlesmesi',
    title: 'Apartman Merdiven Temizliği Sözleşmesi ve Yöneticinin Hukuki Sorumluluğu',
    category: 'Apartman Hijyeni',
    tag: 'Yasal Güvence',
    tagColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
    readTime: '3 dk okuma',
    publishDate: '05 Kasım 2026',
    isoDate: '2026-11-05',
    summary: 'Sigortasız gündelikçi çalıştırmanın idari para cezaları ve kurumsal sözleşmeyle risk devrinin yasal detayları.',
    image: '/assets/images/residential-hall.jpg',
    author: {
      name: 'Çelebi Yönetim Kurulu',
      role: 'Müşteri Hizmetleri & Operasyon',
    },
    keyTakeaways: [
      'Düzenli gelen sigortasız temizlikçiler Yargıtay kararlarına göre hizmet akdine tabidir.',
      'Olası bir merdiven düşme kazasında tüm kat malikleri yüzbinlerce liralık tazminatla karşılaşır.',
      'Kurumsal temizlik faturasıyla tüm cezai ve hukuki sorumluluk firmamıza devredilir.',
      'Sabit gün ve saatte yönetici onaylı imza föyüyle düzenli takip sağlanır.',
    ],
    content: {
      lead: 'Apartmanlarda merdiven temizliği için kayıtsız eleman çağırmak küçük bir tasarruf gibi görünse de, Sosyal Güvenlik Kurumu (SGK) denetimlerinde veya iş kazalarında bina yönetimini yüz binlerce liralık idari para cezalarıyla karşı karşıya getirmektedir.',
      sections: [
        {
          heading: '1. Yargıtay İçtihatları ve Sigorta Zorunluluğu',
          paragraphs: [
            'Yargıtay Hukuk Genel Kurulu’nun yerleşik kararlarına göre, haftada bir gün dahi olsa düzenli olarak apartman merdiveni silen kişiler ile bina yönetimi arasında belirsiz süreli kısmi süreli iş sözleşmesi kurulmuş sayılır. Bu kişinin sigortasız çalıştırılması durumunda geriye dönük primler, gecikme zamları ve idari para cezaları kat maliklerine rücu edilir.',
          ],
        },
        {
          heading: '2. Çelebi Temizlik Sözleşmesiyle Sıfır Risk Garantisi',
          paragraphs: [
            'Firmamızla yapılan haftalık apartman temizliği sözleşmesinde çalışan tüm personeller şirketimizin bordrolu çalışanıdır. Yöneticinin hiçbir işverenlik sorumluluğu kalmaz. Her hafta asansörler, tırabzanlar, posta kutuları ve kapı girişleri onaylı formla temizlenir.',
          ],
        },
      ],
    },
  },
];

