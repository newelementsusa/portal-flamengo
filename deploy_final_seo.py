import ftplib, os, subprocess

BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")

# All 38 pages (excluding titulos redirect)
pages = [
    ("index.html", ""),
    ("origem/index.html", "origem"),("jogadores/index.html", "jogadores"),
    ("tecnicos/index.html", "tecnicos"),("escalacoes/index.html", "escalacoes"),
    ("presidentes/index.html", "presidentes"),("curiosidades/index.html", "curiosidades"),
    ("noticias/index.html", "noticias"),("momentos-historicos/index.html", "momentos-historicos"),
    ("elenco/index.html", "elenco"),("artilheiros/index.html", "artilheiros"),
    ("hino/index.html", "hino"),("jogos-historicos/index.html", "jogos-historicos"),
    ("rivalidades/index.html", "rivalidades"),("uniformes/index.html", "uniformes"),
    ("estadios/index.html", "estadios"),("quiz/index.html", "quiz"),
    ("torcida/index.html", "torcida"),("estatisticas/index.html", "estatisticas"),
    ("base/index.html", "base"),("sobre/index.html", "sobre"),
    ("contato/index.html", "contato"),("termos-de-uso/index.html", "termos-de-uso"),
    ("politica-privacidade/index.html", "politica-privacidade"),
    ("artigos/index.html", "artigos"),("jogos-2026/index.html", "jogos-2026"),
    ("proximo-jogo/index.html", "proximo-jogo"),("onde-assistir/index.html", "onde-assistir"),
    ("classificacao/index.html", "classificacao"),("todos-os-titulos/index.html", "todos-os-titulos"),
    ("ingressos/index.html", "ingressos"),("mascote/index.html", "mascote"),
    ("goleadas/index.html", "goleadas"),("selecao-brasileira/index.html", "selecao-brasileira"),
    ("confrontos/index.html", "confrontos"),("wallpapers/index.html", "wallpapers"),
    ("frases/index.html", "frases"),("memes/index.html", "memes"),
]

ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

for local_file, remote_dir in pages:
    local_path = os.path.join(BASE, local_file)
    remote_path = "/public_html/" + remote_dir if remote_dir else "/public_html"
    try: ftp.cwd(remote_path)
    except:
        ftp.mkd(remote_path)
        ftp.cwd(remote_path)
    with open(local_path, "rb") as f:
        ftp.storbinary("STOR index.html", f)

ftp.quit()
print(f"Deploy: {len(pages)} páginas")

os.chdir(BASE)
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "SEO final: google-adsense-account meta + keywords + FAQPage schema\n\n- Added google-adsense-account meta to all 38 pages\n- Added keywords meta to politica-privacidade and termos-de-uso\n- Added FAQPage schema to contato\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"', shell=True)
subprocess.run("git push origin main", shell=True)
print("Done!")
