import feedparser

# URL do Feed RSS da Revista ADEGA
FEED_URL = "https://revistaadega.uol.com.br/feed/completo"
feed = feedparser.parse(FEED_URL)

# Selecionar as 10 matérias mais recentes
items = feed.entries[:10]

# Início do HTML
html = """
<div style='font-family:Arial,sans-serif; max-width:600px; margin:0 auto; padding:20px;'>
  <div style='text-align:center; margin-bottom:15px;'>
    <img src='https://revistaadega.uol.com.br/static/img/logo_adega_w400.png' alt='Revista ADEGA' style='max-width:220px; height:auto;'>
    <div style='margin-top:6px; font-size:12px;'>
      <a href='https://www.revistaadega.com.br' style='text-decoration:none; color:#912e1f;'>www.revistaadega.com.br</a>
    </div>
  </div>

  <h1 style='text-align:center; color:#912e1f; font-size:24px; margin-bottom:10px;'>Notícias da Semana</h1>
  <p style='text-align:center; color:#555; font-size:16px; margin-bottom:40px;'>Você está recebendo as últimas notícias publicadas em nosso site</p>
"""

# Adicionando as 10 matérias com imagem e botão
for item in items:
    title = item.title
    link = item.link

    # Tentativa de captura da imagem da matéria
    image = ""
    if 'media_content' in item and item.media_content:
        image = item.media_content[0].get('url', '')
    elif 'enclosures' in item and item.enclosures:
        image = item.enclosures[0].get('url', '')

    html += f"""
    <div style='margin:30px 0; border-top:1px solid #ccc; padding-top:20px;'>
      <img src='{image}' alt='{title}' width='500' style='max-width:100%; height:auto; display:block; margin:0 auto 15px; border-radius:8px;'/>
      <h2 style='font-size:18px; color:#333; margin:10px 0; text-align:center;'>{title}</h2>

      <!--[if mso]>
      <center>
        <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word"
          href="{link}" style="height:40px;v-text-anchor:middle;width:220px;" arcsize="10%" strokecolor="#912e1f" fillcolor="#912e1f">
          <w:anchorlock/>
          <center style="color:#ffffff;font-family:Arial,sans-serif;font-size:14px;font-weight:bold;">
            Leia a matéria completa
          </center>
        </v:roundrect>
      </center>
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

# Banner comercial ao final
html += """
  <div style='text-align:center; margin-top:40px;'>
    <a href='https://www.adegaonline.com.br/products/coravin-three-timeless' target='_blank'>
      <img src='https://d335luupugsy2.cloudfront.net/cms/files/730291/1745615983/$qpip5qpjcil' alt='Banner Comercial' width='500' style='max-width:100%; height:auto; border-radius:6px; margin-top:30px;'/>
    </a>
  </div>
</div>
"""

# Salvando o arquivo HTML
with open("newsletter_adega_final.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML da newsletter gerado com sucesso!")

