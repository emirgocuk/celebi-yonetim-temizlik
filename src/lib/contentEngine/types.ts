/**
 * Content Engine Types for Celebi Yonetim ve Temizlik
 */

export type GenerationMode = 'hybrid' | 'template' | 'llm';

export type ArticleCategory = 
  | 'Site Yönetimi'
  | 'Hukuk & KMK'
  | 'Aidat & Finans'
  | 'Kurumsal Temizlik'
  | 'İnşaat Temizliği'
  | 'Dış Cephe & Vinç'
  | 'Apartman Hijyeni';

export interface KeywordItem {
  id?: string;
  keyword: string;
  category: ArticleCategory;
  targetDistrict?: string;
  priority?: number;
  used?: boolean;
}

export interface ArticleDraft {
  baslik: string;
  slug: string;
  ozet: string; // Rich HTML body (p, h2, ul, li, img; NO h1)
  kategori: ArticleCategory;
  kategoriRenk: string;
  tarih: string;
  okumaSuresi: string;
  aktif: boolean;
  seoTitle: string;
  seoDescription: string;
  kapakGorsel?: string;
  kaynak?: string;
  kelimeSayisi?: number;
  h2Sayisi?: number;
  qualityPassed?: boolean;
}

export interface QualityReport {
  passed: boolean;
  wordCount: number;
  h2Count: number;
  hasCta: boolean;
  hasInternalLinks: boolean;
  properEnding: boolean;
  issues: string[];
}

export interface GenerationOptions {
  mode?: GenerationMode;
  keyword: string;
  category?: ArticleCategory;
  district?: string;
  openRouterApiKey?: string;
}

