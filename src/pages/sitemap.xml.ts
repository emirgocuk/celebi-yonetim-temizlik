import type { APIRoute } from 'astro';
import { ARTICLES_DATA } from '@/lib/articles-data';

const staticPages = [
  '',
  'iletisim',
  'yazilar',
];

const articlePages = ARTICLES_DATA.map((a) => `yazilar/${a.slug}`);

const allPages = [...staticPages, ...articlePages];

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = site ? site.origin : 'https://www.celebiyonetim.com.tr';
  const lastmod = new Date().toISOString().split('T')[0];

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
