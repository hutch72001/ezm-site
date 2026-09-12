from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
TARGETS=[]
for slug in ['gwangsan','bukgu','seogu','namgu','donggu']:
    TARGETS.append(('gwangju',slug,ROOT/'region'/'gwangju'/slug/'index.html'))
for slug in ['mokpo','yeosu','suncheon','naju','gwangyang','damyang','gokseong','gurye','goheung','boseong','hwasun','jangheung','gangjin','haenam','yeongam','muan','hampyeong','yeonggwang','jangseong','wando','jindo','sinan']:
    TARGETS.append(('jeonnam',slug,ROOT/'region'/'jeonnam'/slug/'index.html'))
for slug in ['gochang','jeongeup','namwon','sunchang']:
    TARGETS.append(('jeonbuk',slug,ROOT/'region'/'jeonbuk'/slug/'index.html'))

NAMES={
'gwangsan':'광주 광산구','bukgu':'광주 북구','seogu':'광주 서구','namgu':'광주 남구','donggu':'광주 동구',
'mokpo':'목포','yeosu':'여수','suncheon':'순천','naju':'나주','gwangyang':'광양','damyang':'담양','gokseong':'곡성','gurye':'구례','goheung':'고흥','boseong':'보성','hwasun':'화순','jangheung':'장흥','gangjin':'강진','haenam':'해남','yeongam':'영암','muan':'무안','hampyeong':'함평','yeonggwang':'영광','jangseong':'장성','wando':'완도','jindo':'진도','sinan':'신안','gochang':'고창','jeongeup':'정읍','namwon':'남원','sunchang':'순창'}

def visual(name):
    return f'''<aside class="v4-region-visual" aria-label="{name} 더정밀누수하수구 상담 이미지"><div class="v4-region-scene"><div class="v4-region-copy"><span>{name} 출장상담</span><strong>하수구막힘 · 누수탐지</strong><small>아파트 · 주택 · 상가 · 공장</small></div><img src="/assets/img/friend-real-portrait.webp" alt="더정밀누수하수구 상담 담당자 실제 사진" loading="eager" fetchpriority="high"></div></aside>'''

for province,slug,p in TARGETS:
    if not p.exists(): continue
    name=NAMES[slug]
    s=p.read_text(encoding='utf-8')
    if 'v4-region-visual' in s: continue
    # hero shell only: split existing contents into copy + real-photo visual
    m=re.search(r'(<section class="v4-hero"><div class="v4-shell">)(.*?)(</div></section>)',s,re.S)
    if not m:
        print('SKIP HERO',p)
        continue
    new=m.group(1).replace('class="v4-shell"','class="v4-shell v4-hero-grid"')+'<div class="v4-hero-copy">'+m.group(2)+'</div>'+visual(name)+m.group(3)
    s=s[:m.start()]+new+s[m.end():]
    p.write_text(s,encoding='utf-8')
    print('HERO',p.relative_to(ROOT))

css=ROOT/'assets'/'style.css'
s=css.read_text(encoding='utf-8')
marker='/* THEJEONGMIL REAL PORTRAIT REGION HERO */'
if marker not in s:
    s+='''\n\n/* THEJEONGMIL REAL PORTRAIT REGION HERO */\n.v4-hero-grid{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(300px,.88fr);gap:34px;align-items:center}.v4-hero-copy{min-width:0}.v4-region-visual{align-self:stretch;min-height:520px}.v4-region-scene{height:100%;min-height:520px;position:relative;overflow:hidden;border-radius:28px;background:radial-gradient(circle at 65% 22%,#2970c7 0,#153967 40%,#071a34 100%);box-shadow:0 24px 60px #0005}.v4-region-scene:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 0,transparent 46%,#06172ed9 100%),radial-gradient(circle at 85% 15%,#52c7ff55,transparent 34%)}.v4-region-scene img{position:absolute;right:-2%;bottom:0;width:84%;height:92%;object-fit:cover;object-position:center 30%;border-radius:0;filter:saturate(.96) contrast(1.02)}.v4-region-copy{position:absolute;z-index:3;left:22px;right:22px;bottom:22px;padding:17px 18px;border-radius:18px;background:#06172ee8;border:1px solid #ffffff2e;backdrop-filter:blur(8px)}.v4-region-copy span,.v4-region-copy strong,.v4-region-copy small{display:block}.v4-region-copy span{color:#55ceff;font-size:14px;font-weight:900}.v4-region-copy strong{color:#fff;font-size:24px;line-height:1.25;margin:3px 0}.v4-region-copy small{color:#d6e4f5;font-size:14px}.v4-region-visual:after{content:"실제 인물 사진 · 지역명과 안내문구는 페이지별 자동 적용";display:block;color:#a9bad0;font-size:11px;text-align:center;margin-top:8px}@media(max-width:820px){.v4-hero-grid{grid-template-columns:1fr}.v4-region-visual{min-height:auto;margin-top:12px}.v4-region-scene{min-height:390px}.v4-region-scene img{width:76%;height:92%}}\n'''
    css.write_text(s,encoding='utf-8')
(ROOT/'DEPLOY-VERSION.txt').write_text('THEJEONGMIL-V1.6-REAL-PORTRAIT-HERO\n',encoding='utf-8')
