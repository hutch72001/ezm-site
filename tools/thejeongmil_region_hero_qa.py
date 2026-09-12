from pathlib import Path
import re, json

ROOT=Path(__file__).resolve().parents[1]
MAP={
'region/gwangju/gwangsan/index.html':'광산구이미지.png','region/gwangju/bukgu/index.html':'북구이미지.png','region/gwangju/seogu/index.html':'서구이미지.png','region/gwangju/namgu/index.html':'남구이미지.png','region/gwangju/donggu/index.html':'동구이미지.png',
'region/jeonnam/mokpo/index.html':'목포이미지.png','region/jeonnam/yeosu/index.html':'여수지역 이미지.png','region/jeonnam/suncheon/index.html':'순천지역 이미지.png','region/jeonnam/naju/index.html':'나주지역 이미지.png','region/jeonnam/gwangyang/index.html':'광양지역 이미지 주황.png','region/jeonnam/damyang/index.html':'담양이미지.png','region/jeonnam/gokseong/index.html':'곡성이미지.png','region/jeonnam/gurye/index.html':'구례이미지.png','region/jeonnam/goheung/index.html':'고흥이미지.png','region/jeonnam/boseong/index.html':'보성이미지.png','region/jeonnam/hwasun/index.html':'화순이미지.png','region/jeonnam/jangheung/index.html':'장흥이미지.png','region/jeonnam/gangjin/index.html':'강진이미지.png','region/jeonnam/yeongam/index.html':'영암이미지.png','region/jeonnam/muan/index.html':'무안이미지.png','region/jeonnam/hampyeong/index.html':'함평이미지.png','region/jeonnam/yeonggwang/index.html':'영광이미지.png','region/jeonnam/jangseong/index.html':'장성이미지.png',
'region/jeonbuk/gochang/index.html':'고창지역 이미지.png','region/jeonbuk/jeongeup/index.html':'정읍지역 이미지.png','region/jeonbuk/namwon/index.html':'남원이미지.png','region/jeonbuk/sunchang/index.html':'순창지역 이미지.png'}

def fail(lst, page, issue): lst.append({'page':page,'issue':issue})
issues=[]; passed=[]
for rel,img in MAP.items():
 p=ROOT/rel; ip=ROOT/'assets/img'/img
 if not p.exists(): fail(issues,rel,'HTML missing'); continue
 if not ip.exists(): fail(issues,rel,f'image missing: {img}')
 s=p.read_text(encoding='utf-8')
 expected='/assets/img/'+img
 if expected not in s: fail(issues,rel,'hero image path mismatch')
 if 'v4-region-poster' not in s: fail(issues,rel,'hero poster class missing')
 if 'friend-real-portrait.webp' in s: fail(issues,rel,'old selfie hero reference remains')
 if '<meta property="og:image"' not in s or img not in s.split('<meta property="og:image"',1)[1].split('>',1)[0]: fail(issues,rel,'og:image missing or mismatched')
 m=re.search(r'<img src="'+re.escape(expected)+r'" alt="([^"]+)"',s)
 if not m: fail(issues,rel,'representative image alt missing')
 elif '대표이미지' not in m.group(1): fail(issues,rel,'representative image alt not descriptive')
 if '<link rel="stylesheet" href="/assets/thejeongmil-region-hero.css">' not in s: fail(issues,rel,'regional hero CSS link missing')
 if not any(x['page']==rel for x in issues): passed.append(rel)
css=(ROOT/'assets/thejeongmil-region-hero.css').read_text(encoding='utf-8') if (ROOT/'assets/thejeongmil-region-hero.css').exists() else ''
for required in ['object-fit:contain','aspect-ratio:1/1','@media (max-width:899px)','overflow-wrap:anywhere']:
 if required not in css: fail(issues,'assets/thejeongmil-region-hero.css',f'CSS QA rule missing: {required}')
report={'target_pages':len(MAP),'passed_pages':len(passed),'issue_count':len(issues),'issues':issues}
(ROOT/'REGION-HERO-QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 더정밀 지역 대표이미지 QA','',f'- 대상 페이지: {len(MAP)}',f'- PASS: {len(passed)}',f'- 이슈: {len(issues)}','']
if issues:
 md+=['## 이슈']+[f"- `{x['page']}` — {x['issue']}" for x in issues]
else: md+=['## 결과','- 지역별 대표이미지 경로, OG 이미지, alt, 셀카 Hero 제거, 모바일 contain 규칙 모두 PASS']
(ROOT/'REGION-HERO-QA.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
if issues: raise SystemExit(1)
