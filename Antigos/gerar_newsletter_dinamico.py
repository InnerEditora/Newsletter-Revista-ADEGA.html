import feedparser

# Feed RSS da Revista ADEGA
FEED_URL = "https://revistaadega.uol.com.br/feed/completo"
feed = feedparser.parse(FEED_URL)

# Seleciona os 5 conteúdos mais recentes
items = feed.entries[:5]

# HTML base
html = """
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

# Monta os blocos das matérias
for item in items:
    title = item.title
    link = item.link
    image = ""

    # Tenta extrair imagem do RSS
    if 'media_content' in item and item.media_content:
        image = item.media_content[0].get('url', '')
    elif 'enclosures' in item and item.enclosures:
        image = item.enclosures[0].get('url', '')

    html += f"""
    <div style='margin:30px 0; border-top:1px solid #ccc; padding-top:20px;'>
      <img src='{image}' alt='{title}' width='500' style='max-width:100%; height:auto; display:block; margin:0 auto 15px; border-radius:8px;'/>
      <h2 style='font-size:18px; color:#333; margin:10px 0; text-align:center;'>{title}</h2>

      <!--[if mso]>
      <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word"
        href="{link}" style="height:40px;v-text-anchor:middle;width:220px;" arcsize="10%" strokecolor="#912e1f" fillcolor="#912e1f">
        <w:anchorlock/>
        <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:14px;font-weight:bold;">
          Leia a matéria completa
        </center>
      </v:roundrect>
      <![endif]-->

      <!--[if !mso]><!-- -->
      <table cellspacing="0" cellpadding="0" border="0" align="center" style="margin-top:12px;">
        <tr>
          <td align="center" bgcolor="#912e1f" style="border-radius:4px;">
            <a href="{link}" target="_blank" style="display:inline-block; padding:10px 20px; font-size:14px; font-family:Arial,sans-serif; color:#ffffff; text-decoration:none; font-weight:bold;">
              Leia a matéria completa
            </a>
          </td>
        </tr>
      </table>
      <!--<![endif]-->
    </div>
    """

# Banner final
html += """
  <div style='text-align:center; margin-top:40px;'>
    <a href='https://www.adegaonline.com.br/products/coravin-three-timeless' target='_blank'>
      <img src='https://d335luupugsy2.cloudfront.net/cms/files/730291/1745615983/$qpip5qpjcil' alt='Banner Comercial' width='500' style='max-width:100%; height:auto; border-radius:6px; margin-top:30px;'/>
    </a>
  </div>
</div>
"""

# Salva como HTML
with open("newsletter_adega_outlook.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Newsletter gerada com sucesso: newsletter_adega_outlook.html")
