import PocketBase from 'pocketbase';
import type { ArticleDraft, KeywordItem } from './types';

function getPbClient(customUrl?: string): PocketBase {
  const url = customUrl || 
              (typeof process !== 'undefined' ? process.env?.PUBLIC_POCKETBASE_URL : '') || 
              'http://2.27.101.128';
  return new PocketBase(url);
}

/**
 * Saves generated article to PocketBase
 */
export async function saveArticleToPocketBase(
  draft: ArticleDraft,
  authToken?: string,
  pbUrl?: string
): Promise<{ success: boolean; id?: string; error?: string }> {
  try {
    const pb = getPbClient(pbUrl);
    if (authToken) {
      pb.authStore.save(authToken, null);
    }

    const payload = {
      baslik: draft.baslik,
      slug: draft.slug,
      ozet: draft.ozet,
      kategori: draft.kategori,
      kategoriRenk: draft.kategoriRenk || 'blue',
      tarih: draft.tarih,
      okumaSuresi: draft.okumaSuresi || '4 dk okuma',
      aktif: draft.aktif !== undefined ? draft.aktif : true,
      seoTitle: draft.seoTitle,
      seoDescription: draft.seoDescription,
      kapakGorsel: draft.kapakGorsel || '',
      kaynak: draft.kaynak || 'Çelebi Yönetim & Temizlik',
      views: 0
    };

    const record = await pb.collection('yazilar').create(payload);
    return { success: true, id: record.id };
  } catch (err: any) {
    return { success: false, error: err?.message || String(err) };
  }
}

/**
 * Retrieves the next unused keyword from seo_keywords
 */
export async function getNextSeoKeyword(
  pbUrl?: string
): Promise<KeywordItem | null> {
  try {
    const pb = getPbClient(pbUrl);
    const records = await pb.collection('seo_keywords').getList<KeywordItem>(1, 1, {
      filter: 'used = false',
      sort: '-priority,-created'
    });

    if (records.items && records.items.length > 0) {
      return records.items[0];
    }
  } catch (e) {}
  return null;
}

/**
 * Marks keyword as used
 */
export async function markKeywordUsed(
  keywordId: string,
  pbUrl?: string
): Promise<void> {
  try {
    const pb = getPbClient(pbUrl);
    await pb.collection('seo_keywords').update(keywordId, {
      used: true,
      lastGenerated: new Date().toISOString()
    });
  } catch (e) {}
}

/**
 * Fetches all published articles from PocketBase
 */
export async function getPublishedArticlesFromPb(
  pbUrl?: string
): Promise<ArticleDraft[]> {
  try {
    const pb = getPbClient(pbUrl);
    const records = await pb.collection('yazilar').getFullList<ArticleDraft>({
      filter: 'aktif = true',
      sort: '-created'
    });
    return records;
  } catch (e) {
    return [];
  }
}

