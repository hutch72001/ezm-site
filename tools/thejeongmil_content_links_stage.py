from pathlib import Path
import re, json, html
ROOT=Path(__file__).resolve().parents[1]
REGIONS={
'region/gwangju/gwangsan/index.html':('광주 광산구','gwangju','도심·산단 혼합',['region/gwangju/seogu/','region/jeonnam/naju/','region/jeonnam/jangseong/']),
'region/gwangju/bukgu/index.html':('광주 북구','gwangju','아파트·주택 혼합',['region/gwangju/donggu/','region/gwangju/seogu/','region/jeonnam/damyang/']),
'region/gwangju/seogu/index.html':('광주 서구','gwangju','아파트·상가 밀집',['region/gwangju/bukgu/','region/gwangju/namgu/','region/gwangju/gwangsan/']),
'region/gwangju/namgu/index.html':('광주 남구','gwangju','주거·상가 혼합',['region/gwangju/seogu/','region/gwangju/donggu/','region/jeonnam/hwasun/']),
'region/gwangju/donggu/index.html':('광주 동구','gwangju','도심·상가·주거 혼합',['region/gwangju/bukgu/','region/gwangju/namgu/','region/jeonnam/hwasun/']),
'region/jeonnam/mokpo/index.html':('목포','jeonnam','도심·상가·공동주택',['region/jeonnam/muan/','region/jeonnam/yeongam/']),
'region/jeonnam/yeosu/index.html':('여수','jeonnam','도심·상가·산업시설',['region/jeonnam/suncheon/','region/jeonnam/gwangyang/']),
'region/jeonnam/suncheon/index.html':('순천','jeonnam','도심·공동주택·사업장',['region/jeonnam/yeosu/','region/jeonnam/gwangyang/','region/jeonnam/gurye/']),
'region/jeonnam/naju/index.html':('나주','jeonnam','혁신도시·공장·주택',['region/gwangju/gwangsan/','region/jeonnam/hwasun/','region/jeonnam/yeongam/']),
'region/jeonnam/gwangyang/index.html':('광양','jeonnam','공동주택·상가·산업시설',['region/jeonnam/suncheon/','region/jeonnam/yeosu/']),
'region/jeonnam/damyang/index.html':('담양','jeonnam','주택·상가·공장',['region/gwangju/bukgu/','region/jeonnam/jangseong/','region/jeonnam/gokseong/']),
'region/jeonnam/gokseong/index.html':('곡성','jeonnam','주택·상가·농촌시설',['region/jeonnam/damyang/','region/jeonnam/gurye/']),
'region/jeonnam/gurye/index.html':('구례','jeonnam','주택·상가·숙박시설',['region/jeonnam/gokseong/','region/jeonnam/suncheon/']),
'region/jeonnam/goheung/index.html':('고흥','jeonnam','주택·상가·농어촌시설',['region/jeonnam/boseong/','region/jeonnam/suncheon/']),
'region/jeonnam/boseong/index.html':('보성','jeonnam','주택·상가·농촌시설',['region/jeonnam/goheung/','region/jeonnam/jangheung/']),
'region/jeonnam/hwasun/index.html':('화순','jeonnam','아파트·주택·상가',['region/gwangju/namgu/','region/gwangju/donggu/','region/jeonnam/naju/']),
'region/jeonnam/jangheung/index.html':('장흥','jeonnam','주택·상가·농어촌시설',['region/jeonnam/boseong/','region/jeonnam/gangjin/']),
'region/jeonnam/gangjin/index.html':('강진','jeonnam','주택·상가·농어촌시설',['region/jeonnam/jangheung/','region/jeonnam/yeongam/']),
'region/jeonnam/yeongam/index.html':('영암','jeonnam','주택·상가·산업시설',['region/jeonnam/mokpo/','region/jeonnam/muan/','region/jeonnam/naju/']),
'region/jeonnam/muan/index.html':('무안','jeonnam','공동주택·주택·상가',['region/jeonnam/mokpo/','region/jeonnam/yeongam/','region/jeonnam/hampyeong/']),
'region/jeonnam/hampyeong/index.html':('함평','jeonnam','주택·상가·농촌시설',['region/jeonnam/muan/','region/jeonnam/yeonggwang/']),
'region/jeonnam/yeonggwang/index.html':('영광','jeonnam','주택·상가·산업시설',['region/jeonnam/hampyeong/','region/jeonnam/jangseong/','region/jeonbuk/gochang/']),
'region/jeonnam/jangseong/index.html':('장성','jeonnam','주택·상가·산업시설',['region/gwangju/gwangsan/','region/jeonnam/damyang/','region/jeonnam/yeonggwang/']),
'region/jeonbuk/gochang/index.html':('고창','jeonbuk','주택·상가·농촌시설',['region/jeonbuk/jeongeup/','region/jeonnam/yeonggwang/']),
'region/jeonbuk/jeongeup/index.html':('정읍','jeonbuk','도심·주택·상가',['region/jeonbuk/gochang/','region/jeonbuk/sunchang/']),
'region/jeonbuk/namwon/index.html':('남원','jeonbuk','도심·주택·상가',['region/jeonbuk/sunchang/','region/jeonnam/gurye/']),
'region/jeonbuk/sunchang/index.html':('순창','jeonbuk','주택·상가·농촌시설',['region/jeonbuk/namwon/','region/jeonbuk/jeongeup/','region/jeonnam/damyang/'])}

def label(path):
 slug=path.strip('/').split('/')[-1]
 names={'gwangsan':'광주 광산구','bukgu':'광주 북구','seogu':'광주 서구','namgu':'광주 남구','donggu':'광주 동구','mokpo':'목포','yeosu':'여수','suncheon':'순천','naju':'나주','gwangyang':'광양','damyang':'담양','gokseong':'곡성','gurye':'구례','goheung':'고흥','boseong':'보성','hwasun':'화순','jangheung':'장흥','gangjin':'강진','yeongam':'영암','muan':'무안','hampyeong':'함평','yeonggwang':'영광','jangseong':'장성','gochang':'고창','jeongeup':'정읍','namwon':'남원','sunchang':'순창'}
 return names.get(slug,slug)

def section(region, province, profile, neighbors):
 short=region.replace('광주 ','') if region.startswith('광주 ') else region
 neighbor_links=''.join(f'<a href="/{p}">{label(p)}</a>' for p in neighbors)
 q1=f'{short}에서 싱크대나 배수구가 반복해서 막히면 어떤 점을 먼저 확인하나요?'
 a1='한 곳만 느린지 여러 배수구가 함께 역류하는지 확인한 뒤 가지배관과 메인관로를 구분합니다. 반복막힘은 단순 통수보다 배관내시경·관로 확인으로 원인 범위를 좁히는 방식이 적합합니다.'
 q2=f'{short} 누수탐지는 바로 바닥을 철거하나요?'
 a2='피해 위치만 보고 바로 철거하지 않고 냉수·온수·난방 계통을 구분한 뒤 압력검사와 가스·청음·열화상 등 필요한 검사를 조합합니다. 보수한 경우에는 2차 압력검사로 결과를 다시 확인합니다.'
 q3=f'{short}의 {profile}에서 하수구 역류가 생기면 고압세척이 항상 필요한가요?'
 a3='막힘 위치와 원인에 따라 장비 선택이 달라집니다. 석션·플렉스샤프트·고압세척 중 필요한 작업을 판단하고 작업 후 통수와 내부 상태를 다시 확인하는 것이 중요합니다.'
 q4='전화 상담 전에 알려주면 진단에 도움이 되는 내용은 무엇인가요?'
 a4='막힘 또는 물샘이 시작된 시점, 한 곳인지 여러 곳인지, 이전 작업 여부, 천장·벽·바닥 중 피해 위치, 보일러 압력이나 계량기 변화 여부를 알려주면 초기 판단에 도움이 됩니다.'
 return f'''<section class="v4-section v4-content-links" id="faq-local"><div class="v4-shell"><span class="v4-kicker">LOCAL GUIDE</span><h2>{region} 하수구·누수, 증상별 확인 포인트</h2><p class="v4-desc">{profile}이 함께 있는 생활권에서는 같은 역류나 물샘이라도 문제 구간이 다를 수 있습니다. 증상 범위를 먼저 나누고 필요한 검사와 작업을 연결해 과도한 작업을 피하는 방향으로 판단합니다.</p><div class="v4-linkcards"><a href="/drain/"><b>하수구막힘 진단 안내</b><span>싱크대·변기·배수구·오수관·맨홀 역류</span></a><a href="/leak/"><b>누수탐지 진단 안내</b><span>천장 물샘·수도·온수·난방배관 누수</span></a><a href="/region/{province}/"><b>출장지역 전체 보기</b><span>{'광주' if province=='gwangju' else '전남' if province=='jeonnam' else '전북'} 지역 페이지 연결</span></a></div><div class="v4-faq"><details><summary>{q1}</summary><p>{a1}</p></details><details><summary>{q2}</summary><p>{a2}</p></details><details><summary>{q3}</summary><p>{a3}</p></details><details><summary>{q4}</summary><p>{a4}</p></details></div><h3 class="v4-neighbor-title">인접 지역 서비스 안내</h3><div class="v4-neighbor-links">{neighbor_links}</div></div></section>'''

def schema(region, profile):
 short=region.replace('광주 ','') if region.startswith('광주 ') else region
 qs=[
 (f'{short}에서 싱크대나 배수구가 반복해서 막히면 어떤 점을 먼저 확인하나요?','한 곳만 느린지 여러 배수구가 함께 역류하는지 확인한 뒤 가지배관과 메인관로를 구분합니다. 반복막힘은 배관내시경·관로 확인으로 원인 범위를 좁힙니다.'),
 (f'{short} 누수탐지는 바로 바닥을 철거하나요?','피해 위치만 보고 바로 철거하지 않고 배관 계통을 구분한 뒤 압력검사와 필요한 탐지 검사를 조합합니다. 보수 후에는 2차 압력검사로 확인합니다.'),
 (f'{short}의 {profile}에서 하수구 역류가 생기면 고압세척이 항상 필요한가요?','막힘 위치와 원인에 따라 석션·플렉스샤프트·고압세척 등 필요한 장비를 선택합니다.'),
 ('전화 상담 전에 알려주면 진단에 도움이 되는 내용은 무엇인가요?','증상 시작 시점, 한 곳인지 여러 곳인지, 이전 작업 여부, 피해 위치, 보일러 압력이나 계량기 변화 여부가 도움이 됩니다.')]
 data={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in qs]}
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'</script>'

changed=[]
for rel,(region,province,profile,neighbors) in REGIONS.items():
 p=ROOT/rel
 if not p.exists(): continue
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'<section class="v4-section v4-content-links" id="faq-local">.*?</section>','',s,flags=re.S)
 s=re.sub(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"FAQPage".*?</script>','',s,flags=re.S)
 ins=section(region,province,profile,neighbors)+schema(region,profile)
 if '<nav class="v4-bottom">' in s:
  s=s.replace('<nav class="v4-bottom">',ins+'<nav class="v4-bottom">',1)
 else:
  s=s.replace('</body>',ins+'</body>',1)
 p.write_text(s,encoding='utf-8'); changed.append(rel)

cssp=ROOT/'assets/thejeongmil-region-hero.css'
css=cssp.read_text(encoding='utf-8')
addon='''\n/* regional content + internal link stage */\n.v4-linkcards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:26px 0}.v4-linkcards a{display:block;text-decoration:none;border:1px solid #dce4ee;background:#fff;border-radius:18px;padding:20px}.v4-linkcards b{display:block;font-size:18px;margin-bottom:6px}.v4-linkcards span{color:#667085;font-size:14px}.v4-neighbor-title{font-size:22px;margin:30px 0 12px}.v4-neighbor-links{display:flex;flex-wrap:wrap;gap:10px}.v4-neighbor-links a{display:inline-block;text-decoration:none;border:1px solid #dce4ee;background:#fff;border-radius:999px;padding:9px 13px;font-weight:800;color:#1769aa}@media(max-width:700px){.v4-linkcards{grid-template-columns:1fr}.v4-content-links .v4-faq details{padding:16px}.v4-neighbor-links a{font-size:14px}}\n'''
if 'regional content + internal link stage' not in css:
 cssp.write_text(css+addon,encoding='utf-8')
(ROOT/'CONTENT-LINK-STAGE-REPORT.json').write_text(json.dumps({'changed_pages':len(changed),'pages':changed},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'updated {len(changed)} regional pages')
