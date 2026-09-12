from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

MAP = {
    ('gwangju','gwangsan'): ('광주 광산구','광산구이미지.png'),
    ('gwangju','bukgu'): ('광주 북구','북구이미지.png'),
    ('gwangju','seogu'): ('광주 서구','서구이미지.png'),
    ('gwangju','namgu'): ('광주 남구','남구이미지.png'),
    ('gwangju','donggu'): ('광주 동구','동구이미지.png'),
    ('jeonnam','mokpo'): ('목포','목포이미지.png'),
    ('jeonnam','yeosu'): ('여수','여수지역 이미지.png'),
    ('jeonnam','suncheon'): ('순천','순천지역 이미지.png'),
    ('jeonnam','naju'): ('나주','나주지역 이미지.png'),
    ('jeonnam','gwangyang'): ('광양','광양지역 이미지 주황.png'),
    ('jeonnam','damyang'): ('담양','담양이미지.png'),
    ('jeonnam','gokseong'): ('곡성','곡성이미지.png'),
    ('jeonnam','gurye'): ('구례','구례이미지.png'),
    ('jeonnam','goheung'): ('고흥','고흥이미지.png'),
    ('jeonnam','boseong'): ('보성','보성이미지.png'),
    ('jeonnam','hwasun'): ('화순','화순이미지.png'),
    ('jeonnam','jangheung'): ('장흥','장흥이미지.png'),
    ('jeonnam','gangjin'): ('강진','강진이미지.png'),
    ('jeonnam','yeongam'): ('영암','영암이미지.png'),
    ('jeonnam','muan'): ('무안','무안이미지.png'),
    ('jeonnam','hampyeong'): ('함평','함평이미지.png'),
    ('jeonnam','yeonggwang'): ('영광','영광이미지.png'),
    ('jeonnam','jangseong'): ('장성','장성이미지.png'),
    ('jeonbuk','gochang'): ('고창','고창지역 이미지.png'),
    ('jeonbuk','jeongeup'): ('정읍','정읍지역 이미지.png'),
    ('jeonbuk','namwon'): ('남원','남원이미지.png'),
    ('jeonbuk','sunchang'): ('순창','순창지역 이미지.png'),
}

for (province, slug), (name, image_name) in MAP.items():
    page = ROOT / 'region' / province / slug / 'index.html'
    image = ROOT / 'assets' / 'img' / image_name
    if not page.exists():
        raise SystemExit(f'MISSING PAGE: {page.relative_to(ROOT)}')
    if not image.exists():
        raise SystemExit(f'MISSING IMAGE: {image.relative_to(ROOT)}')
    html = page.read_text(encoding='utf-8')
    if '/assets/thejeongmil-region-hero.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/thejeongmil-region-hero.css"></head>', 1)
    hero = (
        f'<aside class="v4-region-visual v4-region-poster" aria-label="{name} 더정밀누수하수구 대표이미지">'
        f'<img src="/assets/img/{image_name}" alt="{name} 하수구막힘 누수탐지 더정밀누수하수구 대표이미지" '
        f'loading="eager" fetchpriority="high" decoding="async"></aside>'
    )
    html, n = re.subn(r'<aside class="v4-region-visual"[^>]*>.*?</aside>', hero, html, count=1, flags=re.S)
    if n == 0:
        html, n = re.subn(r'<aside class="v4-region-visual v4-region-poster"[^>]*>.*?</aside>', hero, html, count=1, flags=re.S)
    if n == 0:
        raise SystemExit(f'HERO NOT FOUND: {page.relative_to(ROOT)}')
    # Remove any lingering direct portrait reference from this page.
    html = html.replace('/assets/img/friend-real-portrait.webp', f'/assets/img/{image_name}')
    # Give social/search previews the same regional representative image.
    og = f'<meta property="og:image" content="https://ezm.co.kr/assets/img/{image_name}">'
    if 'property="og:image"' in html:
        html = re.sub(r'<meta property="og:image"[^>]*>', og, html, count=1)
    else:
        html = html.replace('</head>', og + '</head>', 1)
    page.write_text(html, encoding='utf-8')
    print('CONNECTED', page.relative_to(ROOT), '->', image_name)

(ROOT / 'DEPLOY-VERSION.txt').write_text('THEJEONGMIL-V1.7-REGION-HERO-IMAGES\n', encoding='utf-8')
print('TOTAL', len(MAP))
