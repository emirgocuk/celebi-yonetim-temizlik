import type { APIRoute } from 'astro';
import { ARTICLES_DATA } from '@/lib/articles-data';

const staticPages = [
  '',
  'site-yonetimi',
  'site-yonetimi-fiyat-hesapla',
  'temizlik',
  'cukurova-site-yonetimi',
  'seyhan-apartman-yonetimi',
  'saricam-site-yonetimi',
  'iletisim',
  'yazilar',
  'yasal/kvkk-aydinlatma-metni',
  'yasal/gizlilik-politikasi',
  'yasal/cerez-politikasi',
  'yasal/kullanim-kosullari',
  'yasal/hizmet-ve-teklif-kosullari',
];

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = (site ? site.origin : 'https://celebiyonetim.com.tr').replace('www.', '');
  const lastmod = new Date().toISOString().split('T')[0];

  // Slugs collected from fallback data + live PocketBase API
  const slugsSet = new Set<string>(ARTICLES_DATA.map((a) => a.slug));

  const pbEndpoints = [
    'https://celebiyonetim.com.tr/api/collections/yazilar/records?perPage=200',
    `${import.meta.env.POCKETBASE_URL || 'http://127.0.0.1:8090'}/api/collections/yazilar/records?perPage=200`,
  ];

  for (const endpoint of pbEndpoints) {
    try {
      const res = await fetch(endpoint, {
        headers: { 'User-Agent': 'Mozilla/5.0' },
        signal: AbortSignal.timeout(3500),
      });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data.items) && data.items.length > 0) {
          for (const item of data.items) {
            const slug = String(item.slug || '').trim();
            if (slug && item.aktif !== false && /^[a-z0-9-]+$/i.test(slug)) {
              slugsSet.add(slug);
            }
          }
          break;
        }
      }
    } catch (_) {
      // Try next endpoint or keep fallback set
    }
  }

  const articlePages = Array.from(slugsSet).map((slug) => `yazilar/${slug}`);
  const allPages = [...staticPages, ...articlePages];

const highPriorityPages = new Set([
  'yazilar',
  'site-yonetimi',
  'site-yonetimi-fiyat-hesapla',
  'temizlik',
  'cukurova-site-yonetimi',
  'seyhan-apartman-yonetimi',
  'saricam-site-yonetimi',
]);

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages
  .map((page) => {
    const url = page ? `${baseUrl}/${page}` : baseUrl;
    const priority = page === '' ? '1.0' : page === 'site-yonetimi-fiyat-hesapla' ? '0.95' : highPriorityPages.has(page) ? '0.9' : '0.8';
    return `  <url>
    <loc>${url}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${priority}</priority>
  </url>`;
  })
  .join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
