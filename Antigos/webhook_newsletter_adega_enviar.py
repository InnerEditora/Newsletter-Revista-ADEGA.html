# -*- coding: utf-8 -*-
import feedparser
import requests

# URL do feed RSS da Revista ADEGA
rss_url = "https://revistaadega.uol.com.br/feed/completo"

# Quantidade de matérias a incluir
num_materias = 5

# Ler o feed RSS
feed = feedparser.parse(rss_url)
items = feed.entries[:num_materias]

# Montar o HTML refinado
html_content = """
<div style='font-family:Arial,sans-serif; max-width:600px; margin:0 auto; padding:20px;'>
  <div style='text-align:center; margin-bottom:15px;'>
    <img src='https://revistaadega.uol.com.br/static/img/logo_adega_w400.png' alt='Revista ADEGA' style='max-width:220px; height:auto;'>
    <div style='margin-top:6px; font-size:12px;'>
      <a href='https://www.revistaadega.com.br' style='text-decoration:none; color:#912e1f;'>www.revistaadega.com.br</a>
    </div>
  </div>

  <h1 style='text-align:center; color:#912e1f; font-size:24px; margin-bottom:10px;'>Revista ADEGA News</h1>
  <p style='text-align:center; color:#555; font-size:16px; margin-bottom:40px;'>As novidades do mundo do vinho</p>
"""

for item in items:
    title = item.title
    link = item.link
    # tentar obter imagem (via media_content ou enclosure)
    image = ""
    if "media_content" in item:
        image = item.media_content[0].get("url", "")
    elif "enclosures" in item and item.enclosures:
        image = item.enclosures[0].get("href", "")

    html_content += f"""
    <div style='margin:30px 0; border-top:1px solid #ccc; padding-top:20px;'>
      <img src='{image}' alt='{title}' style='width:100%; max-height:250px; object-fit:cover; border-radius:8px; margin-bottom:15px;'/>
      <h2 style='font-size:18px; color:#333; margin:10px 0;'>{title}</h2>
      <div style='text-align:center;'>
        <a href='{link}' style='display:inline-block; padding:10px 20px; background-color:#912e1f; color:#fff; text-decoration:none; border-radius:4px;'>
          Leia a matéria completa
        </a>
      </div>
    </div>
    """

# Banner comercial com link
html_content += """
  <div style='text-align:center; margin-top:40px;'>
    <a href='https://www.adegaonline.com.br/products/coravin-three-timeless' target='_blank'>
      <img src='https://d335luupugsy2.cloudfront.net/cms/files/730291/1745615983/$qpip5qpjcil' alt='Banner Comercial' style='width:100%; max-width:600px; height:auto; border-radius:6px; margin-top:30px;'/>
    </a>
  </div>
</div>
"""

# (Opcional) salvar localmente para ver preview
with open("newsletter_adega_final.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Enviar para o Webhook do Make
webhook_url = "https://hook.us2.make.com/e4jdphsbx8hwzmak858qspub2t8bm2bd"
payload = {"html": html_content}
resp = requests.post(webhook_url, json=payload)

if resp.status_code == 200:
    print("✅ HTML gerado e enviado com sucesso ao Make.")
else:
    print("❌ Erro ao enviar ao Make:", resp.status_code, resp.text)
