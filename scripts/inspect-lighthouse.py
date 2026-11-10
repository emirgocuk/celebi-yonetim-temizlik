import json

with open('lighthouse-report.json', encoding='utf-8') as f:
    data = json.load(f)

categories = data.get('categories', {})
audits = data.get('audits', {})

print("=== Lighthouse Scores ===")
for cat_id, cat_data in categories.items():
    title = cat_data.get('title', cat_id)
    score = int((cat_data.get('score') or 0) * 100)
    print(f"• {title}: {score}/100")

print("\n=== Key Audits ===")
aria = audits.get('aria-allowed-attr', {})
print(f"• ARIA Allowed Attributes: score={aria.get('score')} ({'PASSED' if aria.get('score') == 1 else 'FAILED'})")

# Look for agentic / accessibility audits
for k in audits:
    if any(term in k.lower() for term in ['agent', 'llm', 'ard', 'aria']):
        a = audits[k]
        score = a.get('score')
        title = a.get('title')
        if score is not None:
            print(f"  - {title} ({k}): {score}")

fcp = audits.get('first-contentful-paint', {}).get('displayValue')
lcp = audits.get('largest-contentful-paint', {}).get('displayValue')
cls = audits.get('cumulative-layout-shift', {}).get('displayValue')
tbt = audits.get('total-blocking-time', {}).get('displayValue')
print(f"\nCore Web Vitals:")
print(f"• FCP: {fcp}")
print(f"• LCP: {lcp}")
print(f"• CLS: {cls}")
print(f"• TBT: {tbt}")
