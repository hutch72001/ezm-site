from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = []

# 광주 5구
for slug in ["gwangsan","bukgu","seogu","namgu","donggu"]:
    TARGETS.append((slug, ROOT / "region" / "gwangju" / slug / "index.html"))

# 전남 22개 시군
for slug in ["mokpo","yeosu","suncheon","naju","gwangyang","damyang","gokseong","gurye","goheung","boseong","hwasun","jangheung","gangjin","haenam","yeongam","muan","hampyeong","yeonggwang","jangseong","wando","jindo","sinan"]:
    TARGETS.append((slug, ROOT / "region" / "jeonnam" / slug / "index.html"))

# 전북 실제 영업권 4개 지역만
for slug in ["gochang","jeongeup","namwon","sunchang"]:
    TARGETS.append((slug, ROOT / "region" / "jeonbuk" / slug / "index.html"))

OLD_PHONE = "010-4833-3447"
NEW_PHONE = "010-5758-3820"
OLD_TEL = "01048333447"
NEW_TEL = "01057583820"

DRAWER = ('<nav id="v4drawer" class="v4-drawer" hidden>'
          '<a href="/">홈</a><a href="/drain/">하수구막힘</a><a href="/leak/">누수탐지</a>'
          '<a href="/region/">출장지역</a><a href="tel:01057583820">전화상담 010-5758-3820</a></nav>')


def neutralize_img_alt(match, slug):
    src, alt = match.group(1), match.group(2)
    name = src.rsplit('/', 1)[-1].lower()
    # 해당 지역에서 검증된 자체 파일명은 기존 지역 alt 유지
    if name.startswith(slug + '-'):
        return match.group(0)
    if 'leak' in name:
        neutral = '누수탐지 실제 작업 장면'
    elif 'drain' in name or 'sewer' in name or 'highpressure' in name:
        neutral = '하수구막힘 실제 작업 장면'
    else:
        neutral = '배관 점검 실제 작업 장면'
    return f'<img src="{src}" alt="{neutral}"'


for slug, path in TARGETS:
    if not path.exists():
        print(f"SKIP missing: {path.relative_to(ROOT)}")
        continue
    s = path.read_text(encoding="utf-8")

    # 브랜드/전화번호 전환
    s = s.replace("배관현장연구소", "더정밀누수하수구")
    s = s.replace("배관<b>현장연구소</b>", "더정밀<b>누수하수구</b>")
    s = s.replace(OLD_PHONE, NEW_PHONE).replace(OLD_TEL, NEW_TEL)

    # 슈퍼맨 운영업체/외부링크 흔적 제거
    s = re.sub(r'<p>[^<]*슈퍼맨하수구누수[^<]*(?:<a[^>]*>.*?</a>)?[^<]*</p>', '', s)
    s = re.sub(r'<a[^>]+href="https://supermandrain\.co\.kr[^"]*"[^>]*>.*?</a>', '', s)

    # 슈퍼맨 외부 이미지 hotlink 제거: 친구 사이트 내부 실제 작업 참고이미지로 교체
    def replace_external_img(m):
        url = m.group(1)
        alt = m.group(2)
        low = url.lower()
        if 'leak' in low:
            src = '/assets/img/leak-acoustic.webp'
            nalt = '누수탐지 실제 작업 장면'
        else:
            src = '/assets/img/hwasun-drain-1.webp'
            nalt = '하수구막힘 실제 작업 장면'
        return f'<img src="{src}" alt="{nalt}"'
    s = re.sub(r'<img src="(https://supermandrain\.co\.kr/[^"]+)" alt="([^"]*)"', replace_external_img, s)

    # 공유 이미지에 실제 촬영지역이 아닌 지역명을 붙이지 않도록 alt 중립화
    s = re.sub(r'<img src="(/assets/img/[^"]+)" alt="([^"]*)"', lambda m: neutralize_img_alt(m, slug), s)

    # 상단 공통 문구는 친구 영업권 기준으로 통일
    s = re.sub(r'<div class="top"><div class="wrap"><span>.*?</span><a class="phone"',
               '<div class="top"><div class="wrap"><span>고창·정읍·남원·순창 · 광주·전남 전지역</span><a class="phone"',
               s, count=1, flags=re.S)

    # V4 햄버거 메뉴 실제 동작
    s = s.replace('<button class="v4-menu">☰</button>',
                  '<button class="v4-menu" type="button" aria-label="메뉴 열기" aria-controls="v4drawer" aria-expanded="false" onclick="const d=document.getElementById(\'v4drawer\');d.hidden=!d.hidden;this.setAttribute(\'aria-expanded\',String(!d.hidden))">☰</button>')
    if 'class="v4-head"' in s and 'id="v4drawer"' not in s:
        s = s.replace('</header>', '</header>' + DRAWER, 1)

    # footer 브랜드가 남아 있으면 정리
    s = s.replace("서비스 문의: 더정밀누수하수구 · ", "상담 · ")
    s = s.replace("현장자료 제공·서비스 문의: 더정밀누수하수구 · ", "상담 · ")

    path.write_text(s, encoding="utf-8")
    print(f"UPDATED {path.relative_to(ROOT)}")

# 버전 파일
(ROOT / "DEPLOY-VERSION.txt").write_text("THEJEONGMIL-V1.3-REGION-QA\n", encoding="utf-8")
