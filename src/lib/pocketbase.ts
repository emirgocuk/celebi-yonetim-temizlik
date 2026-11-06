import PocketBase from 'pocketbase';
import { COMPANY_INFO, FAQS_DATA, REVIEWS_DATA, SERVICES_DATA, STATS_DATA } from './fallback-data';
import type { CompanyMeta, QuoteRequest, ReviewItem, ServiceItem } from './types';

// Singleton instance
const POCKETBASE_URL = import.meta.env.PUBLIC_POCKETBASE_URL || 'http://127.0.0.1:8090';
export const pb = new PocketBase(POCKETBASE_URL);

// Disable auto-cancellation for reliable concurrent requests
pb.autoCancellation(false);

/**
 * Fetch all active services with automatic fallback to static dataset
 */
export async function getServices(): Promise<ServiceItem[]> {
  try {
    const records = await pb.collection('hizmetler').getFullList<ServiceItem>({
      filter: 'is_active = true',
      sort: 'sort_order',
      requestKey: null,
    });
    if (records && records.length > 0) {
      return records;
    }
  } catch (error) {
    // Graceful fallback during SSG builds or offline dev
  }
  return SERVICES_DATA;
}

/**
 * Fetch approved client testimonials
 */
export async function getReviews(): Promise<ReviewItem[]> {
  try {
    const records = await pb.collection('yorumlar').getFullList<ReviewItem>({
      filter: 'is_approved = true',
      sort: '-rating,-created',
      requestKey: null,
    });
    if (records && records.length > 0) {
      return records;
    }
  } catch (error) {
    // Graceful fallback
  }
  return REVIEWS_DATA;
}

/**
 * Submit a new quote inquiry into PocketBase
 */
export async function submitQuoteRequest(data: QuoteRequest): Promise<{ success: boolean; id?: string; error?: string }> {
  try {
    const record = await pb.collection('teklif_talepleri').create({
      ...data,
      status: 'yeni',
    });
    return { success: true, id: record.id };
  } catch (error: any) {
    console.error('PocketBase submitQuoteRequest failed:', error);
    return { success: false, error: error?.message || 'Bir hata oluştu, lütfen doğrudan arayın veya WhatsApp ile iletişime geçin.' };
  }
}

/**
 * Get company settings/metadata
 */
export function getCompanyInfo(): CompanyMeta {
  return COMPANY_INFO;
}

export function getStats() {
  return STATS_DATA;
}

export function getFaqs() {
  return FAQS_DATA;
}

