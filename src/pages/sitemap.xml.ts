import type { APIRoute } from 'astro';
import { ARTICLES_DATA } from '@/lib/articles-data';

const staticPages = [
  '',
  'iletisim',
  'yazilar',
];

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = (site ? site.origin : 'https://celebiyonetim.com.tr').replace('www.', '');
  const lastmod = new Date().toISOString().split('T')[0];

  // Slugs collected from fallback data
  const slugsSet = new Set<string>(ARTICLES_DATA.map((a) => a.slug));

  // Also attempt to fetch latest active articles from PocketBase API
  try {
    const pbUrl = import.meta.env.POCKETBASE_URL || 'http://127.0.0.1:8090';
    const res = await fetch(`${pbUrl}/api/collections/yazilar/records?page=1&perPage=100&filter=aktif%3Dtrue`, {
      signal: AbortSignal.timeout(2000),
    });
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data.items)) {
        for (const item of data.items) {
          if (item.slug) slugsSet.add(item.slug);
        }
      }
    }
  } catch (e) {
    // PocketBase unreachable at build time, fallback set is preserved
  }

  const articlePages = Array.from(slugsSet).map((slug) => `yazilar/${slug}`);
  const allPages = [...staticPages, ...articlePages];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages
  .map((page) => {
    const url = page ? `${baseUrl}/${page}` : baseUrl;
    const priority = page === '' ? '1.0' : page === 'yazilar' ? '0.9' : '0.8';
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
