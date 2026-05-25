# -*- coding: utf-8 -*-
import feedparser

rss_url = "https://revistaadega.uol.com.br/feed/completo"
feed = feedparser.parse(rss_url)

max_items = 5

html_content = """
<div style='font-family:Arial,sans-serif; max-width:600px; margin:0 auto; padding:20px;'>
  <div style='text-align:center; margin-bottom:15px;'>
    <img src='https://revistaadega.uol.com.br/static/img/logo_adega_w400.png' alt='Revista ADEGA' style='max-width:220px; height:auto;'>
    <div style='margin-top:6px; font-size:12px;'>
      <a href='https://www.revistaadega.com.br' style='color:#912e1f; text-decoration:none;'>www.revistaadega.com.br</a>
    </div>
  </div>

  <h1 style='text-align:center; color:#912e1f; font-size:24px; margin-bottom:10px;'>Revista ADEGA News</h1>
  <p style='text-align:center; font-size:16px; color:#555; margin-bottom:40px;'>As novidades do mundo do vinho</p>
"""

for entry in feed.entries[:max_items]:
    title = entry.title
    link = entry.link
    image = entry.enclosures[0].href if entry.enclosures else ""
    html_content += f"""
    <div style='margin-bottom:50px; border-bottom:1px solid #ccc; padding-bottom:30px;'>
      <img src='{image}' alt='{title}' style='width:100%; max-height:240px; object-fit:cover; border-radius:8px; margin-bottom:15px;'>
      <h2 style='font-size:18px; color:#333; margin-bottom:20px;'>{title}</h2>
      <div style='text-align:center;'>
        <a href='{link}' target='_blank' style='display:inline-block; background-color:#912e1f; color:#fff; padding:10px 20px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:14px;'>
          ➤ Leia a matéria completa
        </a>
      </div>
    </div>
    """

html_content += """
  <div style='text-align:center; margin-top:50px;'>
    <a href='https://revistaadega.uol.com.br/' style='color:#912e1f; font-weight:bold; font-size:14px;'>Ver todas as matérias no site</a>
  </div>
  <div style='text-align:center; margin-top:40px;'>
    <a href='https://www.adegaonline.com.br/products/coravin-three-timeless' target='_blank'>
      <img src='https://d335luupugsy2.cloudfront.net/cms/files/730291/1745615983/$qpip5qpjcil' alt='Banner Comercial' style='width:100%; max-width:600px; height:auto; margin-top:30px; border-radius:6px;'>
    </a>
  </div>
</div>
"""

with open("newsletter_adega_final.py.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTML final gerado com sucesso!")
