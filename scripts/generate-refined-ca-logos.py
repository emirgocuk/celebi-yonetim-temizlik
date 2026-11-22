import os
import subprocess

SVG_DIR = os.path.abspath("public/assets/images")
ART_DIR = r"C:\Users\Emir\.gemini\antigravity\brain\735d97f9-6db9-41b9-a356-8ec8cfeb771c"
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(ART_DIR, exist_ok=True)

# Common Building Geometry (Exact 100% Faithful Reproduction of the Original Reference)
# Center X = 400
def get_building_svg(ca_content, title="Çelebi Logo"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="100%" height="100%" fill="none">
  <!-- {title} -->
  <defs>
    <style>
      .black-part {{ fill: #000000; }}
      .blue-part  {{ fill: #004aad; }}
    </style>
  </defs>

  <g transform="translate(0, 30)">
    <!-- 1. ROOF CHEVRON -->
    <!-- Left Roof (Black) -->
    <path class="black-part" d="M 400 120 L 145 260 L 145 322 L 400 182 Z" />
    <!-- Right Roof (Blue) -->
    <path class="blue-part" d="M 400 120 L 655 260 L 655 322 L 400 182 Z" />

    <!-- 2. FLOOR 1 (TOP FLOOR) -->
    <!-- Left Facade: Outer Block + Inner Block -->
    <path class="black-part" d="M 152 342 L 235 297 L 235 360 L 152 405 Z" />
    <path class="black-part" d="M 252 287 L 392 212 L 392 275 L 252 350 Z" />
    <!-- Right Facade: Inner Block + Outer Block -->
    <path class="blue-part" d="M 408 212 L 548 287 L 548 350 L 408 275 Z" />
    <path class="blue-part" d="M 565 297 L 648 342 L 648 405 L 565 360 Z" />

    <!-- 3. FLOOR 2 (MIDDLE FLOOR - WITH ÇA OPENING) -->
    <!-- Left Facade: Outer Block -->
    <path class="black-part" d="M 152 425 L 305 342 L 305 405 L 152 488 Z" />
    <!-- Right Facade: Outer Block -->
    <path class="blue-part" d="M 495 342 L 648 425 L 648 488 L 495 405 Z" />

    <!-- ==================== CENTRAL ÇA EMBLEM ==================== -->
    {ca_content}
    <!-- ========================================================== -->

    <!-- 4. FLOOR 3 (LOWER FLOOR) -->
    <!-- Left Facade: Outer Block + Inner Block -->
    <path class="black-part" d="M 152 508 L 235 463 L 235 526 L 152 571 Z" />
    <path class="black-part" d="M 252 453 L 392 378 L 392 441 L 252 516 Z" />
    <!-- Right Facade: Inner Block + Outer Block -->
    <path class="blue-part" d="M 408 378 L 548 453 L 548 516 L 408 441 Z" />
    <path class="blue-part" d="M 565 463 L 648 508 L 648 571 L 565 526 Z" />

    <!-- 5. BASE ANCHOR (BOTTOM FOUNDATION) -->
    <path class="black-part" d="M 252 538 L 392 463 L 392 526 L 252 601 Z" />
    <path class="blue-part" d="M 408 463 L 548 538 L 548 601 L 408 526 Z" />
  </g>
</svg>'''

# VARIATION 1: Modern Swiss Geometric ÇA (Cleaned up, perfectly balanced, modern cedilla)
ca_v1 = '''<g id="ca-v1-geometric">
      <!-- 'Ç' in Solid Black (Geometric, harmonious curve, sleek modern cedilla) -->
      <g class="black-part">
        <!-- Main 'C' Body -->
        <path d="M 390 348 L 348 348 C 322 348 304 366 304 395 C 304 424 322 442 348 442 L 390 442 L 390 422 L 350 422 C 334 422 324 412 324 395 C 324 378 334 368 350 368 L 390 368 Z" />
        <!-- Sleek Modern Cedilla (Alt Çengeli - Clean architectural anchor) -->
        <path d="M 342 446 L 354 446 L 354 464 L 338 464 L 338 456 L 344 456 Z" />
      </g>

      <!-- 'A' in Royal Blue (Crisp apex, unified line-weight, balanced crossbar) -->
      <g class="blue-part">
        <!-- Outer A Contour & Inner Counter -->
        <path d="M 452 348 L 420 442 L 441 442 L 447 423 L 477 423 L 483 442 L 504 442 L 472 348 Z M 462 376 L 472 406 L 452 406 Z" />
      </g>
    </g>'''

# VARIATION 2: Isometric 3D Angled ÇA (Perspektif Uyumlu: Ç sola yatık, A sağa yatık)
ca_v2 = '''<g id="ca-v2-isometric">
      <!-- 'Ç' in Solid Black (Slightly sheared to match left building perspective) -->
      <g class="black-part" transform="translate(348, 395) skewY(8) translate(-348, -395)">
        <path d="M 392 348 L 348 348 C 322 348 304 366 304 395 C 304 424 322 442 348 442 L 392 442 L 392 421 L 350 421 C 334 421 324 412 324 395 C 324 378 334 369 350 369 L 392 369 Z" />
        <path d="M 342 446 L 354 446 L 354 465 L 336 465 L 336 456 L 344 456 Z" />
      </g>

      <!-- 'A' in Royal Blue (Slightly sheared to match right building perspective) -->
      <g class="blue-part" transform="translate(460, 395) skewY(-8) translate(-460, -395)">
        <path d="M 452 348 L 420 442 L 441 442 L 447 423 L 477 423 L 483 442 L 504 442 L 472 348 Z M 462 376 L 472 406 L 452 406 Z" />
      </g>
    </g>'''

# VARIATION 3: Luxury Bold Architectural ÇA (Thicker luxury stroke, perfectly matching the heavy block weight)
ca_v3 = '''<g id="ca-v3-luxury-bold">
      <!-- 'Ç' Bold Architectural Weight -->
      <g class="black-part">
        <path d="M 392 344 L 345 344 C 316 344 296 365 296 395 C 296 425 316 446 345 446 L 392 446 L 392 422 L 348 422 C 332 422 322 411 322 395 C 322 379 332 368 348 368 L 392 368 Z" />
        <!-- Minimalist Diamond / Prism Cedilla -->
        <polygon points="345,450 354,460 345,470 336,460" />
      </g>

      <!-- 'A' Bold Architectural Weight with floating modern crossbar -->
      <g class="blue-part">
        <path d="M 454 344 L 418 446 L 443 446 L 450 425 L 478 425 L 485 446 L 510 446 L 474 344 Z M 464 372 L 474 404 L 454 404 Z" />
      </g>
    </g>'''

svg_v1 = get_building_svg(ca_v1, "Çelebi Logo - Variation 1: Geometrik Modern Dokunuş")
svg_v2 = get_building_svg(ca_v2, "Çelebi Logo - Variation 2: İzometrik Perspektif Dokunuşu")
svg_v3 = get_building_svg(ca_v3, "Çelebi Logo - Variation 3: Lüks Mimari Ç-A")

# Complete Lockup with ÇA V1 + Clean Typography Below
svg_v4 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1150" width="100%" height="100%" fill="none">
  <!-- Çelebi Logo - Variation 4: Orijinal Mimari + Zarif Tipografi -->
  <defs>
    <style>
      .black-part {{ fill: #000000; }}
      .blue-part  {{ fill: #004aad; }}
    </style>
  </defs>

  <!-- MARK (Scaled and centered at top) -->
  <g transform="translate(100, 20)">
    <!-- 1. ROOF CHEVRON -->
    <path class="black-part" d="M 400 120 L 145 260 L 145 322 L 400 182 Z" />
    <path class="blue-part" d="M 400 120 L 655 260 L 655 322 L 400 182 Z" />

    <!-- 2. FLOOR 1 -->
    <path class="black-part" d="M 152 342 L 235 297 L 235 360 L 152 405 Z" />
    <path class="black-part" d="M 252 287 L 392 212 L 392 275 L 252 350 Z" />
    <path class="blue-part" d="M 408 212 L 548 287 L 548 350 L 408 275 Z" />
    <path class="blue-part" d="M 565 297 L 648 342 L 648 405 L 565 360 Z" />

    <!-- 3. FLOOR 2 (WITH POLISHED ÇA) -->
    <path class="black-part" d="M 152 425 L 305 342 L 305 405 L 152 488 Z" />
    <path class="blue-part" d="M 495 342 L 648 425 L 648 488 L 495 405 Z" />

    {ca_v1}

    <!-- 4. FLOOR 3 -->
    <path class="black-part" d="M 152 508 L 235 463 L 235 526 L 152 571 Z" />
    <path class="black-part" d="M 252 453 L 392 378 L 392 441 L 252 516 Z" />
    <path class="blue-part" d="M 408 378 L 548 453 L 548 516 L 408 441 Z" />
    <path class="blue-part" d="M 565 463 L 648 508 L 648 571 L 565 526 Z" />

    <!-- 5. BASE ANCHOR -->
    <path class="black-part" d="M 252 538 L 392 463 L 392 526 L 252 601 Z" />
    <path class="blue-part" d="M 408 463 L 548 538 L 548 601 L 408 526 Z" />
  </g>

  <!-- TYPOGRAPHY: REFINED MODERN EXECUTIVE FONT (Replaces old stretched font) -->
  <text x="500" y="770" text-anchor="middle" font-family="system-ui, -apple-system, 'SF Pro Display', 'Inter', sans-serif" font-size="58" font-weight="900" fill="#004aad" letter-spacing="10">
    ÇELEBİ YÖNETİM
  </text>
  <text x="500" y="820" text-anchor="middle" font-family="system-ui, -apple-system, 'Inter', sans-serif" font-size="20" font-weight="700" fill="#0f172a" letter-spacing="8">
    HİZMET İŞLERİ LTD. ŞTİ.
  </text>
</svg>'''

files = {
    "celebi-logo-original-refined-v1.svg": svg_v1,
    "celebi-logo-original-refined-v2.svg": svg_v2,
    "celebi-logo-original-refined-v3.svg": svg_v3,
    "celebi-logo-original-refined-v4.svg": svg_v4
}

for name, content in files.items():
    p_pub = os.path.join(SVG_DIR, name)
    p_art = os.path.join(ART_DIR, name)
    with open(p_pub, "w", encoding="utf-8") as f:
        f.write(content.strip())
    with open(p_art, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated: {name}")

# Render to PNG for artifact preview
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

for name in files.keys():
    svg_p = os.path.join(ART_DIR, name)
    png_name = name.replace(".svg", ".png")
    png_p = os.path.join(ART_DIR, png_name)
    win_size = "1000,1150" if "v4" in name else "1000,1000"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        f"--screenshot={png_p}",
        f"--window-size={win_size}",
        "--default-background-color=00000000",
        svg_p
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(png_p):
        print(f"Rendered PNG: {png_name} ({os.path.getsize(png_p)} bytes)")

# Remove temporary script if any
if os.path.exists("scripts/create-ca-script.py"):
    os.remove("scripts/create-ca-script.py")
