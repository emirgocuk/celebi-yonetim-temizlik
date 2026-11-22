"""
Generates clean, scalable SVG vector files for the 4 Çelebi Logo Re-interpretations.
"""

import os

SVG_DIR = os.path.abspath("public/assets/images")
os.makedirs(SVG_DIR, exist_ok=True)

# 1. Concept 1: Pure Architectural Monolith (Healed middle floor, no ÇA, no text)
svg_concept_1 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="100%" height="100%" fill="none">
  <!-- Concept 1: The Pure Architectural Monolith (Isometric Building Mark) -->
  <defs>
    <style>
      .black-block { fill: #0a0e17; transition: fill 0.3s; }
      .blue-block  { fill: #0056d6; transition: fill 0.3s; }
      .gap-line    { fill: #ffffff; }
    </style>
  </defs>

  <g transform="translate(0, 40)">
    <!-- ROOF / CROWN CHEVRON -->
    <!-- Left Crown (Black) -->
    <path class="black-block" d="M 400 120 L 140 270 L 140 330 L 400 180 Z" />
    <!-- Right Crown (Blue) -->
    <path class="blue-block" d="M 400 120 L 660 270 L 660 330 L 400 180 Z" />

    <!-- FLOOR 3 (UPPER LEVEL) -->
    <!-- Left Facade: 2 Blocks -->
    <path class="black-block" d="M 148 350 L 235 300 L 235 365 L 148 415 Z" />
    <path class="black-block" d="M 255 288 L 392 210 L 392 275 L 255 353 Z" />
    <!-- Right Facade: 2 Blocks -->
    <path class="blue-block" d="M 408 210 L 545 288 L 545 353 L 408 275 Z" />
    <path class="blue-block" d="M 565 300 L 652 350 L 652 415 L 565 365 Z" />

    <!-- FLOOR 2 (MIDDLE LEVEL - HEALED, SEAMLESS ARCHITECTURAL BLOCKS) -->
    <!-- Left Facade: 2 Blocks (Replaced the awkward ÇA cutout with solid architecture) -->
    <path class="black-block" d="M 148 435 L 300 348 L 300 413 L 148 500 Z" />
    <path class="black-block" d="M 320 336 L 392 295 L 392 360 L 320 401 Z" />
    <!-- Right Facade: 2 Blocks -->
    <path class="blue-block" d="M 408 295 L 480 336 L 480 401 L 408 360 Z" />
    <path class="blue-block" d="M 500 348 L 652 435 L 652 500 L 500 413 Z" />

    <!-- FLOOR 1 (GROUND LEVEL - TAPERING FOUNDATION) -->
    <!-- Left Facade: 2 Blocks -->
    <path class="black-block" d="M 148 520 L 235 470 L 235 535 L 148 585 Z" />
    <path class="black-block" d="M 255 458 L 392 380 L 392 445 L 255 523 Z" />
    <!-- Right Facade: 2 Blocks -->
    <path class="blue-block" d="M 408 380 L 545 458 L 545 523 L 408 445 Z" />
    <path class="blue-block" d="M 565 470 L 652 520 L 652 585 L 565 535 Z" />

    <!-- BASE ANCHOR (BOTTOM FOUNDATION) -->
    <path class="black-block" d="M 255 545 L 392 467 L 392 532 L 255 610 Z" />
    <path class="blue-block" d="M 408 467 L 545 545 L 545 610 L 408 532 Z" />
  </g>
</svg>'''

# 2. Concept 2: Neo-Isometric with Gradient & Depth (Apple Glassmorphism Style)
svg_concept_2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="100%" height="100%" fill="none">
  <!-- Concept 2: Neo-Isometric with Premium Gradients & Ambient Lighting -->
  <defs>
    <linearGradient id="grad-black" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <linearGradient id="grad-blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2563eb" />
      <stop offset="50%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#0369a1" />
    </linearGradient>
    <linearGradient id="grad-roof-l" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    <linearGradient id="grad-roof-r" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#0284c7" />
    </linearGradient>
    <filter id="subtle-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#0284c7" flood-opacity="0.12" />
    </filter>
  </defs>

  <g transform="translate(0, 40)" filter="url(#subtle-shadow)">
    <!-- ROOF / CROWN CHEVRON -->
    <path fill="url(#grad-roof-l)" d="M 400 120 L 140 270 L 140 330 L 400 180 Z" />
    <path fill="url(#grad-roof-r)" d="M 400 120 L 660 270 L 660 330 L 400 180 Z" />

    <!-- Specular highlight on crown apex -->
    <path d="M 400 120 L 400 180" stroke="#ffffff" stroke-width="2" stroke-linecap="round" opacity="0.6" />

    <!-- FLOOR 3 -->
    <path fill="url(#grad-black)" d="M 148 350 L 235 300 L 235 365 L 148 415 Z" />
    <path fill="url(#grad-black)" d="M 255 288 L 392 210 L 392 275 L 255 353 Z" />
    <path fill="url(#grad-blue)" d="M 408 210 L 545 288 L 545 353 L 408 275 Z" />
    <path fill="url(#grad-blue)" d="M 565 300 L 652 350 L 652 415 L 565 365 Z" />

    <!-- FLOOR 2 (UNIFIED LUXURY ARCHITECTURE) -->
    <path fill="url(#grad-black)" d="M 148 435 L 300 348 L 300 413 L 148 500 Z" />
    <path fill="url(#grad-black)" d="M 320 336 L 392 295 L 392 360 L 320 401 Z" />
    <path fill="url(#grad-blue)" d="M 408 295 L 480 336 L 480 401 L 408 360 Z" />
    <path fill="url(#grad-blue)" d="M 500 348 L 652 435 L 652 500 L 500 413 Z" />

    <!-- FLOOR 1 -->
    <path fill="url(#grad-black)" d="M 148 520 L 235 470 L 235 535 L 148 585 Z" />
    <path fill="url(#grad-black)" d="M 255 458 L 392 380 L 392 445 L 255 523 Z" />
    <path fill="url(#grad-blue)" d="M 408 380 L 545 458 L 545 523 L 408 445 Z" />
    <path fill="url(#grad-blue)" d="M 565 470 L 652 520 L 652 585 L 565 535 Z" />

    <!-- FOUNDATION TAPER -->
    <path fill="url(#grad-black)" d="M 255 545 L 392 467 L 392 532 L 255 610 Z" />
    <path fill="url(#grad-blue)" d="M 408 467 L 545 545 L 545 610 L 408 532 Z" />
  </g>
</svg>'''

# 3. Concept 3: Full Brandmark with Modern Luxury Typography Lockup
svg_concept_3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1100" width="100%" height="100%" fill="none">
  <!-- Concept 3: Full Logo with Modern Architectural Typography -->
  <defs>
    <linearGradient id="c3-black" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <linearGradient id="c3-blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#0369a1" />
    </linearGradient>
  </defs>

  <!-- ICON (Centered, Scale 0.8) -->
  <g transform="translate(180, 20) scale(0.8)">
    <!-- ROOF CHEVRON -->
    <path fill="#0f172a" d="M 400 120 L 140 270 L 140 330 L 400 180 Z" />
    <path fill="#0284c7" d="M 400 120 L 660 270 L 660 330 L 400 180 Z" />

    <!-- FLOOR 3 -->
    <path fill="#0f172a" d="M 148 350 L 235 300 L 235 365 L 148 415 Z" />
    <path fill="#0f172a" d="M 255 288 L 392 210 L 392 275 L 255 353 Z" />
    <path fill="#0284c7" d="M 408 210 L 545 288 L 545 353 L 408 275 Z" />
    <path fill="#0284c7" d="M 565 300 L 652 350 L 652 415 L 565 365 Z" />

    <!-- FLOOR 2 -->
    <path fill="#0f172a" d="M 148 435 L 300 348 L 300 413 L 148 500 Z" />
    <path fill="#0f172a" d="M 320 336 L 392 295 L 392 360 L 320 401 Z" />
    <path fill="#0284c7" d="M 408 295 L 480 336 L 480 401 L 408 360 Z" />
    <path fill="#0284c7" d="M 500 348 L 652 435 L 652 500 L 500 413 Z" />

    <!-- FLOOR 1 -->
    <path fill="#0f172a" d="M 148 520 L 235 470 L 235 535 L 148 585 Z" />
    <path fill="#0f172a" d="M 255 458 L 392 380 L 392 445 L 255 523 Z" />
    <path fill="#0284c7" d="M 408 380 L 545 458 L 545 523 L 408 445 Z" />
    <path fill="#0284c7" d="M 565 470 L 652 520 L 652 585 L 565 535 Z" />

    <!-- BASE -->
    <path fill="#0f172a" d="M 255 545 L 392 467 L 392 532 L 255 610 Z" />
    <path fill="#0284c7" d="M 408 467 L 545 545 L 545 610 L 408 532 Z" />
  </g>

  <!-- TYPOGRAPHY: RE-INTERPRETED & REFINED -->
  <!-- "ÇELEBİ" in Bold Modern Architectural Kerning -->
  <text x="500" y="680" text-anchor="middle" font-family="system-ui, -apple-system, 'SF Pro Display', 'Inter', sans-serif" font-size="54" font-weight="900" fill="#0f172a" letter-spacing="14">
    ÇELEBİ
  </text>
  
  <!-- "YÖNETİM & TEMİZLİK" in Royal Blue with Premium Letter-spacing -->
  <text x="500" y="735" text-anchor="middle" font-family="system-ui, -apple-system, 'SF Pro Display', 'Inter', sans-serif" font-size="24" font-weight="700" fill="#0284c7" letter-spacing="8">
    YÖNETİM &amp; TEMİZLİK
  </text>

  <!-- Tagline / Trust Indicator -->
  <line x1="320" y1="775" x2="680" y2="775" stroke="#e2e8f0" stroke-width="1.5" />
  <text x="500" y="805" text-anchor="middle" font-family="system-ui, -apple-system, 'Inter', sans-serif" font-size="13" font-weight="600" fill="#64748b" letter-spacing="4">
    KURUMSAL TESİS YÖNETİMİ &bull; ADANA
  </text>
</svg>'''

# 4. Concept 4: Horizontal Header Lockup (Optimized for Web Navbar & Mobile)
svg_concept_4 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 80" width="100%" height="100%" fill="none">
  <!-- Concept 4: Horizontal Web Navigation Lockup -->
  <!-- Mark (Scaled and positioned left) -->
  <g transform="translate(-10, -5) scale(0.135)">
    <!-- Roof -->
    <path fill="#0f172a" d="M 400 120 L 140 270 L 140 330 L 400 180 Z" />
    <path fill="#0284c7" d="M 400 120 L 660 270 L 660 330 L 400 180 Z" />
    <!-- Floor 3 -->
    <path fill="#0f172a" d="M 148 350 L 235 300 L 235 365 L 148 415 Z" />
    <path fill="#0f172a" d="M 255 288 L 392 210 L 392 275 L 255 353 Z" />
    <path fill="#0284c7" d="M 408 210 L 545 288 L 545 353 L 408 275 Z" />
    <path fill="#0284c7" d="M 565 300 L 652 350 L 652 415 L 565 365 Z" />
    <!-- Floor 2 -->
    <path fill="#0f172a" d="M 148 435 L 300 348 L 300 413 L 148 500 Z" />
    <path fill="#0f172a" d="M 320 336 L 392 295 L 392 360 L 320 401 Z" />
    <path fill="#0284c7" d="M 408 295 L 480 336 L 480 401 L 408 360 Z" />
    <path fill="#0284c7" d="M 500 348 L 652 435 L 652 500 L 500 413 Z" />
    <!-- Floor 1 -->
    <path fill="#0f172a" d="M 148 520 L 235 470 L 235 535 L 148 585 Z" />
    <path fill="#0f172a" d="M 255 458 L 392 380 L 392 445 L 255 523 Z" />
    <path fill="#0284c7" d="M 408 380 L 545 458 L 545 523 L 408 445 Z" />
    <path fill="#0284c7" d="M 565 470 L 652 520 L 652 585 L 565 535 Z" />
    <!-- Base -->
    <path fill="#0f172a" d="M 255 545 L 392 467 L 392 532 L 255 610 Z" />
    <path fill="#0284c7" d="M 408 467 L 545 545 L 545 610 L 408 532 Z" />
  </g>

  <!-- Typography -->
  <text x="96" y="38" font-family="system-ui, -apple-system, 'SF Pro Display', 'Inter', sans-serif" font-size="28" font-weight="900" fill="#0f172a" letter-spacing="4">
    ÇELEBİ
  </text>
  <text x="96" y="58" font-family="system-ui, -apple-system, 'SF Pro Display', 'Inter', sans-serif" font-size="12" font-weight="700" fill="#0284c7" letter-spacing="2.5">
    YÖNETİM &amp; TEMİZLİK
  </text>
</svg>'''

files = {
    "celebi-logo-monolith.svg": svg_concept_1,
    "celebi-logo-gradient.svg": svg_concept_2,
    "celebi-logo-full-brandmark.svg": svg_concept_3,
    "celebi-logo-header.svg": svg_concept_4
}

for name, content in files.items():
    p = os.path.join(SVG_DIR, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated: {p}")
