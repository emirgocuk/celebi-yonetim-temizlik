/**
 * Çelebi Yönetim ve Temizlik - Telifsiz Stok Görsel Kütüphanesi & Akıllı Eşleştirici
 * Tüm görseller Unsplash License (Ticari ve gayriticari kullanıma %100 açık, telifsiz) kapsamındadır.
 * Ultra hızlı Imgix/Cloudflare CDN üzerinden optimize edilmiş WebP/JPG olarak servis edilir.
 */

export interface StockImageItem {
  id: string;
  url: string;
  thumbnail: string;
  title: string;
  category: string;
  keywords: string[];
}

export const STOCK_IMAGES_COLLECTION: Record<string, StockImageItem[]> = {
  // 1. Site ve Apartman Yönetimi / Rezidans
  site_yonetimi: [
    {
      id: 'sy-1',
      url: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=300&q=70',
      title: 'Modern Çok Katlı Rezidans & Site Kompleksi',
      category: 'Site Yönetimi',
      keywords: ['site', 'apartman', 'rezidans', 'kompleks', 'yönetim', 'blok']
    },
    {
      id: 'sy-2',
      url: 'https://images.unsplash.com/photo-1574362848149-11496d93a7c7?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1574362848149-11496d93a7c7?auto=format&fit=crop&w=300&q=70',
      title: 'Lüks Konut Projesi & Ortak Yaşam Alanları',
      category: 'Site Yönetimi',
      keywords: ['konut', 'proje', 'daire', 'havuz', 'peyzaj', 'bahçe']
    },
    {
      id: 'sy-3',
      url: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=300&q=70',
      title: 'Yeşil Alanlı ve Peyzajlı Modern Site',
      category: 'Site Yönetimi',
      keywords: ['peyzaj', 'bahçe', 'yeşil', 'tesis', 'otopark']
    },
    {
      id: 'sy-4',
      url: 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=300&q=70',
      title: 'Mülk ve Anahtar Teslimi Yönetim Masası',
      category: 'Site Yönetimi',
      keywords: ['anahtar', 'teslim', 'yönetici', 'malik', 'seçim']
    }
  ],

  // 2. Kat Mülkiyeti Kanunu (KMK), Aidat, Hukuk & İcra
  hukuk_icra: [
    {
      id: 'hk-1',
      url: 'https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=300&q=70',
      title: 'Hukuk Bürosu ve Yasal Mevzuat Masası',
      category: 'Hukuk & İcra',
      keywords: ['kmk', 'kanun', 'hukuk', 'icra', 'avukat', 'dava', 'ihtar']
    },
    {
      id: 'hk-2',
      url: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=300&q=70',
      title: 'Şeffaf Bütçe & Aidat Muhasebe Analizi',
      category: 'Hukuk & İcra',
      keywords: ['aidat', 'hesap', 'bütçe', 'mali', 'muhasebe', 'tahsilat', 'gecikme']
    },
    {
      id: 'hk-3',
      url: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=300&q=70',
      title: 'Resmi Sözleşme ve Noter Tasdik Süreci',
      category: 'Hukuk & İcra',
      keywords: ['sözleşme', 'noter', 'karar', 'defteri', 'genel kurul', 'imza']
    },
    {
      id: 'hk-4',
      url: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=300&q=70',
      title: 'Adalet Terazisi & Kat Mülkiyeti Hukuku',
      category: 'Hukuk & İcra',
      keywords: ['yasal', 'tazminat', 'mahkeme', 'uyuşmazlık', 'komşuluk']
    }
  ],

  // 3. Kurumsal Ofis ve İş Yeri Temizliği
  kurumsal_temizlik: [
    {
      id: 'kt-1',
      url: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=300&q=70',
      title: 'Tertemiz Modern Kurumsal Plaza Ofisi',
      category: 'Kurumsal Temizlik',
      keywords: ['ofis', 'kurumsal', 'plaza', 'şirket', 'iş yeri', 'hijyen']
    },
    {
      id: 'kt-2',
      url: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=300&q=70',
      title: 'Profesyonel Temizlik Ekipmanları ve Dezenfeksiyon',
      category: 'Kurumsal Temizlik',
      keywords: ['temizlik', 'malzeme', 'ekipman', 'dezenfeksiyon', 'sgk']
    },
    {
      id: 'kt-3',
      url: 'https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?auto=format&fit=crop&w=300&q=70',
      title: 'Pırıl Pırıl Yönetim ve Toplantı Salonu',
      category: 'Kurumsal Temizlik',
      keywords: ['toplantı', 'yönetim', 'salon', 'zemin', 'cilalama']
    }
  ],

  // 4. İnşaat ve Tadilat Sonrası Anahtar Teslim Temizlik
  insaat_temizlik: [
    {
      id: 'it-1',
      url: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=300&q=70',
      title: 'İnşaat Sonrası Kusursuz Temizlenmiş Yeni Daire',
      category: 'İnşaat Temizliği',
      keywords: ['inşaat', 'tadilat', 'sonrası', 'anahtar', 'teslim', 'sıfır']
    },
    {
      id: 'it-2',
      url: 'https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?auto=format&fit=crop&w=300&q=70',
      title: 'Derz ve Harç Kalıntılarından Arındırılmış Islak Hacim',
      category: 'İnşaat Temizliği',
      keywords: ['fayans', 'derz', 'boya', 'leke', 'harç', 'kireç']
    },
    {
      id: 'it-3',
      url: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=300&q=70',
      title: 'Taşınmaya Hazır Aydınlık İç Mekan',
      category: 'İnşaat Temizliği',
      keywords: ['taşınma', 'oturuma', 'hazır', 'cam', 'çerçeve']
    }
  ],

  // 5. Dış Cephe Cam Temizliği & Sepetli Vinç
  dis_cephe: [
    {
      id: 'dc-1',
      url: 'https://images.unsplash.com/photo-1506146332389-18140dc7b2fb?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1506146332389-18140dc7b2fb?auto=format&fit=crop&w=300&q=70',
      title: 'Gökdelen ve Yüksek Bina Cam Cephe Yansımaları',
      category: 'Dış Cephe',
      keywords: ['dış cephe', 'cam', 'plaza', 'yıkama', 'vinç', 'sepetli', 'isg']
    },
    {
      id: 'dc-2',
      url: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=300&q=70',
      title: 'Yüksek Plaza Mimarisi ve Dış Cephe',
      category: 'Dış Cephe',
      keywords: ['kompozit', 'yükseklik', 'iş güvenliği', 'dağcı', 'halat']
    }
  ],

  // 6. Apartman Merdiven ve Ortak Alan Temizliği
  merdiven_temizlik: [
    {
      id: 'mt-1',
      url: 'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=300&q=70',
      title: 'Pırıl Pırıl Mermer Apartman Giriş Holü',
      category: 'Apartman Temizliği',
      keywords: ['merdiven', 'giriş', 'hol', 'mermer', 'asansör', 'apartman']
    },
    {
      id: 'mt-2',
      url: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80',
      thumbnail: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=300&q=70',
      title: 'Aydınlık ve Hijyenik Ortak Koridor',
      category: 'Apartman Temizliği',
      keywords: ['koridor', 'parmaklık', 'korkuluk', 'haftalık', 'sözleşme']
    }
  ]
};

/**
 * Konu ve kategoriye en uygun telifsiz görseli akıllıca seçer.
 */
export function getRoyaltyFreeStockImage(topic: string = '', category: string = ''): StockImageItem {
  const t = (topic + ' ' + category).toLowerCase();

  // 1. Hukuk / Aidat / KMK / İcra
  if (t.includes('aidat') || t.includes('icra') || t.includes('kanun') || t.includes('kmk') || t.includes('hukuk') || t.includes('dava') || t.includes('borç') || t.includes('muhasebe') || t.includes('bütçe')) {
    const list = STOCK_IMAGES_COLLECTION.hukuk_icra;
    const idx = Math.abs(hashString(topic)) % list.length;
    return list[idx];
  }

  // 2. Dış Cephe / Cam / Vinç
  if (t.includes('dış cephe') || t.includes('cam') || t.includes('vinç') || t.includes('kompozit') || t.includes('yüksek')) {
    const list = STOCK_IMAGES_COLLECTION.dis_cephe;
    const idx = Math.abs(hashString(topic)) % list.length;
    return list[idx];
  }

  // 3. İnşaat / Tadilat Sonrası
  if (t.includes('inşaat') || t.includes('tadilat') || t.includes('harç') || t.includes('boya') || t.includes('anahtar teslim')) {
    const list = STOCK_IMAGES_COLLECTION.insaat_temizlik;
    const idx = Math.abs(hashString(topic)) % list.length;
    return list[idx];
  }

  // 4. Kurumsal Ofis / Plaza
  if (t.includes('ofis') || t.includes('kurumsal') || t.includes('plaza') || t.includes('şirket') || t.includes('iş yeri')) {
    const list = STOCK_IMAGES_COLLECTION.kurumsal_temizlik;
    const idx = Math.abs(hashString(topic)) % list.length;
    return list[idx];
  }

  // 5. Merdiven / Apartman Hijyeni
  if (t.includes('merdiven') || t.includes('asansör') || t.includes('ortak alan') || t.includes('apartman temizli')) {
    const list = STOCK_IMAGES_COLLECTION.merdiven_temizlik;
    const idx = Math.abs(hashString(topic)) % list.length;
    return list[idx];
  }

  // Varsayılan: Site Yönetimi Rezidans Görselleri
  const defaultList = STOCK_IMAGES_COLLECTION.site_yonetimi;
  const idx = Math.abs(hashString(topic)) % defaultList.length;
  return defaultList[idx];
}

/**
 * Tüm telifsiz görsel kataloğunu düz liste olarak döner (Admin seçici için).
 */
export function getAllStockImages(): StockImageItem[] {
  return Object.values(STOCK_IMAGES_COLLECTION).flat();
}

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return hash;
}

