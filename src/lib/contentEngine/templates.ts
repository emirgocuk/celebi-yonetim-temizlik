import type { ArticleCategory, ArticleDraft } from './types';

export interface TemplateDefinition {
  id: string;
  name: string;
  category: ArticleCategory;
  categoryColor: string;
  matchPatterns: string[];
  generate: (keyword: string, district?: string) => Omit<ArticleDraft, 'kelimeSayisi' | 'h2Sayisi' | 'qualityPassed'>;
}

function slugify(text: string): string {
  const trMap: Record<string, string> = {
    'ç': 'c', 'Ç': 'c', 'ğ': 'g', 'Ğ': 'g', 'ı': 'i', 'İ': 'i',
    'ö': 'o', 'Ö': 'o', 'ş': 's', 'Ş': 's', 'ü': 'u', 'Ü': 'u'
  };
  return text
    .split('')
    .map(c => trMap[c] || c)
    .join('')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

function getFormattedDate(): string {
  const now = new Date();
  const months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
  return `${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()}`;
}

export const NEWS_TEMPLATES: TemplateDefinition[] = [
  // 1. Şehir / İlçe + Profesyonel Site Yönetimi Rehberi
  {
    id: 'adana_site_yonetimi',
    name: 'Şehir/İlçe Profesyonel Site Yönetimi Rehberi',
    category: 'Site Yönetimi',
    categoryColor: 'blue',
    matchPatterns: ['site yönetimi', 'apartman yönetimi', 'yönetim şirketleri', 'fiyatları'],
    generate: (keyword, district = 'Çukurova') => {
      const title = `Adana ${district} Bölgesinde Profesyonel Site Yönetimi Nasıl Yapılır?`;
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Adana'da hızla artan çok katlı konut projeleri ve sitelerde huzurlu bir yaşam sürdürmenin en temel şartı, şeffaf ve kanuna uygun bir yönetim modelidir. Özellikle ${district} ve Seyhan bölgelerinde komşuluk ilişkilerinin zedelenmemesi adına profesyonel yönetim şirketlerine duyulan ihtiyaç her geçen gün artmaktadır.</p>

<h2>Kat Mülkiyeti Kanunu Çerçevesinde Profesyonel Yönetim</h2>
<p>Bireysel yöneticilikte yaşanan en büyük sorunlar; aidat tahsilatlarının aksaması, ortak alan arızalarının gecikmesi ve mali kayıtların denetlenememesidir. Profesyonel yönetim firmaları, 634 Sayılı Kat Mülkiyeti Kanunu (KMK) mevzuatına tam uyumlu işletme projeleri hazırlayarak her harcamanın yasal dayanağını belgeler.</p>
<ul>
  <li><strong>Şeffaf Muhasebe:</strong> Her ay düzenli yayınlanan gelir-gider tabloları ve banka dökümleri.</li>
  <li><strong>Düzenli Denetim:</strong> Denetim kuruluna sunulan resmi evrak ve karar defteri kayıtları.</li>
  <li><strong>Hukuki Danışmanlık:</strong> Aidat uyuşmazlıklarında uzman avukatlar aracılığıyla arabuluculuk ve takip.</li>
</ul>

<h2>Ortak Alanların Bakımı ve Güvenlik Standartları</h2>
<p>Asansörlerin periyodik kırmızı/yeşil etiket kontrolleri, yangın hidrofor sistemlerinin testi ve hidrofor bakımları uzmanlık gerektirir. ${district} genelinde hizmet veren Çelebi Yönetim, anlaşmalı akredite servislerle binaların teknik aksamlarını güvence altına almaktadır.</p>

<h2>Adana İklimine Uygun Peyzaj ve Havuz İdaresi</h2>
<p>Çukurova'nın sıcak yaz aylarında site havuzlarının kimyasal dengesi ve bahçe sulama sistemlerinin düzeni özel dikkat ister. Sağlık Bakanlığı onaylı havuz ilaçlamaları ve su analizleri sakinlerin sağlığı için periyodik olarak raporlanır.</p>

<h2>Çelebi Yönetim ile Huzurlu ve Şeffaf Yaşam Alanları</h2>
<p>Apartman veya sitenizde aidat karmaşasından ve teknik arıza stresinden kurtulmak istiyorsanız, Çelebi Yönetim ve Temizlik olarak Adana Mahfesığmaz merkez ofisimizden tüm ilçelere kurumsal yönetim çözümleri sunuyoruz. Ücretsiz keşif ve işletme projesi analizi için bize <strong>0 (322) 235 15 88</strong> veya WhatsApp <strong>0 (535) 873 03 24</strong> hattımızdan hemen ulaşabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Site Yönetimi',
        kategoriRenk: 'blue',
        tarih: getFormattedDate(),
        okumaSuresi: '4 dk okuma',
        aktif: true,
        seoTitle: `Adana ${district} Profesyonel Site Yönetimi | Çelebi`,
        seoDescription: `Adana ${district} ve Seyhan bölgesinde Kat Mülkiyeti Kanununa uygun şeffaf site yönetimi, aidat tahsilatı ve teknik bakım rehberi.`,
        kapakGorsel: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Yönetim Hukuk & Operasyon Masası'
      };
    }
  },

  // 2. KMK ve Yönetici Yasal Sorumlulukları
  {
    id: 'kmk_yonetici_rehberi',
    name: 'Kat Mülkiyeti Kanunu ve Yönetici Sorumlulukları',
    category: 'Hukuk & KMK',
    categoryColor: 'purple',
    matchPatterns: ['kmk', 'kat mülkiyeti', 'yönetici seçimi', 'kanun', 'mevzuat'],
    generate: (keyword) => {
      const title = 'Kat Mülkiyeti Kanununa Göre Yöneticinin Hukuki ve Cezai Sorumlulukları';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>634 Sayılı Kat Mülkiyeti Kanunu (KMK), apartman ve site yöneticilerine geniş yetkiler verirken aynı zamanda çok ciddi hukuki ve cezai yükümlülükler yükler. Yöneticinin basiretli bir vekil gibi davranma borcu, ihmal durumunda şahsi mal varlığıyla tazminat sorumluluğunu doğurabilir.</p>

<h2>KMK Madde 35 Kapsamında Yöneticinin Temel Görevleri</h2>
<p>Yönetici, genel kurulda alınan kararların uygulayıcısıdır. Kanunen zorunlu olan defterlerin noter tasdiki, ortak avansların toplanması ve sigorta işlemlerinin takibi yöneticinin asli vazifesidir.</p>
<ul>
  <li><strong>Karar ve İşletme Defteri:</strong> Her yıl noterden kapanış ve açılış tasdiklerinin süresinde yapılması.</li>
  <li><strong>Banka Hesabı Açılması:</strong> Site adına özel vadesiz hesap açılması; paraların şahsi hesaplarda tutulmasının yasak olması.</li>
  <li><strong>Tebligat ve Bilgilendirme:</strong> İşletme projesinin tüm bağımsız bölüm maliklerine taahhütlü mektupla veya imza karşılığı tebliğ edilmesi.</li>
</ul>

<h2>İşletme Projesinin Kesinleşmesi ve İtiraz Süresi</h2>
<p>Yönetici tarafından hazırlanan işletme projesine kat malikleri tebliğden itibaren yedi gün içinde itiraz edebilir. İtiraz edilmezse proje kesinleşir ve İcra ve İflas Kanunu'nun 68. maddesi anlamında ilam niteliğinde belge sayılır.</p>

<h2>Yöneticinin Hesap Verme Yükümlülüğü ve İbra Süreci</h2>
<p>Yönetici, olağan kat malikleri kurulu toplantısında ayrıntılı bir hesap raporu sunmak zorundadır. Kurul tarafından ibra edilmeyen yönetici hakkında denetçiler veya kat malikleri tarafından Sulh Hukuk Mahkemesi'nde dava açılabilir.</p>

<h2>Çelebi Yönetim ile Yasal Riskleri Sıfırlayın</h2>
<p>Bireysel olarak yöneticilik yaparken karşılaşılan cezai ve hukuki riskleri üstlenmek yerine, işi profesyonel ellere devredin. Çelebi Yönetim ve Temizlik olarak Adana genelinde tüm siteleri hukuki güvence altına alıyoruz. Danışma ve bilgi için <strong>0 (322) 235 15 88</strong> numaramızdan uzmanlarımıza bağlanabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Hukuk & KMK',
        kategoriRenk: 'purple',
        tarih: getFormattedDate(),
        okumaSuresi: '5 dk okuma',
        aktif: true,
        seoTitle: 'KMK Yönetici Sorumlulukları ve Hukuki Rehber | Çelebi',
        seoDescription: 'Kat Mülkiyeti Kanununa göre apartman yöneticisinin hukuki görevleri, işletme projesi tebliği ve ibra süreci hakkında uzman rehberi.',
        kapakGorsel: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Yönetim Hukuk Danışmanlığı'
      };
    }
  },

  // 3. Aidat Tahsilatı, Gecikme Tazminatı ve İcra Takibi
  {
    id: 'aidat_tahsilati_icra',
    name: 'Aidat Tahsilatı ve Yasal İcra Takibi Rehberi',
    category: 'Aidat & Finans',
    categoryColor: 'emerald',
    matchPatterns: ['aidat', 'tahsilat', 'icra', 'gecikme tazminatı', 'ödemeyen'],
    generate: (keyword) => {
      const title = 'Apartman Aidatını Ödemeyen Maliklere Karşı Yasal Haklar ve İcra Süreci';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Toplu yaşam alanlarında aidatların zamanında ödenmemesi; temizlik personelinin maaşının aksamasından elektrik ve suyun kesilmesine kadar tüm site sakinlerini mağdur eden büyük bir sorundur. KMK bu konuda yönetime çok güçlü yasal yaptırım araçları tanımıştır.</p>

<h2>KMK Madde 20 Uyarınca Aylık %5 Gecikme Tazminatı</h2>
<p>Kanun gereğince ortak gider payını gününde ödemeyen kat maliki veya kiracı, ödemede geciktiği günler için aylık yüzde beş (yıllık %60) gecikme tazminatı ödemekle yükümlüdür. Bu oran genel kurulda düşürülemez veya yok sayılamaz.</p>
<ul>
  <li><strong>İcra Takibi Başlatma:</strong> Borcunu ödemeyen sakin aleyhine ilamsız icra takibi (Örnek No: 7) başlatılabilir.</li>
  <li><strong>İtirazın İptali Davası:</strong> Borçlunun haksız itirazı durumunda Sulh Hukuk Mahkemesinde dava açılarak %20 icra inkar tazminatına hükmedilir.</li>
  <li><strong>Kanuni İpotek Hakkı:</strong> Borç ödenmezse yöneticinin talebiyle borçlunun dairesi üzerine ipotek konulabilir.</li>
</ul>

<h2>Kiracı ile Ev Sahibinin Müteselsil Sorumluluğu</h2>
<p>Kira sözleşmesinde aidatın kiracı tarafından ödeneceği kararlaştırılmış olsa dahi, ana gayrimenkulün sahibi ev sahibi de kanunen bu borçtan müteselsilen sorumludur. Yönetim, ödenmeyen aidatı doğrudan mülk sahibinden icra yoluyla tahsil edebilir.</p>

<h2>Banka Onaylı Otomatik Tahsilatın Önemi</h2>
<p>Elden para toplama dönemi kapanmıştır. Tüm tahsilatların bina adına açılmış özel banka hesapları veya sanal POS / kredi kartı entegrasyonlarıyla yapılması, olası suistimalleri tamamen engeller.</p>

<h2>Çelebi Yönetim ile Sıfır Aidat Kaybı</h2>
<p>Çelebi Yönetim olarak geliştirdiğimiz şeffaf takip otomasyonu ve bünyemizdeki hukuk müşavirliği sayesinde aidat tahsilat oranını %98'in üzerine çıkarıyoruz. Komşularınızla yüz göz olmadan kurumsal tahsilat için bize <strong>0 (535) 873 03 24</strong> WhatsApp hattımızdan ulaşabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Aidat & Finans',
        kategoriRenk: 'emerald',
        tarih: getFormattedDate(),
        okumaSuresi: '4 dk okuma',
        aktif: true,
        seoTitle: 'Aidat Tahsilatı ve İcra Takibi Yasal Rehberi | Çelebi',
        seoDescription: 'Apartman ve site aidatını ödemeyenlere karşı KMK Madde 20 gecikme tazminatı, icra takibi ve kanuni ipotek hakları hakkında detaylı rehber.',
        kapakGorsel: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Yönetim Finans & Hukuk Birimi'
      };
    }
  },

  // 4. Kurumsal Ofis ve İş Yeri Hijyen Standartları
  {
    id: 'kurumsal_ofis_temizligi',
    name: 'Kurumsal Ofis ve Plaza Hijyen Protokolleri',
    category: 'Kurumsal Temizlik',
    categoryColor: 'cyan',
    matchPatterns: ['ofis', 'kurumsal temizlik', 'iş yeri', 'plaza', 'şirket temizliği'],
    generate: (keyword, district = 'Çukurova') => {
      const title = `Adana ${district} Bölgesinde Kurumsal Ofis Temizliğinde Dikkat Edilecekler`;
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>İş yerlerinde hijyen, çalışan sağlığı ve kurumsal prestijin ayrılmaz bir parçasıdır. Gün boyu onlarca kişinin kullandığı çalışma masaları, klavyeler ve ortak mutfak alanları düzenli dezenfekte edilmediğinde salgın hastalıkların ve verim düşüklüğünün kaynağı haline gelir.</p>

<h2>Çapraz Bulaşmayı Önleyen Renk Kodlu Bez Sistemi</h2>
<p>Kurumsal temizlikte en kritik kural, tuvalet temizliğinde kullanılan ekipmanların asla ofis masaları veya mutfakta kullanılmamasıdır. Uluslararası temizlik protokollerine göre renk ayrımı zorunludur:</p>
<ul>
  <li><strong>Kırmızı Bezler:</strong> Yüksek riskli alanlar (klozet, pisuvar).</li>
  <li><strong>Sarı Bezler:</strong> Lavabo, fayans ve ayna yüzeyleri.</li>
  <li><strong>Mavi Bezler:</strong> Çalışma masaları, dolaplar ve toplantı salonları.</li>
  <li><strong>Yeşil Bezler:</strong> Ofis mutfağı ve yemekhane yüzeyleri.</li>
</ul>

<h2>Mesai Saatleri Dışında Sözleşmeli Temizlik Konforu</h2>
<p>Ofis personelinizin dikkati dağılmadan, akşam mesai bitimi (18:30 sonrası) veya sabah mesai öncesi yapılan periyodik temizlik, çalışma ortamının her sabah ferah ve hazır olmasını sağlar.</p>

<h2>SGK ve İş Güvenliği Belgeli Kadro Güvencesi</h2>
<p>Ofisinize aldığınız temizlik personelinin sigortasız olması, olası bir iş kazasında işletme sahibine yüzbinlerce liralık cezai sorumluluk getirir. Kurumsal firmalarla çalışmak bu riski sıfıra indirir.</p>

<h2>Çelebi Temizlik ile Ofisinizde Kusursuz Prestij</h2>
<p>Çelebi Yönetim ve Temizlik olarak Ziyapaşa, Gazipaşa ve Çukurova genelindeki plaza ve iş merkezlerine sözleşmeli, SGK garantili temizlik hizmeti sunuyoruz. Ücretsiz keşif ve demo temizlik için bize <strong>0 (533) 597 59 81</strong> numaramızdan ulaşabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Kurumsal Temizlik',
        kategoriRenk: 'cyan',
        tarih: getFormattedDate(),
        okumaSuresi: '3 dk okuma',
        aktif: true,
        seoTitle: `Adana ${district} Kurumsal Ofis Temizliği | Çelebi`,
        seoDescription: `Adana ${district} ve Seyhan bölgesinde plazalar, hukuk büroları ve şirketler için renk kodlu, SGK garantili kurumsal ofis temizliği rehberi.`,
        kapakGorsel: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Temizlik Hijyen Denetim Kurulu'
      };
    }
  },

  // 5. İnşaat ve Tadilat Sonrası Anahtar Teslim Temizlik
  {
    id: 'insaat_sonrasi_temizlik',
    name: 'İnşaat ve Tadilat Sonrası Temizlik Rehberi',
    category: 'İnşaat Temizliği',
    categoryColor: 'amber',
    matchPatterns: ['inşaat', 'tadilat', 'harç', 'boya', 'anahtar teslim'],
    generate: (keyword) => {
      const title = 'İnşaat ve Tadilat Sonrası Temizlikte Çiziksiz ve Kusursuz Sonuç İçin 5 Kural';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Yeni bir eve taşınırken veya kapsamlı bir tadilat sonrasında karşılaşılan en zorlu aşama inşaat kalıntılarının temizliğidir. Alçı, derz dolgusu, boya sıçramaları ve pencere emniyet bantları doğru kimyasal ve ekipman kullanılmazsa kalıcı hasarlara yol açabilir.</p>

<h2>Pencereleri ve Doğramaları Çizmeden Temizleme</h2>
<p>Camlarda kurumuş harç ve boya lekelerini raspa ile kazırken yanlış açı veya kalitesiz bıçak kullanımı camın geri dönülmez şekilde çizilmesine neden olur. Çözüm, özel harç yumuşatıcı solüsyonlar ve profesyonel cam jiletleridir.</p>
<ul>
  <li><strong>Güneşte Yanmış Koruyucu Bantlar:</strong> PVC pencerelerde güneşte eriyen bantlar buharlı makineler ve özel yapışkan sökücülerle yüzeye zarar vermeden çıkarılır.</li>
  <li><strong>Derz Sisi Temizliği:</strong> Granit ve seramik yüzeylerdeki beyaz derz buğusu asit bazlı olmayan derz temizleyicilerle arındırılır.</li>
  <li><strong>Parke Koruma:</strong> Ahşap zeminlerde su basması yapılmaz; nem kontrollü endüstriyel vakum kullanılır.</li>
</ul>

<h2>Banyo ve Mutfak Islak Hacim Dezenfeksiyonu</h2>
<p>Fayans aralarına sinen inşaat tozları standart paspasla temizlenemez. Yüksek devirli zemin cilalama ve yıkama makineleri ile gözeneklerdeki tüm toz vakumlanır.</p>

<h2>Anahtar Teslim Taşınmaya Hazır Teslimat</h2>
<p>Profesyonel inşaat sonrası temizlikte amaç, ev sahibinin tek bir toz dahi görmeden doğrudan eşyalarını yerleştirebilmesidir. Dolap içleri, prizler ve kapı pervazları titizlikle elden geçirilir.</p>

<h2>Çelebi Temizlik ile Sıfır Hata Garantisi</h2>
<p>Adana Seyhan ve Çukurova genelinde müteahhit teslimleri ve lüks konut tadilatları sonrası anahtar teslim temizlik sunuyoruz. Detaylı bilgi ve randevu için temizlik operasyon hattımız: <strong>0 (533) 597 59 81</strong>.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'İnşaat Temizliği',
        kategoriRenk: 'amber',
        tarih: getFormattedDate(),
        okumaSuresi: '4 dk okuma',
        aktif: true,
        seoTitle: 'İnşaat ve Tadilat Sonrası Temizlik Rehberi | Çelebi',
        seoDescription: 'İnşaat sonrası derz, harç, boya ve pencere bantlarının çizilmeden temizlenmesi için profesyonel ipuçları ve anahtar teslim hizmet rehberi.',
        kapakGorsel: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi İnşaat Temizliği Operasyon Şefliği'
      };
    }
  },

  // 6. Dış Cephe Cam Temizliği ve Vinçli Yıkama Güvenliği
  {
    id: 'dis_cephe_cam_guvenligi',
    name: 'Yüksek Katlı Binalarda Dış Cephe Temizliği',
    category: 'Dış Cephe & Vinç',
    categoryColor: 'blue',
    matchPatterns: ['dış cephe', 'cam temizliği', 'vinç', 'sepetli vinç', 'plaza camı'],
    generate: (keyword) => {
      const title = 'Yüksek Katlı Binalarda Dış Cephe Cam Temizliği ve İSG Güvenlik Kuralları';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Modern plazaların ve rezidansların dış görünümünü belirleyen en önemli unsur tertemiz cam ve kompozit cephelerdir. Ancak yüksekte çalışma kategorisine giren dış cephe temizliği, en yüksek iş güvenliği standartlarını gerektiren son derece uzman bir alandır.</p>

<h2>İş Sağlığı ve Güvenliği (İSG) Zorunlulukları</h2>
<p>Yüksekte çalışacak personelin yüksekte çalışma sertifikasına, mesleki yeterlilik belgesine ve geçerli periyodik sağlık raporuna sahip olması yasal bir mecburiyettir.</p>
<ul>
  <li><strong>Sepetli Vinç Operasyonu:</strong> Kullanılan vinçlerin periyodik makine mühendisleri odası kontrol belgeleri tam olmalıdır.</li>
  <li><strong>Çift Emniyet Kemeri:</strong> Personelin emniyet halatı ve paraşüt tipi kemer donanımı eksiksiz kullanılmalıdır.</li>
  <li><strong>Zemin Güvenlik Çemberi:</strong> Yıkama esnasında bina çevresi şeritle kapatılarak yaya trafiği korunmalıdır.</li>
</ul>

<h2>Adana Sıcağında Cam Yanıklarını Önleyen Arıtılmış Su</h2>
<p>Güneş altında deterjanlı suyun kuruması camda kireç yanıklarına yol açar. Saf su arıtma (Revers Osmosis) filtreleri ile mineralden arındırılmış su kullanılarak lekesiz parlaklık elde edilir.</p>

<h2>Kompozit Panellerin Ömrünü Uzatan Bakım</h2>
<p>Asitli kimyasallar kompozit panellerin rengini soldurur. Yalnızca pH nötr dış cephe şampuanları kullanılarak binanın dış yalıtım kaplaması korunur.</p>

<h2>Çelebi Yönetim ile Güvenli ve Parlak Cepheler</h2>
<p>Çelebi Yönetim ve Temizlik olarak Adana genelinde plaza ve rezidanslara sözleşmeli dış cephe cam temizliği hizmeti sunuyoruz. Detaylı keşif için bize <strong>0 (322) 235 15 88</strong> veya <strong>0 (533) 597 59 81</strong> hatlarımızdan ulaşabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Dış Cephe & Vinç',
        kategoriRenk: 'blue',
        tarih: getFormattedDate(),
        okumaSuresi: '4 dk okuma',
        aktif: true,
        seoTitle: 'Dış Cephe Cam Temizliği ve Vinçli Yıkama Rehberi | Çelebi',
        seoDescription: 'Yüksek katlı plazalarda İSG kurallarına uygun sepetli vinçle dış cephe cam temizliği, saf su teknolojisi ve kompozit bakım rehberi.',
        kapakGorsel: 'https://images.unsplash.com/photo-1541888946425-d0fbb186156a?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi İSG ve Yüksekte Çalışma Departmanı'
      };
    }
  },

  // 7. Apartman Merdiven ve Ortak Alan Temizliği
  {
    id: 'apartman_merdiven_temizligi',
    name: 'Apartman Merdiven Temizliği Sözleşmesi',
    category: 'Apartman Hijyeni',
    categoryColor: 'emerald',
    matchPatterns: ['merdiven', 'apartman temizliği', 'ortak alan', 'merdiven yıkama'],
    generate: (keyword) => {
      const title = 'Apartman Merdiven Temizliğinde Sigortasız Eleman Çalıştırmanın Ağır Riskleri';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Apartman yöneticilerinin sıklıkla düştüğü en büyük yanılgı, haftada bir gelen merdiven temizlikçisinin sigorta gerektirmediği düşüncesidir. Oysa Sosyal Güvenlik Kurumu (SGK) mevzuatına göre düzenli temizlik yapan herkes kısmi süreli çalışan statüsündedir.</p>

<h2>Olası Bir Düşme Kazasında Yöneticinin Hukuki Mesuliyeti</h2>
<p>Merdivenden kayarak düşen sigortasız bir çalışanın tedavi masrafları ve açacağı iş kazası tazminat davaları, bina sakinleri ve yöneticiyi doğrudan yüzbinlerce liralık borçla karşı karşıya bırakabilir.</p>
<ul>
  <li><strong>Fatura ve Kurumsal Sözleşme:</strong> Kurumsal temizlik şirketi ile çalışıldığında tüm SGK ve iş hukuku sorumluluğu şirkete aittir.</li>
  <li><strong>Malzeme Masrafı Yok:</strong> Deterjan, paspas, çöp poşeti ve koku gidericiler firma tarafından temin edilir.</li>
  <li><strong>Yedek Personel Güvencesi:</strong> Personel rahatsızlansa dahi yerine hemen ikame eleman yönlendirilir, bina asla temizliksiz kalmaz.</li>
</ul>

<h2>Ortak Alan Hijyen Protokolü (Asansör, Tırabzan, Posta Kutusu)</h2>
<p>Sadece basamakların silinmesi temizlik değildir. Asansör aynaları ve kabini, kapı kolları, yangın merdivenleri ve tırabzanlar dezenfektanlarla hijyenik hale getirilmelidir.</p>

<h2>Çelebi Temizlik ile Güvenli ve Tertemiz Merdivenler</h2>
<p>Adana Çukurova, Seyhan ve Yüreğir genelinde yüzlerce binaya kurumsal sözleşmeli merdiven temizliği hizmeti sağlıyoruz. Binanızı güvenceye almak için temizlik hattımız: <strong>0 (533) 597 59 81</strong>.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Apartman Hijyeni',
        kategoriRenk: 'emerald',
        tarih: getFormattedDate(),
        okumaSuresi: '3 dk okuma',
        aktif: true,
        seoTitle: 'Apartman Merdiven Temizliği ve SGK Güvencesi | Çelebi',
        seoDescription: 'Apartman merdiven temizliğinde sigortasız işçi çalıştırma riskleri, kurumsal sözleşme avantajları ve ortak alan hijyen standartları.',
        kapakGorsel: 'https://images.unsplash.com/photo-1527515637462-cff94eecc1ac?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Apartman Hizmetleri Masası'
      };
    }
  },

  // 8. Site Bütçesi ve İşletme Projesi Hazırlama
  {
    id: 'site_butcesi_hesaplama',
    name: 'Site İşletme Projesi ve Bütçe Hazırlama',
    category: 'Aidat & Finans',
    categoryColor: 'purple',
    matchPatterns: ['işletme projesi', 'site bütçesi', 'bütçe hesaplama', 'avans'],
    generate: (keyword) => {
      const title = 'Kat Malikleri Kurulu Öncesi Kusursuz Site İşletme Projesi Nasıl Hazırlanır?';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>İşletme projesi, bir sitenin bir yıl boyunca yapacağı tüm harcamaların ve toplanacak aidatların anayasası niteliğindedir. Hukuki prosedürlere uygun hazırlanmayan bir işletme projesi, genel kurulda iptal edilebilir veya aidat tahsilatlarını tamamen tıkayabilir.</p>

<h2>İşletme Projesinde Mutlaka Yer Alması Gereken Kalemler</h2>
<p>KMK Madde 37 uyarınca işletme projesinde tahmini gelir ve giderler ile her bağımsız bölümün hissesine düşecek miktar açıkça gösterilmelidir.</p>
<ul>
  <li><strong>Personel Giderleri:</strong> Kapıcı, güvenlik, temizlik personeli maaş, kıdem tazminatı fonu ve SGK primleri.</li>
  <li><strong>Ortak Tesis Faturaları:</strong> Asansör elektriği, ortak hidrofor ve çevre aydınlatma maliyetleri.</li>
  <li><strong>Bakım Sözleşmeleri:</strong> Asansör, jeneratör, havuz ve yangın tüpü periyodik kontrol sözleşmeleri.</li>
  <li><strong>Beklenmedik Gider Fonu (%10):</strong> Olası acil su patlağı veya çatı akması gibi durumlar için ayrılan yedek akçe.</li>
</ul>

<h2>Arsa Payına Göre ve Eşit Dağıtılacak Giderler</h2>
<p>Kapıcı ve güvenlik gibi işletme giderleri kural olarak tüm dairelere eşit paylaştırılırken; sigorta, çatı veya ana yapı onarım giderleri arsa payı oranında paylaştırılır.</p>

<h2>Çelebi Yönetim ile Matematiksel ve Şeffaf Bütçeleme</h2>
<p>Çelebi Yönetim ve Temizlik olarak Adana'daki binalarınız için enflasyona ve yasal mevzuata tam uyumlu işletme projeleri hazırlıyoruz. Profesyonel bütçe desteği için bize <strong>0 (322) 235 15 88</strong> numaramızdan ulaşabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Aidat & Finans',
        kategoriRenk: 'purple',
        tarih: getFormattedDate(),
        okumaSuresi: '4 dk okuma',
        aktif: true,
        seoTitle: 'Site İşletme Projesi ve Aidat Hesaplama Rehberi | Çelebi',
        seoDescription: 'KMK Madde 37 kapsamında apartman ve site işletme projesi hazırlama, gider dağılımı ve yedek akçe hesaplama rehberi.',
        kapakGorsel: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Yönetim Mali Denetim Kurulu'
      };
    }
  },

  // 9. Apartman & Site Genel Kurul Düzenleme Adımları
  {
    id: 'genel_kurul_isletme_projesi',
    name: 'Apartman Genel Kurulu ve Karar Alma Süreci',
    category: 'Hukuk & KMK',
    categoryColor: 'blue',
    matchPatterns: ['genel kurul', 'karar defteri', 'kat malikleri kurulu', 'divan'],
    generate: (keyword) => {
      const title = 'Apartman ve Site Genel Kurul Toplantısı Nasıl Yapılır? Yasal Çağrı ve Karar Nisapları';
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Kat malikleri kurulu toplantıları, sitenin bir yıllık geleceğini belirleyen en üst karar organıdır. Ancak toplantı çağrısının usulüne uygun yapılmaması, genel kurulda alınan tüm kararların mahkemece iptal edilmesine (yok hükmünde sayılmasına) yol açabilir.</p>

<h2>Genel Kurul Çağrı ve Tebligat Şartları</h2>
<p>Toplantı çağrısının en az 15 gün önceden tüm maliklere imza karşılığı veya iadeli taahhütlü mektupla ulaştırılması gerekir. İlk toplantıda yeter sayı sağlanamazsa, ikinci toplantının günü ve saati ilk çağrıda belirtilmelidir.</p>
<ul>
  <li><strong>Toplantı Yeter Sayısı (Nisap):</strong> İlk toplantıda sayı ve arsa payı çoğunluğu aranır. İkinci toplantıda ise katılanların çoğunluğu ile karar alınabilir.</li>
  <li><strong>Vekalet Sınırı:</strong> Bir kişi, oy sayısının en fazla yüzde beşini (%5) temsil edebilir. 40 ve daha az daireli binalarda bir kişi en fazla 2 kişiye vekalet edebilir.</li>
  <li><strong>Karar Defteri Yazımı:</strong> Alınan kararlar toplantı divanı ve maliklerce imzalanmalı, muhalif kalanların şerhleri deftere işlenmelidir.</li>
</ul>

<h2>Çelebi Yönetim ile İptal Edilemez Genel Kurullar</h2>
<p>Çelebi Yönetim olarak divan başkanlığından hazirun cetveline, tebligatlardan noter onaylarına kadar tüm genel kurul sürecinizi sıfır hukuki hatayla yürütüyoruz. Destek için: <strong>0 (322) 235 15 88</strong>.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Hukuk & KMK',
        kategoriRenk: 'blue',
        tarih: getFormattedDate(),
        okumaSuresi: '4 dk okuma',
        aktif: true,
        seoTitle: 'Apartman Genel Kurulu ve Karar Nisapları Rehberi | Çelebi',
        seoDescription: 'Kat Malikleri Kurulu toplantı çağrısı, vekalet sınırları, karar yeter sayıları ve karar defteri noter onay prosedürleri.',
        kapakGorsel: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Genel Kurul Yönetim Birimi'
      };
    }
  },

  // 10. Adana Temizlik Şirketi Seçerken Dikkat Edilecekler
  {
    id: 'temizlik_sirketi_secimi',
    name: 'Profesyonel Temizlik Şirketi Seçim Kriterleri',
    category: 'Kurumsal Temizlik',
    categoryColor: 'cyan',
    matchPatterns: ['en iyi temizlik', 'temizlik şirketi', 'güvenilir temizlik', 'temizlik tavsiye'],
    generate: (keyword, district = 'Adana') => {
      const title = `Adana'da Profesyonel Temizlik Şirketi Seçerken Nelere Dikkat Edilmelidir?`;
      const slug = `${slugify(title)}-${Date.now().toString().slice(-4)}`;
      const body = `
<p>Ev, ofis veya bina temizliği hizmeti alırken doğru firmayı seçmek hem hijyen hem de güvenlik açısından hayati önem taşır. Piyasada kayıt dışı çalışan pek çok kişi ve merdiven altı oluşum bulunurken, kurumsal bir temizlik şirketi seçerken dikkat edilmesi gereken temel kriterler vardır.</p>

<h2>Kurumsal Temizlik Firmasının 4 Temel Özelliği</h2>
<ul>
  <li><strong>1. SGK Güvencesi ve Sabıka Kaydı:</strong> Evinize veya ofisinize giren tüm personelin adli sicil kaydı kontrol edilmiş ve SGK'sı tam yatırılmış olmalıdır.</li>
  <li><strong>2. Profesyonel Ekipman ve Kimyasal:</strong> Market tipi deterjanlar yerine Sağlık Bakanlığı onaylı, yüzeylere zarar vermeyen endüstriyel kimyasallar kullanılmalıdır.</li>
  <li><strong>3. Sözleşme ve Memnuniyet Garantisi:</strong> Yapılan işin kapsamı yazılı sözleşmeye bağlanmalı, beğenilmeyen alanlar telafi edilmelidir.</li>
  <li><strong>4. Ulaşılabilir Sabit Hat ve Fiziksel Ofis:</strong> Yalnızca cep telefonuyla çalışan değil, Adana'da fiziksel ofisi ve sabit santral hattı olan firmalar tercih edilmelidir.</li>
</ul>

<h2>Çelebi Temizlik ile Güvenli ve Kusursuz Temizlik</h2>
<p>Adana Mahfesığmaz merkezli Çelebi Yönetim ve Temizlik olarak kurumsal ofis, inşaat sonrası, dış cephe ve ev temizliğinde uzman kadromuzla yanınızdayız. Bilgi ve randevu için bize <strong>0 (533) 597 59 81</strong> numaramızdan ulaşabilirsiniz.</p>
`;
      return {
        baslik: title,
        slug,
        ozet: body.trim(),
        kategori: 'Kurumsal Temizlik',
        kategoriRenk: 'cyan',
        tarih: getFormattedDate(),
        okumaSuresi: '3 dk okuma',
        aktif: true,
        seoTitle: `Adana Temizlik Şirketi Seçim Rehberi | Çelebi`,
        seoDescription: `Adana'da kurumsal temizlik şirketi seçerken dikkat edilmesi gereken SGK, ekipman, İSG ve memnuniyet güvencesi kriterleri.`,
        kapakGorsel: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80',
        kaynak: 'Çelebi Müşteri Güvenliği Kurulu'
      };
    }
  }
];

export function findTemplateForKeyword(keyword: string): TemplateDefinition {
  const lower = keyword.toLowerCase();
  for (const t of NEWS_TEMPLATES) {
    if (t.matchPatterns.some(p => lower.includes(p))) {
      return t;
    }
  }
  // Default to first template (adana_site_yonetimi)
  return NEWS_TEMPLATES[0];
}

