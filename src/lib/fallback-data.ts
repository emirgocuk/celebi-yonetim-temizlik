import type { CompanyMeta, ReviewItem, ServiceItem } from './types';

export const COMPANY_INFO: CompanyMeta = {
  name: 'Çelebi Yönetim ve Temizlik',
  tagline: 'Profesyonel Tesis Yönetimi & Endüstriyel Temizlik Standartları',
  description: 'Toplu yaşam alanlarında şeffaf, kanuna uygun site yönetimi ve SGK garantili uzman kadroyla A+ hijyen sağlayan temizlik çözümleri.',
  phone: '+90 555 000 00 00',
  phoneFormatted: '0 (555) 000 00 00',
  whatsapp: '905550000000',
  whatsappFormatted: '+90 555 000 00 00',
  email: 'iletisim@celebiyonetim.com',
  address: 'Merkez Mah. Atatürk Cad. No: 42/B, Çelebi Plaza Kat: 3, Türkiye',
  workingHours: 'Pazartesi - Cumartesi: 08:30 - 19:00 (Acil Destek: 7/24)',
  mapsEmbedUrl: 'https://maps.google.com/maps?q=Atat%C3%BCrk%20Caddesi%20No:42,%20Istanbul,%20Turkey&t=&z=15&ie=UTF8&iwloc=&output=embed',
  mapsQuery: 'Atatürk Caddesi No:42, Istanbul, Turkey',
};

export const SERVICES_DATA: ServiceItem[] = [
  {
    id: 'site-yonetimi',
    slug: 'site-ve-apartman-yonetimi',
    title: 'Site ve Apartman Yönetimi',
    category: 'yonetim',
    badge: 'Mevzuata %100 Uyumlu',
    summary: 'Kat Mülkiyeti Kanunu çerçevesinde hukuki, idari ve mali süreçlerin bağımsız, şeffaf ve profesyonel idaresi.',
    description: 'Komşuluk ilişkilerini zedelemeden, aidat gecikmelerini minimize eden; asansör, yangın, hidrofor ve çevre düzenlemesi gibi teknik kontrolleri düzenli yapan kurumsal yönetim hizmeti.',
    highlights: [
      'Online Şeffaf Kasa & Aidat Takibi (Mobil Bildirimli)',
      'Kat Mülkiyeti Kanunu (KMK) Uzmanı Hukuki Süreç Yönetimi',
      'Asansör, Jenaratör ve Yangın Tesisatı Periyodik Bakım Denetimi',
      'Yıllık İşletme Projesi ve Tahmini Bütçe Hazırlama',
    ],
    features: [
      'Banka entegrasyonlu online tahsilat',
      'Her ay panoya asılan onaylı gelir-gider tablosu',
      'Bina görevlisi SGK ve bordro işlemleri takibi',
      '7/24 acil tesisat ve asansör arıza koordinasyonu',
    ],
    idealFor: 'Apartmanlar, çok bloklu konut siteleri, iş merkezleri ve ticari plazalar.',
  },
  {
    id: 'ofis-ve-ticari-temizlik',
    slug: 'ofis-ve-ticari-temizlik',
    title: 'Ofis ve Ticari Alan Temizliği',
    category: 'temizlik',
    badge: 'SGK Belgeli & Sigortalı Personel',
    summary: 'Çalışma alanlarınızın verimliliğini artıran, kurumsal imajınızı güçlendiren periyodik ve sözleşmeli ofis hijyeni.',
    description: 'Sabah mesai öncesi veya akşam mesai sonrası seçenekleriyle; çalışma masaları, teknolojik ekipmanlar, ortak alanlar ve ıslak zeminler için profesyonel kimyasal ve mikrofiber bez kodlama sistemiyle derinlemesine temizlik.',
    highlights: [
      'Mesai Saatlerinizi Aksatmayan Esnek Çalışma Planı',
      'Renk Kodlu Çapraz Bulaşma Önleyici Mikrofiber Ekipman',
      'Sözleşmeli, SGK’lı ve Güvenlik Soruşturmalı Kadro',
      'Aylık Süpervizör Denetim & Memnuniyet Raporu',
    ],
    features: [
      'Zemin cilalama ve halı yıkama opsiyonu',
      'Sarf malzeme (havlu, sabun, deterjan) takip ve tedariki',
      'Kurumsal faturalandırma ve şeffaf sözleşme',
    ],
    idealFor: 'Şirket genel merkezleri, plazalar, klinikler, showroomlar ve ortak çalışma alanları.',
  },
  {
    id: 'insaat-sonrasi-temizlik',
    slug: 'insaat-ve-tadilat-sonrasi-temizlik',
    title: 'İnşaat ve Tadilat Sonrası Temizlik',
    category: 'temizlik',
    badge: 'Ağır Kir & Moloz Çözümleri',
    summary: 'Derz dolgu, boya artıkları, harç ve silikon lekelerinin yüzeylere zarar vermeden endüstriyel makinelerle arındırılması.',
    description: 'Yeni teslim edilecek konutlar ve yenilenen ticari mekanlar için taşınmaya hazır anahtar teslim temizlik. Camlardaki koruma bantları, zeminlerdeki kireç ve kimyasal atıklar profesyonel buharlı ve vakumlu makinelerle temizlenir.',
    highlights: [
      'Çizilmeyi Önleyen Özel Kimyasal ve Kazıyıcı Protokolü',
      'Endüstriyel Islak/Kuru Zemin Vakum Makineleri',
      'Aynı Gün İçinde Taşınmaya Hazır Teslimat Garantisi',
      'Cam, PVC ve Doğrama Bantlarının Kalıntısız Sökümü',
    ],
    features: [
      'Tüm odalar, mutfak dolap içi/dışı ve banyolar',
      'Balkon, petek araları ve süpürgelik detay hijyeni',
      'İş teslim tutanağı ve müşteri onay formu',
    ],
    idealFor: 'Müteahhitler, mimarlık ofisleri, yeni ev alanlar ve kapsamlı tadilat yaptıranlar.',
  },
  {
    id: 'dis-cephe-ve-cam-temizligi',
    slug: 'dis-cephe-ve-cam-temizligi',
    title: 'Dış Cephe ve Yüksek Cam Temizliği',
    category: 'temizlik',
    badge: 'İSG Belgeli & Sepetli Vinçli',
    summary: 'Plaza ve binaların dış cephe cam, kompozit ve alüminyum yüzeylerinin mevzuata uygun iş güvenliğiyle temizlenmesi.',
    description: 'Hava koşullarının ve egzoz dumanının oluşturduğu is ve kireç tabakasını özel saf su teknolojisi (deiyonize su) ve sepetli platformlarla temizleyerek uzun süreli parlaklık sağlıyoruz.',
    highlights: [
      'Yüksekte Çalışma Sertifikalı (IRATA / İSG) Uzman Ekip',
      'Leke Bırakmayan Saf Su (Osmos) Yıkama Sistemi',
      'Cephe Malzemesine (Kompozit/Granit) Özel Nötr Kimyasal',
      'Üçüncü Şahıs Mali Mesuliyet Sigortası Kapsamında',
    ],
    features: [
      'Geniş cepheler için sepetli vinç ve iskele kurulumu',
      'Yılda 2 veya 4 periyotluk kurumsal bakım sözleşmesi',
    ],
    idealFor: 'Rezidanslar, kamu binaları, hastaneler, alışveriş merkezleri ve oteller.',
  },
  {
    id: 'merdiven-ve-ortak-alan',
    slug: 'merdiven-ve-ortak-alan-temizligi',
    title: 'Apartman Merdiven ve Ortak Alan Temizliği',
    category: 'temizlik',
    badge: 'Düzenli Haftalık Takip',
    summary: 'Apartman sakinleri arasında sıra tartışmasına son veren, haftalık düzenli merdiven, asansör ve bina giriş hijyeni.',
    description: 'Belirlenen gün ve saatte gelen sabit personelimiz; merdiven korkulukları, asansör kabini, posta kutuları, bina giriş kapısı ve sığınak alanlarını kaliteli parfümlü dezenfektanlarla temizler.',
    highlights: [
      'Haftada 1 veya 2 Gün Sabit Saat Uygulaması',
      'Asansör İçi Aynalar ve Kumanda Paneli Dezenfeksiyonu',
      'Bina Girişi Camları ve Giriş Alanı Paspas Yıkama',
      'Çöp Kovaları ve Merdiven Korkulukları Detaylı Silim',
    ],
    features: [
      'Yönetici onaylı ziyaret imza çizelgesi panosu',
      'Kullanılan kimyasalların kokusuz ve antialerjik olması',
    ],
    idealFor: 'Kapıcısı olmayan apartmanlar ve butik siteler.',
  },
];

export const STATS_DATA = [
  { value: '140+', label: 'Yönetilen Bağımsız Bölüm', detail: 'Aktif site ve apartman dairesi' },
  { value: '%98', label: 'Zamanında Aidat Tahsilatı', detail: 'Online takip ve hukuki disiplinle' },
  { value: '25+', label: 'SGK Güvenceli Personel', detail: 'Eğitimli ve denetlenen kadro' },
  { value: '24/7', label: 'Acil Arıza Müdahalesi', detail: 'Asansör, elektrik ve su tesisatı' },
];

export const REVIEWS_DATA: ReviewItem[] = [
  {
    id: 'rev-1',
    author: 'Mehmet Yılmaz',
    role: 'Site Denetim Kurulu Başkanı',
    buildingName: 'Defne Konakları (48 Daire)',
    serviceType: 'Site Yönetimi & Ortak Alan Hijyeni',
    comment: 'Eski yönetim döneminde aidatını ödemeyenler yüzünden yakıt alamıyorduk. Çelebi Yönetim devraldıktan sonra 2 ay içinde tüm geçmiş borçlar tahsil edildi. Her ay kuruşu kuruşuna rapor kapımıza asılıyor.',
    rating: 5,
    date: '2026-09-14',
  },
  {
    id: 'rev-2',
    author: 'Av. Elif Karadağ',
    role: 'Yönetici Ortak',
    buildingName: 'Karadağ Hukuk Bürosu',
    serviceType: 'Sözleşmeli Ofis Temizliği',
    comment: 'Hukuk büromuz için en önemli konu gizlilik ve güvendi. Gönderdikleri personel son derece saygılı, evrak düzenine dokunmadan masaları tertemiz yapıyor. Çapraz bez kodlama sistemleri gerçekten profesyonel.',
    rating: 5,
    date: '2026-10-02',
  },
  {
    id: 'rev-3',
    author: 'Serkan Öztürk',
    role: 'Proje Müdürü',
    buildingName: 'Vadi Panorama Evleri',
    serviceType: 'İnşaat Sonrası Daire Temizliği',
    comment: '36 dairelik projemizin tesliminde anlaştık. Derz aralarındaki kireci ve pencere bantlarını camlara tek bir çizik atmadan söktüler. Müşterilerimize daireleri gururla teslim ettik.',
    rating: 5,
    date: '2026-10-21',
  },
];

export const FAQS_DATA = [
  {
    question: 'Site yönetimi hizmeti neleri kapsıyor?',
    answer: 'Kat Mülkiyeti Kanunu uyarınca işletme projesinin hazırlanması, banka entegrasyonlu aidat tahsilatı, asansör/yangın/hidrofor bakımlarının yetkili firmalarca yapılması, bina görevlisi bordrolama işlemleri ve borcunu ödemeyenlere karşı hukuki icra takibini eksiksiz kapsar.',
  },
  {
    question: 'Temizlik personeliniz sigortalı mı?',
    answer: 'Evet. Çalışanlarımızın tamamı Çelebi bünyesinde SGK’lı ve iş sağlığı güvenliği eğitimlerini tamamlamış kadrolu personeldir. Taşeron veya kayıtsız eleman kesinlikle çalıştırılmaz.',
  },
  {
    question: 'Temizlik malzemelerini kim temin ediyor?',
    answer: 'İnşaat sonrası ve dış cephe temizliklerinde tüm endüstriyel makineler ve profesyonel kimyasallar firmamıza aittir. Ofis ve merdiven temizliklerinde ise tercihinize göre malzemeli veya malzemesiz sözleşme yapılabilir.',
  },
  {
    question: 'Fiyat teklifi nasıl belirleniyor?',
    answer: 'Apartman/site yönetiminde bağımsız bölüm sayısı ve tesisin ortak alan büyüklüğüne göre; temizlikte ise metrekare, periyot sıklığı ve mekanın mevcut kirlilik durumuna göre net, gizli masrafsız bir teklif sunulur.',
  },
];

