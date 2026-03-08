import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_premium_grid_scraper():
    # مصدر الأخبار (RT رياضة)
    rss_url = "https://arabic.rt.com/rss/sport/"
    # مصدر المباريات (YallaKora)
    matches_url = "https://www.yallakora.com/match-center"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        # 1. سحب المباريات (التصميم العلوي)
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

        # 2. سحب الأخبار (عرض الصور الحقيقية فقط)
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_grid_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            img = item.find('enclosure').get('url') if item.find('enclosure') else None
            
            # تخطي الخبر إذا لم تتوفر صورة حقيقية (الإضافة رقم 3)
            if not img:
                continue
            
            news_grid_html += f'''
            <div class="n-card">
                <a href="{my_link}" target="_blank">
                    <div class="n-img">
                        <img src="{img}" loading="lazy">
                        <div class="n-badge">حصري</div>
                    </div>
                    <div class="n-info">
                        <h3>{title}</h3>
                        <div class="n-footer">
                            <span>⏱️ {datetime.now().strftime('%H:%M')}</span>
                            <span class="n-more">التفاصيل</span>
                        </div>
                    </div>
                </a>
            </div>'''

        # 3. بناء الواجهة (Vortex-Grid UI)
        update_time = datetime.now().strftime('%H:%M')
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ستاديوم 24 | VORTEX</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #0b0d11; --card: #161a21; --gold: #c5a059; --text: #e1e1e1; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Cairo', sans-serif; margin: 0; padding: 0; }}
        
        header {{ background: var(--card); padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 2px solid var(--gold); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo {{ color: #fff; }} .logo span {{ color: var(--gold); }}

        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; }}
        
        /* إضافة: شريط حالة التحديث */
        .status-bar {{ font-size: 12px; color: #00ff88; margin-bottom: 10px; text-align: left; }}

        .match-scroller {{ display: flex; gap: 10px; overflow-x: auto; padding-bottom: 15px; margin-bottom: 25px; scrollbar-width: none; }}
        .m-card {{ background: var(--card); min-width: 180px; padding: 12px; border-radius: 12px; border: 1px solid #252a33; text-align: center; }}
        .m-team {{ font-size: 12px; font-weight: bold; margin: 5px 0; }}
        .m-score {{ background: var(--gold); color: #000; font-weight: 900; padding: 2px 8px; border-radius: 4px; display: inline-block; }}

        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        .n-card {{ background: var(--card); border-radius: 15px; overflow: hidden; border: 1px solid #232932; transition: 0.3s; }}
        .n-card:hover {{ transform: translateY(-5px); border-color: var(--gold); }}
        .n-card a {{ text-decoration: none; color: inherit; }}
        .n-img {{ position: relative; height: 180px; }}
        .n-img img {{ width: 100%; height: 100%; object-fit: cover; }}
        .n-badge {{ position: absolute; top: 10px; right: 10px; background: var(--gold); color: #000; font-size: 10px; font-weight: 900; padding: 3px 10px; border-radius: 5px; }}
        
        .n-info {{ padding: 15px; }}
        .n-info h3 {{ font-size: 15px; margin: 0 0 15px 0; line-height: 1.6; height: 48px; overflow: hidden; font-weight: 700; }}
        .n-footer {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #888; }}
        .n-more {{ color: var(--gold); border: 1px solid var(--gold); padding: 2px 10px; border-radius: 20px; }}

        .ad-slot {{ text-align: center; margin: 20px 0; overflow: hidden; }}

        footer {{ background: #000; padding: 40px; text-align: center; border-top: 2px solid var(--gold); margin-top: 50px; }}
        
        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
            .n-img {{ height: 220px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">VORTEX<span>26</span></a>
        <div style="color: #00ff88; font-size: 13px; font-weight: bold;">● مباشر</div>
    </header>

    <div class="container">
        <div class="status-bar">آخر تحديث: {update_time}</div>
        
        <div class="ad-slot">
            <ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>
        </div>

        <div class="match-scroller">
            {matches_html}
        </div>

        <h2 style="border-right: 5px solid var(--gold); padding-right: 15px; margin-bottom: 25px;">أبرز الأخبار الآن</h2>
        <div class="news-grid">
            {news_grid_html}
        </div>

        <div class="ad-slot">
            <script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>
        </div>
    </div>

    <footer>
        <div style="font-size: 26px; font-weight: 900; color: #fff;">VORTEX 26</div>
        <p style="font-size: 12px; color: #555;">تغطية رياضية عالمية بنمط المربعات الفخم</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        print("تم التحديث بنجاح.")
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run_premium_grid_scraper()
