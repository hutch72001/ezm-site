from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
PHONE='010-5758-3820'; TEL='01057583820'
REGIONS={
'gwangju':{'gwangsan':'광산구','bukgu':'북구','seogu':'서구','namgu':'남구','donggu':'동구'},
'jeonnam':{'mokpo':'목포','yeosu':'여수','suncheon':'순천','naju':'나주','gwangyang':'광양','damyang':'담양','gokseong':'곡성','gurye':'구례','goheung':'고흥','boseong':'보성','hwasun':'화순','jangheung':'장흥','gangjin':'강진','haenam':'해남','yeongam':'영암','muan':'무안','hampyeong':'함평','yeonggwang':'영광','jangseong':'장성','wando':'완도','jindo':'진도','sinan':'신안'},
'jeonbuk':{'gochang':'고창','jeongeup':'정읍','namwon':'남원','sunchang':'순창'}}
KEYS={
'gwangju':'싱크대막힘 · 변기막힘 · 배수구막힘 · 하수구냄새 · 천장누수 · 수도배관누수',
'jeonnam':'하수구막힘 · 오수관막힘 · 맨홀역류 · 고압세척 · 천장누수 · 누수탐지',
'jeonbuk':'하수구막힘 · 싱크대막힘 · 오수관막힘 · 배관내시경 · 천장누수 · 난방배관누수'}

def block(name, province):
    keys=KEYS[province]
    return f'''<section class="v4-section v4-stage3" id="field-guide"><div class="v4-shell"><span class="v4-kicker">FIELD DIAGNOSIS</span><h2>{name} 배관 증상, 작업보다 진단이 먼저입니다</h2><p>{name}에서 하수구막힘이나 누수가 발생하면 같은 증상처럼 보여도 원인은 다를 수 있습니다. 한 곳만 막히는지, 여러 배수구가 동시에 역류하는지, 천장 물샘과 계량기 움직임이 함께 있는지부터 확인해 작업 범위를 판단합니다.</p><div class="v4-symgrid"><div><b>싱크대·배수구가 느려요</b><span>가지배관 막힘과 기름 슬러지 여부를 확인합니다.</span></div><div><b>변기·맨홀이 함께 역류해요</b><span>오수관·메인관로 범위를 확인합니다.</span></div><div><b>천장·벽에서 물이 보여요</b><span>냉수·온수 계통을 압력검사로 구분합니다.</span></div><div><b>보일러 압력이 떨어져요</b><span>난방배관 이상 여부를 확인한 뒤 탐지 범위를 좁힙니다.</span></div></div></div></section>
<section class="v4-section v4-soft"><div class="v4-shell"><span class="v4-kicker">SEARCH GUIDE</span><h2>{name}에서 많이 찾는 배관 문제</h2><p>{keys}</p><p>단순히 지역명만 바꾼 설명이 아니라 증상 → 의심 구간 → 필요한 검사 → 작업 후 검증 순서로 안내합니다.</p></div></section>
<section class="v4-section"><div class="v4-shell"><span class="v4-kicker">WORK FLOW</span><h2>현장 판단 기준</h2><div class="v4-symgrid"><div><b>하수구</b><span>관로·내시경 확인 → 석션·플렉스샤프트·고압세척 등 원인에 맞는 작업 → 최종 통수·내부 확인</span></div><div><b>누수</b><span>압력검사 → 가스·청음·열화상 교차확인 → 필요한 구간만 개방·보수 → 보수 후 2차 압력검사</span></div></div><a class="v4-maincall" href="tel:{TEL}">{name} 증상 상담 {PHONE}</a></div></section>'''

for province,items in REGIONS.items():
    for slug,name in items.items():
        p=ROOT/'region'/province/slug/'index.html'
        if not p.exists(): continue
        s=p.read_text(encoding='utf-8')
        s=re.sub(r'<section class="v4-section v4-stage3".*?(?=<nav class="v4-bottom">)', '', s, flags=re.S)
        insert=block(name,province)
        s=s.replace('<nav class="v4-bottom">',insert+'<nav class="v4-bottom">',1)
        p.write_text(s,encoding='utf-8')
        print('ENRICHED',p.relative_to(ROOT))
(ROOT/'DEPLOY-VERSION.txt').write_text('THEJEONGMIL-V1.4-STAGE3-LANDING\n',encoding='utf-8')
