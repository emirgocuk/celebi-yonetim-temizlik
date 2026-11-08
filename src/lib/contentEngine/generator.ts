import { findTemplateForKeyword } from './templates';
import { polishArticleWithLlm } from './llmPolish';
import { 
  assessArticleDraft, 
  ensureMinArticleWords, 
  injectInternalLinks, 
  countHtmlWords, 
  countH2Tags 
} from './qualityGate';
import type { ArticleDraft, GenerationOptions, GenerationResult } from './types';

export interface GenerationPipelineResult {
  draft: ArticleDraft;
  modeUsed: 'hybrid-llm' | 'template-fallback' | 'pure-template';
  qualityPassed: boolean;
  issues: string[];
}

/**
 * Runs the complete Article Draft Pipeline
 */
export async function runArticleDraftPipeline(
  options: GenerationOptions
): Promise<GenerationPipelineResult> {
  const { keyword, district = 'Çukurova', mode = 'hybrid', openRouterApiKey } = options;

  // 1. Select Template
  const template = findTemplateForKeyword(keyword);
  let baseDraft = template.generate(keyword, district);
  let modeUsed: 'hybrid-llm' | 'template-fallback' | 'pure-template' = 'pure-template';

  // 2. Hybrid / LLM Polishing
  if (mode === 'hybrid' || mode === 'llm') {
    const polished = await polishArticleWithLlm(baseDraft, keyword, openRouterApiKey);
    if (polished) {
      baseDraft = {
        ...baseDraft,
        baslik: polished.title,
        ozet: polished.bodyHtml,
        seoDescription: polished.seoDescription
      };
      modeUsed = 'hybrid-llm';
    } else {
      modeUsed = 'template-fallback';
    }
  }

  // 3. Quality Enrichment (Word count & Internal links)
  let enrichedBody = ensureMinArticleWords(baseDraft.ozet);
  enrichedBody = injectInternalLinks(enrichedBody, baseDraft.kategori);

  // 4. Assemble Draft
  const wordCount = countHtmlWords(enrichedBody);
  const h2Count = countH2Tags(enrichedBody);

  const finalDraft: ArticleDraft = {
    ...baseDraft,
    ozet: enrichedBody,
    kelimeSayisi: wordCount,
    h2Sayisi: h2Count,
    qualityPassed: false
  };

  // 5. Final Quality Gate Assessment
  const report = assessArticleDraft(finalDraft);
  finalDraft.qualityPassed = report.passed;

  return {
    draft: finalDraft,
    modeUsed,
    qualityPassed: report.passed,
    issues: report.issues
  };
}

