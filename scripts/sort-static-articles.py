import re

content = open('src/lib/articles-data.ts', encoding='utf-8').read()
header_idx = content.find('export const ARTICLES_DATA: ArticleItem[] = [')
header = content[:header_idx]
array_part = content[header_idx + len('export const ARTICLES_DATA: ArticleItem[] = ['):]

# Split articles by top-level object
items = []
current = []
depth = 0
in_string = False
str_char = ''
escape = False

for char in array_part:
    if escape:
        escape = False
        current.append(char)
        continue
    if char == '\\':
        escape = True
        current.append(char)
        continue
    if char in ('"', "'"):
        if not in_string:
            in_string = True
            str_char = char
        elif str_char == char:
            in_string = False
        current.append(char)
        continue
    if in_string:
        current.append(char)
        continue
    if char == '{':
        depth += 1
        current.append(char)
    elif char == '}':
        depth -= 1
        current.append(char)
        if depth == 0:
            item_text = ''.join(current).strip().rstrip(',')
            if item_text:
                items.append(item_text)
            current = []
    elif depth > 0:
        current.append(char)

print(f'Parsed {len(items)} items')
assert len(items) == 6

# Reverse items (newest first)
reversed_items = list(reversed(items))

helper = """
export function parseDateToTime(dateStr: string): number {
  if (!dateStr) return 0;
  const str = String(dateStr).trim();
  if (str.toLowerCase() === 'bugün' || str.toLowerCase() === 'yeni') return Date.now();

  const trMonths: Record<string, number> = {
    'ocak': 0, 'şubat': 1, 'mart': 2, 'nisan': 3, 'mayıs': 4, 'haziran': 5,
    'temmuz': 6, 'ağustos': 7, 'eylül': 8, 'ekim': 9, 'kasım': 10, 'aralık': 11,
    'january': 0, 'february': 1, 'march': 2, 'april': 3, 'may': 4, 'june': 5,
    'july': 6, 'august': 7, 'september': 8, 'october': 9, 'november': 10, 'december': 11
  };

  const m = str.match(/^(\\d{1,2})\\s+([a-zA-ZçÇğĞıİöÖşŞüÜ]+)\\s+(\\d{4})/i);
  if (m) {
    const day = parseInt(m[1], 10);
    const monthKey = m[2].toLowerCase();
    const year = parseInt(m[3], 10);
    if (monthKey in trMonths) {
      return new Date(year, trMonths[monthKey], day).getTime();
    }
  }

  const parsed = Date.parse(str);
  if (!isNaN(parsed)) return parsed;

  return 0;
}
"""

new_content = header + helper + '\nexport const ARTICLES_DATA: ArticleItem[] = [\n' + ',\n'.join(['  ' + it for it in reversed_items]) + '\n];\n'
open('src/lib/articles-data.ts', 'w', encoding='utf-8').write(new_content)
print('Successfully rewrote src/lib/articles-data.ts sorted newest-first!')
