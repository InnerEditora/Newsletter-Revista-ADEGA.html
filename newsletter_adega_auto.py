import feedparser
import subprocess
import requests
import json
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES — PREENCHA AQUI
# ============================================================

RD_TOKEN_PRIVADO = "f4db4fdfc57bf5cf0f187c9dbb629fc9"  # Cole aqui o Token Privado do RD Station
RD_CAMPANHA_BASE_ID = 19596655               # ID da campanha base para duplicar
RD_EMAIL_REMETENTE = "contato@adegaonline.com.br"
RD_NOME_REMETENTE = "Revista ADEGA"
RD_ASSUNTO = "As últimas notícias da semana para você ler no final de semana."

GITHUB_PAGES_URL = "https://innereditora.github.io/Newsletter-Revista-ADEGA.html/"

GIT_EXE = r"C:\Users\felip\AppData\Local\GitHubDesktop\app-3.5.8\resources\app\git\cmd\git.exe"
PASTA_NEWSLETTER = r"C:\Users\felip\Desktop\Newsletter"
ARQUIVO_HTML = r"C:\Users\felip\Desktop\Newsletter\newsletter_adega_final.html"

FEED_URL = "https://revistaadega.uol.com.br/feed/completo"

# ============================================================
# PASSO 1 — GERAR O HTML DA NEWSLETTER
# ============================================================

print("▶ [1/3] Gerando HTML da newsletter...")

feed = feedparser.parse(FEED_URL)
items = feed.entries[:10]

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

for item in items:
    title = item.title
    link = item.link

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
        <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
          xmlns:w="urn:schemas-microsoft-com:office:word"
          href="{link}"
          style="height:40px;v-text-anchor:middle;width:220px;"
          arcsize="10%"
          strokecolor="#912e1f"
          fillcolor="#912e1f">
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
            <a href="{link}" target="_blank"
               style="display:inline-block;padding:10px 20px;font-size:14px;font-family:Arial,sans-serif;color:#ffffff;text-decoration:none;font-weight:bold;">
              Leia a matéria completa
            </a>
          </td>
        </tr>
      </table>
      <!--<![endif]-->
    </div>
    """

html += """
  <div style='text-align:center; margin-top:40px;'>
    <a href='https://www.adegaonline.com.br/products/coravin-three-timeless' target='_blank'>
      <img src='https://d335luupugsy2.cloudfront.net/cms/files/730291/1745615983/$qpip5qpjcil'
           alt='Banner Comercial' width='500'
           style='max-width:100%;height:auto;border-radius:6px;margin-top:30px;'/>
    </a>
  </div>
</div>
"""

with open(ARQUIVO_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ HTML gerado com sucesso!")

# ============================================================
# PASSO 2 — PUSH PARA O GITHUB
# ============================================================

print("▶ [2/3] Enviando para o GitHub...")

data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

try:
    subprocess.run([GIT_EXE, "-C", PASTA_NEWSLETTER, "add", "."], check=True)

    resultado_commit = subprocess.run(
        [GIT_EXE, "-C", PASTA_NEWSLETTER, "commit", "-m", f"Newsletter automática - {data_hoje}"],
        capture_output=True, text=True
    )

    if resultado_commit.returncode == 0:
        print("  → Commit realizado!")
    else:
        print("  → Nenhuma alteração nova, seguindo para o push...")

    subprocess.run([GIT_EXE, "-C", PASTA_NEWSLETTER, "push", "origin", "HEAD:main"], check=True)
    print("✅ Push realizado com sucesso!")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Erro no Git: {e}")
    print("Verifique se o repositório está configurado corretamente.")
    exit(1)

# ============================================================
# PASSO 3 — DUPLICAR CAMPANHA E DISPARAR NO RD STATION
# ============================================================

print("▶ [3/3] Acessando RD Station...")

headers = {
    "Authorization": f"Bearer {RD_TOKEN_PRIVADO}",
    "Content-Type": "application/json"
}

# 3a. Duplicar a campanha base
print(f"  → Duplicando campanha {RD_CAMPANHA_BASE_ID}...")
url_duplicar = f"https://api.rd.services/emails/campaigns/{RD_CAMPANHA_BASE_ID}/clone"

resp_clone = requests.post(url_duplicar, headers=headers)

if resp_clone.status_code not in [200, 201]:
    print(f"❌ Erro ao duplicar campanha: {resp_clone.status_code}")
    print(resp_clone.text)
    exit(1)

nova_campanha = resp_clone.json()
nova_id = nova_campanha.get("id") or nova_campanha.get("data", {}).get("id")
print(f"  → Nova campanha criada com ID: {nova_id}")

# 3b. Atualizar link, assunto e remetente
print("  → Atualizando campanha...")
url_atualizar = f"https://api.rd.services/emails/campaigns/{nova_id}"

payload_update = {
    "subject": RD_ASSUNTO,
    "sender_email": RD_EMAIL_REMETENTE,
    "sender_name": RD_NOME_REMETENTE,
    "html_body_url": GITHUB_PAGES_URL
}

resp_update = requests.patch(url_atualizar, headers=headers, data=json.dumps(payload_update))

if resp_update.status_code not in [200, 201]:
    print(f"❌ Erro ao atualizar campanha: {resp_update.status_code}")
    print(resp_update.text)
    exit(1)

print("  → Campanha atualizada!")

# 3c. Disparar
print("  → Disparando campanha...")
url_disparar = f"https://api.rd.services/emails/campaigns/{nova_id}/send"

resp_envio = requests.post(url_disparar, headers=headers)

if resp_envio.status_code in [200, 201, 204]:
    print("✅ Campanha disparada com sucesso no RD Station!")
else:
    print(f"❌ Erro ao disparar campanha: {resp_envio.status_code}")
    print(resp_envio.text)
    exit(1)

print("\n🎉 Processo completo! Newsletter enviada automaticamente.")