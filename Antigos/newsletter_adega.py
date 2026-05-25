import feedparser

# URL do feed RSS da Revista ADEGA
rss_url = "https://revistaadega.uol.com.br/feed/completo"
feed = feedparser.parse(rss_url)

# Seleciona os 5 primeiros itens
items = feed.entries[:5]

# Monta o HTML
html_output = """
<div style="font-family:Arial,sans-serif; max-width:600px; margin:0 auto; padding:20px;">
  <div style="text-align:center; margin-bottom:20px;">
    <img src="https://revistaadega.uol.com.br/media/images/logo_adega.png" alt="Revista ADEGA" style="max-width:200px; height:auto;">
  </div>
  <h1 style="text-align:center; color:#912e1f;">🍷 Destaques da Semana – Revista ADEGA</h1>
"""

# Loop para cada item
for entry in items:
    title = entry.title
    link = entry.link
    description = entry.description
    image_url = entry.enclosures[0].href if 'enclosures' in entry and entry.enclosures else ""

    html_output += f"""
    <div style="margin-bottom:30px; border-bottom:1px solid #ddd; padding-bottom:20px;">
      <img src="{image_url}" alt="{title}" style="width:100%; max-width:550px; border-radius:6px;">
      <h2 style="font-size:20px; margin:10px 0 5px; color:#912e1f;">{title}</h2>
      <p style="color:#333; font-size:14px;">{description}</p>
      <a href="{link}" target="_blank" style="color:#912e1f; font-weight:bold;">Leia a matéria completa</a>
    </div>
    """

# Rodapé
html_output += """
  <div style="text-align:center; margin-top:30px; font-size:14px; color:#555;">
    <a href="https://revistaadega.uol.com.br/" style="color:#912e1f; font-weight:bold;">Ver todas as matérias no site</a>
  </div>
</div>
"""

# Salvar em arquivo HTML
with open("newsletter_adega.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ HTML gerado com sucesso: newsletter_adega.html")
