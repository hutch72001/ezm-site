from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGETS = []

# 광주 5구
for slug in ["gwangsan","bukgu","seogu","namgu","donggu"]:
    TARGETS.append(ROOT / "region" / "gwangju" / slug / "index.html")

# 전남 22개 시군
for slug in ["mokpo","yeosu","suncheon","naju","gwangyang","damyang","gokseong","gurye","goheung","boseong","hwasun","jangheung","gangjin","haenam","yeongam","muan","hampyeong","yeonggwang","jangseong","wando","jindo","sinan"]:
    TARGETS.append(ROOT / "region" / "jeonnam" / slug / "index.html")

# 전북 실제 영업권 4개 지역만
for slug in ["gochang","jeongeup","namwon","sunchang"]:
    TARGETS.append(ROOT / "region" / "jeonbuk" / slug / "index.html")

OLD_PHONE = "010-4833-3447"
NEW_PHONE = "010-5758-3820"
OLD_TEL = "01048333447"
NEW_TEL = "01057583820"

for path in TARGETS:
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

    # 상단 공통 문구는 친구 영업권 기준으로 통일
    s = re.sub(r'<div class="top"><div class="wrap"><span>.*?</span><a class="phone"',
               '<div class="top"><div class="wrap"><span>고창·정읍·남원·순창 · 광주·전남 전지역</span><a class="phone"',
               s, count=1, flags=re.S)

    # footer 브랜드가 남아 있으면 정리
    s = s.replace("서비스 문의: 더정밀누수하수구 · ", "상담 · ")
    s = s.replace("현장자료 제공·서비스 문의: 더정밀누수하수구 · ", "상담 · ")

    path.write_text(s, encoding="utf-8")
    print(f"UPDATED {path.relative_to(ROOT)}")

# 버전 파일
(ROOT / "DEPLOY-VERSION.txt").write_text("THEJEONGMIL-V1.2-REGION-CONVERSION\n", encoding="utf-8")
