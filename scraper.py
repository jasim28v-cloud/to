import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_premium_grid_scraper():
    rss_url = "https://arabic.rt.com/rss/sport/"
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. جلب المباريات
        match_res = requests.get(matches_url, headers=headers, timeout=15)
        match_res.encoding = 'utf-8'
        match_soup = BeautifulSoup(match_res.content, 'lxml')
        matches_html = ""
        for league in match_soup.find_all('div', class_='matchCard')[:3]:
            for m in league.find_all('div', class_='allMatchesList')[:1]:
                t1 = m.find('div', class_='teamA').text.strip()
                t2 = m.find('div', class_='teamB').text.strip()
                res = m.find('div', class_='MResult').find_all('span')
                score = f"{res[0].text}-{res[1].text}" if len(res) > 1 else "VS"
                matches_html += f'''
                <div class="m-card">
                    <div class="m-team">{t1}</div>
                    <div class="m-score">{score}</div>
                    <div class="m-team">{t2}</div>
                </div>'''

        # 2. جلب الأخبار (صور حقيقية فقط + تأثيرات حديثة)
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else None
            if not img: continue # عرض الصور الحقيقية فقط
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-overlay"></div>
                        <div class="n-badge">حداثة</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span>🕒 {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-more">التفاصيل</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. الواجهة الحديثة (Vortex Next-Gen)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | الحداثة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #05070a; --card: #11141b; --gold: #d4af37; --text: #f0f0f0; --glass: rgba(255, 255, 255, 0.03); }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding: 0; }}
        
        header {{ background: rgba(17, 20, 27, 0.8); backdrop-filter: blur(10px); padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 1px solid var(--glass); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; letter-spacing: -1px; }}
        .logo span {{ color: var(--gold); }}

        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}

        /* شريط المباريات بشكل أحدث */
        .match-scroller {{ display: flex; gap: 15px; overflow-x: auto; padding-bottom: 20px; scrollbar-width: none; }}
        .m-card {{ background: var(--card); min-width: 190px; padding: 15px; border-radius: 16px; border: 1px solid var(--glass); text-align: center; transition: 0.3s; }}
        .m-card:hover {{ border-color: var(--gold); background: #1a1e26; }}
        .m-team {{ font-size: 13px; font-weight: 700; margin-bottom: 8px; }}
        .m-score {{ background: var(--gold); color: #000; font-weight: 900; padding: 3px 12px; border-radius: 6px; font-size: 15px; }}

        /* شبكة الأخبار بتأثيرات بصرية */
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 25px; }}
        .n-card {{ background: var(--card); border-radius: 20px; overflow: hidden; border: 1px solid var(--glass); transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); }}
        .n-card:hover {{ transform: scale(1.03); border-color: rgba(212, 175, 55, 0.5); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        
        .n-img {{ position: relative; height: 190px; overflow: hidden; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.6s; }}
        .n-card:hover .n-img img {{ transform: scale(1.1) rotate(1deg); }}
        .n-overlay {{ position: absolute; bottom: 0; left: 0; width: 100%; height: 50%; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); }}
        .n-badge {{ position: absolute; top: 12px; right: 12px; background: rgba(212, 175, 55, 0.9); color: #000; font-size: 10px; font-weight: 900; padding: 4px 12px; border-radius: 8px; backdrop-filter: blur(5px); }}
        
        .n-info {{ padding: 20px; }}
        .n-info h3 {{ font-size: 16px; margin: 0 0 15px 0; line-height: 1.5; font-weight: 700; color: #fff; height: 48px; overflow: hidden; }}
        .n-footer {{ display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #888; }}
        .n-more {{ color: var(--gold); font-weight: bold; text-transform: uppercase; border-bottom: 1px solid transparent; transition: 0.3s; }}
        .n-card:hover .n-more {{ border-color: var(--gold); }}

        .ad-slot {{ display: flex; justify-content: center; margin: 30px 0; border-radius: 15px; overflow: hidden; }}

        footer {{ background: #000; padding: 60px 20px; text-align: center; border-top: 1px solid var(--glass); margin-top: 60px; }}
        .footer-logo {{ font-size: 30px; font-weight: 900; color: #fff; margin-bottom: 10px; }}
        
        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
            .n-img {{ height: 230px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX<span>NEXT</span></a>
        <div style="color: #00ff88; font-size: 12px; font-weight: bold; letter-spacing: 1px;">● LIVE UPDATE</div>
    </header>

    <div class="container">
        <div class="ad-slot">
            <ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>
        </div>

        <div class="match-scroller">
            {matches_html}
        </div>

        <h2 style="font-size: 22px; font-weight: 900; margin-bottom: 30px; display: flex; align-items: center; gap: 10px;">
            <span style="width: 4px; height: 25px; background: var(--gold); display: inline-block; border-radius: 10px;"></span>
            أحدث التقارير
        </h2>
        
        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="ad-slot">
            <script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>
        </div>
    </div>

    <footer>
        <div class="footer-logo">VORTEX <span>2026</span></div>
        <p style="color: #555; max-width: 500px; margin: 0 auto; line-height: 1.8;">تجربة رياضية حديثة تعتمد على الذكاء الاصطناعي في جلب وتنسيق المحتوى الرياضي العالمي.</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_premium_grid_scraper()
