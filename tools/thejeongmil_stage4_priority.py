from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
PHONE='010-5758-3820'; TEL='01057583820'
DATA={
('jeonbuk','gochang'):('고창','고창읍·고수면·아산면·무장면·공음면·상하면·해리면·성송면·대산면·심원면·흥덕면·성내면·신림면·부안면','주택·상가·농촌형 건물의 하수구막힘, 오수관 역류와 수도·온수배관 누수 상담','고창하수구막힘 · 고창싱크대막힘 · 고창오수관막힘 · 고창누수 · 고창누수탐지 · 고창천장누수'),
('jeonbuk','jeongeup'):('정읍','수성동·장명동·내장상동·시기동·초산동·연지동·농소동·상교동·신태인읍','아파트·주택·상가의 싱크대·배수구·오수관 문제와 천장·수도배관 누수 상담','정읍하수구막힘 · 정읍싱크대막힘 · 정읍배수구막힘 · 정읍누수 · 정읍누수탐지 · 정읍천장누수'),
('jeonbuk','namwon'):('남원','도통동·향교동·노암동·왕정동·동충동·죽항동·금동·월락동·인월면','아파트·주택·상가 배수불량과 반복막힘, 수도·온수·난방배관 누수 상담','남원하수구막힘 · 남원싱크대막힘 · 남원변기막힘 · 남원누수 · 남원누수탐지 · 남원난방누수'),
('jeonbuk','sunchang'):('순창','순창읍·인계면·동계면·적성면·유등면·풍산면·금과면·팔덕면·복흥면·쌍치면·구림면','주택·상가의 하수구·오수관 막힘과 수도·온수배관 누수 상담','순창하수구막힘 · 순창싱크대막힘 · 순창오수관막힘 · 순창누수 · 순창누수탐지 · 순창수도누수'),
('jeonnam','naju'):('나주','빛가람동·송월동·성북동·금남동·영산동·남평읍·노안면·산포면·왕곡면','혁신도시 아파트·상가와 공장·사업장의 싱크대·오수관·맨홀 역류, 배관누수 상담','나주하수구막힘 · 나주싱크대막힘 · 나주오수관막힘 · 나주맨홀역류 · 나주누수 · 나주누수탐지'),
('jeonnam','damyang'):('담양','담양읍·수북면·대전면·봉산면·고서면·가사문학면·창평면·대덕면·무정면·금성면·용면·월산면','주택·상가·공장 배관의 반복막힘, 기름 슬러지·오수관 문제와 누수 상담','담양하수구막힘 · 담양싱크대막힘 · 담양배수구막힘 · 담양고압세척 · 담양누수 · 담양누수탐지'),
('jeonnam','jangseong'):('장성','장성읍·진원면·남면·동화면·삼서면·삼계면·황룡면·서삼면·북일면·북이면·북하면','광주 인접 주택·상가·사업장의 하수구막힘과 수도·온수·난방배관 누수 상담','장성하수구막힘 · 장성싱크대막힘 · 장성오수관막힘 · 장성누수 · 장성누수탐지 · 장성천장누수'),
('jeonnam','hwasun'):('화순','화순읍·도곡면·도암면·능주면·춘양면·청풍면·이양면·한천면·동복면·사평면·동면','아파트·주택·음식점·상가의 반복 하수구막힘과 천장·온수배관 누수 상담','화순하수구막힘 · 화순싱크대막힘 · 화순배수구막힘 · 화순고압세척 · 화순누수 · 화순누수탐지')}

def section(name,areas,context,keys):
 return f'''<section class="v4-section v4-priority" id="local-intent"><div class="v4-shell"><span class="v4-kicker">LOCAL SERVICE</span><h2>{name} 생활권별 하수구·누수 상담</h2><p>{context}을 기준으로 증상을 확인합니다. 아래 지역명은 출장 상담 범위를 안내하기 위한 것이며 특정 지역의 시공사례를 의미하지 않습니다.</p><div class="v4-areas">{''.join('<span>'+x+'</span>' for x in areas.split('·'))}</div></div></section><section class="v4-section v4-soft"><div class="v4-shell"><span class="v4-kicker">CUSTOMER SEARCH</span><h2>{name} 고객이 증상에 따라 찾는 서비스</h2><p>{keys}</p><div class="v4-symgrid"><div><b>한 곳만 막힐 때</b><span>싱크대·변기·바닥배수구의 개별 배관부터 확인합니다.</span></div><div><b>여러 곳이 같이 역류할 때</b><span>공용배관·오수관·맨홀 방향까지 범위를 넓혀 확인합니다.</span></div><div><b>천장 물샘이 보일 때</b><span>피해 위치만 보고 단정하지 않고 냉수·온수·난방 계통을 구분합니다.</span></div><div><b>반복되는 문제일 때</b><span>단순 통수보다 내시경·관로 확인으로 재발 원인을 찾는 데 초점을 둡니다.</span></div></div><a class="v4-maincall" href="tel:{TEL}">{name} 전화상담 {PHONE}</a></div></section>'''

for (province,slug),vals in DATA.items():
 p=ROOT/'region'/province/slug/'index.html'
 if not p.exists(): continue
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'<section class="v4-section v4-priority".*?(?=<nav class="v4-bottom">)','',s,flags=re.S)
 s=s.replace('<nav class="v4-bottom">',section(*vals)+'<nav class="v4-bottom">',1)
 p.write_text(s,encoding='utf-8')
 print('PRIORITY',p.relative_to(ROOT))
(ROOT/'DEPLOY-VERSION.txt').write_text('THEJEONGMIL-V1.5-PRIORITY-REGIONS\n',encoding='utf-8')
