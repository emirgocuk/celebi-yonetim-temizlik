export interface ServiceItem {
  id: string;
  slug: string;
  title: string;
  category: 'yonetim' | 'temizlik';
  badge: string;
  summary: string;
  description: string;
  highlights: string[];
  features: string[];
  idealFor: string;
}

export interface ReviewItem {
  id: string;
  author: string;
  role: string;
  buildingName: string;
  serviceType: string;
  comment: string;
  rating: number;
  date: string;
}

export interface QuoteRequest {
  id?: string;
  fullName: string;
  phone: string;
  email?: string;
  serviceType: 'site-yonetimi' | 'ofis-temizlik' | 'insaat-sonrasi' | 'dis-cephe' | 'diger';
  buildingUnits?: number;
  squareMeters?: number;
  cityDistrict?: string;
  message?: string;
  status?: 'yeni' | 'inceleniyor' | 'teklif-gonderildi' | 'tamamlandi';
  created?: string;
}

export interface CompanyMeta {
  name: string;
  tagline: string;
  description: string;
  phone: string;
  phoneFormatted: string;
  whatsapp: string;
  whatsappFormatted: string;
  email: string;
  address: string;
  workingHours: string;
  mapsEmbedUrl?: string;
  mapsQuery?: string;
}

