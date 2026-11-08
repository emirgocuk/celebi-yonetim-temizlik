import type { ArticleDraft } from './types';

const FALLBACK_MODELS = [
  'nvidia/nemotron-3.5-lightning:free',
  'nvidia/nemotron-3-ultra-550b-a55b:free',
  'google/gemma-2-9b-it:free',
  'meta-llama/llama-3.3-70b-instruct:free'
];

interface PolishResult {
  title: string;
  bodyHtml: string;
  seoDescription: string;
}

/**
 * Polishes an article draft using OpenRouter with resilient fallback chain.
 * Returns null if LLM fails, enabling fail-soft template execution.
 */
export async function polishArticleWithLlm(
  draft: Omit<ArticleDraft, 'kelimeSayisi' | 'h2Sayisi' | 'qualityPassed'>,
  keyword: string,
  apiKey?: string
): Promise<PolishResult | null> {
  const token = apiKey || (typeof process !== 'undefined' ? process.env?.OPENROUTER_API_KEY : '');
  if (!token) {
    return null; // Fail-soft to template engine
  }

  const systemPrompt = `Sen Adana'da faaliyet gösteren "Çelebi Yönetim ve Temizlik" firmasının kıdemli içerik yöneticisi ve Kat Mülkiyeti Kanunu uzmanısın.
Görevin; verilen taslak makaleyi Adana yerel şartlarına (Çukurova, Seyhan, Yüreğir) uygun, doğal akıcı Türkiye Türkçesiyle, profesyonel ve ikna edici bir dille zenginleştirmektir.

KURALLAR:
1. Devrik, yabancı veya çeviri kokan yapay zeka klişeleri KESİNLİKLE YASAKTIR.
2. Kesinlikle <h1> KULLANMA. Başlıklar sadece <h2> olmalıdır.
3. En az 3 adet <h2> başlığı bulunmalı ve metin 250-400 kelime arasında olmalıdır.
4. Son paragrafta mutlaka Çelebi Yönetim ve Temizlik marka adı, Adana Çukurova Mahfesığmaz ofisi, 0 (322) 235 15 88 sabit hat veya 0 (535) 873 03 24 WhatsApp teklif çağrısı (CTA) yer almalıdır.
5. Çıktıyı JSON formatında ver: {"title": "...", "bodyHtml": "...", "seoDescription": "..."}`;

  const userPrompt = `Konu/Anahtar Kelime: ${keyword}
Mevcut Başlık: ${draft.baslik}
Kategori: ${draft.kategori}
Mevcut HTML Taslak:
${draft.ozet}

Lütfen bu taslağı cilala, HTML formatında (p, h2, ul, li) zenginleştir ve JSON olarak döndür.`;

  for (const model of FALLBACK_MODELS) {
    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://celebiyonetim.com.tr',
          'X-Title': 'Celebi Yonetim Content Engine'
        },
        body: JSON.stringify({
          model,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userPrompt }
          ],
          response_format: { type: 'json_object' },
          temperature: 0.7,
          max_tokens: 1500
        }),
        signal: AbortSignal.timeout(12000)
      });

      if (!response.ok) {
        continue; // Try next fallback model
      }

      const data = await response.json();
      const rawContent = data.choices?.[0]?.message?.content;
      if (!rawContent) continue;

      const parsed = JSON.parse(rawContent);
      if (parsed.bodyHtml && parsed.title) {
        return {
          title: parsed.title,
          bodyHtml: parsed.bodyHtml,
          seoDescription: parsed.seoDescription || draft.seoDescription
        };
      }
    } catch (err) {
      // Continue to next model on timeout or error
      continue;
    }
  }

  // All LLM attempts failed or timed out: Gracefully fallback
  return null;
}

