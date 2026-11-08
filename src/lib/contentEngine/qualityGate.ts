import type { ArticleDraft, QualityReport } from './types';

export const MIN_ARTICLE_WORDS = 200;
export const MIN_ARTICLE_H2 = 3;

/**
 * Counts words in an HTML string ignoring HTML tags
 */
export function countHtmlWords(html: string): number {
  const text = html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
  if (!text) return 0;
  return text.split(' ').filter(w => w.length > 0).length;
}

/**
 * Counts <h2> tags in HTML
 */
export function countH2Tags(html: string): number {
  const matches = html.match(/<h2[^>]*>.*?<\/h2>/gi);
  return matches ? matches.length : 0;
}

/**
 * Checks if the text has proper Çelebi call to action
 */
export function hasCelebiCta(html: string): boolean {
  const lower = html.toLowerCase();
  const hasBrand = lower.includes('çelebi') || lower.includes('celebi');
  const hasContact = lower.includes('0 (322) 235 15 88') || 
                     lower.includes('0 (535) 873 03 24') || 
                     lower.includes('0 (533) 597 59 81') ||
                     lower.includes('whatsapp') ||
                     lower.includes('teklif');
  return hasBrand && hasContact;
}

/**
 * Injects internal contextual links
 */
export function injectInternalLinks(html: string, category: string): string {
  if (html.includes('id="celebi-internal-links"')) {
    return html;
  }

  const linksBlock = `
<div id="celebi-internal-links" class="mt-8 pt-6 border-t border-slate-200/80 bg-slate-50/60 p-4 rounded-2xl">
  <p class="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">İlgili Hizmet ve Rehber Sayfalarımız:</p>
  <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-sky-700 font-semibold">
    <li><a href="/site-yonetimi" class="hover:underline flex items-center gap-1.5"><span>🏢</span> Adana Profesyonel Site ve Apartman Yönetimi</a></li>
    <li><a href="/temizlik" class="hover:underline flex items-center gap-1.5"><span>✨</span> Kurumsal Ofis, İnşaat ve Merdiven Temizliği</a></li>
    <li><a href="/yazilar" class="hover:underline flex items-center gap-1.5"><span>📚</span> Kat Mülkiyeti Kanunu ve Sektörel Makaleler</a></li>
    <li><a href="/iletisim" class="hover:underline flex items-center gap-1.5"><span>📍</span> Çukurova / Mahfesığmaz Ofisimiz ve İletişim</a></li>
  </ul>
</div>
`;
  return html.trim() + '\n' + linksBlock;
}

const ENRICHMENT_SNIPPETS = [
  {
    h2: 'KMK Madde 20 ve Yasal Aidat Tahsilat Güvencesi',
    content: '<p>Kat Mülkiyeti Kanunu Madde 20 uyarınca, ortak gider avansını zamanında ödemeyen kat maliklerine aylık yüzde beş gecikme tazminatı işletilir. Çelebi Yönetim, aidat takip sürecini banka onaylı sistemler ve uzman hukukçular eşliğinde yürüterek binalarda sıfır tahsilat kaybı hedefler.</p>'
  },
  {
    h2: 'Adana Şehir İkliminde Düzenli Bakımın Önemi',
    content: '<p>Çukurova bölgesinin yoğun nemi ve yüksek yaz sıcaklıkları, bina hidrofor ve klima drenaj hatlarında kireçlenmeye; dış cephelerde ise toz birikmesine yol açar. Periyodik teknik bakım ve yüksek debili yıkama protokolleri, ortak donanımların kullanım ömrünü uzatır.</p>'
  },
  {
    h2: 'İşletme Projesi ve Şeffaf Mali Raporlama İlkeleri',
    content: '<p>Apartman bütçesi hazırlanırken tahmini yakıt, asansör periyodik muayene ve ortak elektrik faturaları arsa payına göre adil şekilde paylaştırılmalıdır. Her ay panoya asılan veya mobil bilgilendirmeyle paylaşılan gelir-gider dökümleri, komşular arasındaki güveni tesis eder.</p>'
  },
  {
    h2: 'SGK Belgeli Personel ile Hukuki Güvence',
    content: '<p>Temizlik ve bina bakım hizmetlerinde sigortasız eleman çalıştırmak yöneticilere ağır tazminat yükümlülükleri doğurabilir. Kurumsal sözleşmeli hizmet almak, tüm iş hukuku ve iş güvenliği sorumluluğunu profesyonel firmaya devreder.</p>'
  }
];

/**
 * Ensures minimum word count by enriching short drafts
 */
export function ensureMinArticleWords(html: string): string {
  let currentWords = countHtmlWords(html);
  if (currentWords >= MIN_ARTICLE_WORDS) {
    return html;
  }

  let enrichedHtml = html;
  for (const snippet of ENRICHMENT_SNIPPETS) {
    if (!enrichedHtml.toLowerCase().includes(snippet.h2.toLowerCase())) {
      const insertion = `\n<h2>${snippet.h2}</h2>\n${snippet.content}\n`;
      // Insert before the last paragraph or CTA
      const lastPIndex = enrichedHtml.lastIndexOf('<p>');
      if (lastPIndex !== -1) {
        enrichedHtml = enrichedHtml.slice(0, lastPIndex) + insertion + enrichedHtml.slice(lastPIndex);
      } else {
        enrichedHtml += insertion;
      }
      currentWords = countHtmlWords(enrichedHtml);
      if (currentWords >= MIN_ARTICLE_WORDS) {
        break;
      }
    }
  }

  return enrichedHtml;
}

/**
 * Complete assessment of an article draft
 */
export function assessArticleDraft(draft: ArticleDraft): QualityReport {
  const issues: string[] = [];
  const wordCount = countHtmlWords(draft.ozet);
  const h2Count = countH2Tags(draft.ozet);
  const hasCta = hasCelebiCta(draft.ozet);
  const hasInternalLinks = draft.ozet.includes('celebi-internal-links');

  // Check ending punctuation
  const cleanText = draft.ozet.replace(/<[^>]*>/g, ' ').trim();
  const properEnding = cleanText.endsWith('.') || cleanText.endsWith('!') || cleanText.endsWith('?');

  if (wordCount < MIN_ARTICLE_WORDS) {
    issues.push(`Kelime sayısı yetersiz (${wordCount}/${MIN_ARTICLE_WORDS}). En az ${MIN_ARTICLE_WORDS} kelime olmalı.`);
  }

  if (h2Count < MIN_ARTICLE_H2) {
    issues.push(`H2 alt başlık sayısı yetersiz (${h2Count}/${MIN_ARTICLE_H2}). En az ${MIN_ARTICLE_H2} adet <h2> başlığı bulunmalı.`);
  }

  if (!hasCta) {
    issues.push('Çelebi Yönetim marka adı veya telefon/WhatsApp iletişim çağrısı (CTA) eksik.');
  }

  if (!properEnding) {
    issues.push('Metin düzgün bitirilmemiş (nokta, ünlem veya soru işareti ile bitmeli).');
  }

  return {
    passed: issues.length === 0,
    wordCount,
    h2Count,
    hasCta,
    hasInternalLinks,
    properEnding,
    issues
  };
}

