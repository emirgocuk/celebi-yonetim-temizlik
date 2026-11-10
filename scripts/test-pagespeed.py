import urllib.request
import json
import sys

def run_test(strategy='mobile'):
    print(f"Running Google PageSpeed Insights test ({strategy})...")
    api_url = (
        f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
        f"url=https://celebiyonetim.com.tr&strategy={strategy}&"
        f"category=ACCESSIBILITY&category=PERFORMANCE&category=BEST_PRACTICES&category=SEO"
    )
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode('utf-8'))
            lighthouse = result.get('lighthouseResult', {})
            categories = lighthouse.get('categories', {})
            audits = lighthouse.get('audits', {})

            print("\n=== Lighthouse Scores ===")
            for cat_id, cat_data in categories.items():
                title = cat_data.get('title', cat_id)
                score = int((cat_data.get('score') or 0) * 100)
                print(f"• {title}: {score}/100")

            # Check ARIA audit
            aria_audit = audits.get('aria-allowed-attr', {})
            print(f"\n• ARIA Allowed Attributes: {aria_audit.get('score')} ({aria_audit.get('displayValue', 'Passed' if aria_audit.get('score') == 1 else 'Failed')})")

            # Core Web Vitals
            fcp = audits.get('first-contentful-paint', {}).get('displayValue')
            lcp = audits.get('largest-contentful-paint', {}).get('displayValue')
            cls = audits.get('cumulative-layout-shift', {}).get('displayValue')
            tbt = audits.get('total-blocking-time', {}).get('displayValue')

            print("\n=== Core Web Vitals ===")
            print(f"• First Contentful Paint (FCP): {fcp}")
            print(f"• Largest Contentful Paint (LCP): {lcp}")
            print(f"• Cumulative Layout Shift (CLS): {cls}")
            print(f"• Total Blocking Time (TBT): {tbt}")
            return result
    except Exception as e:
        print(f"Error calling PageSpeed API: {e}", file=sys.stderr)
        return None

if __name__ == '__main__':
    run_test('mobile')
