import ftplib, os

LOCAL_BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")

# All main pages + institutional
pages = [
    ("index.html", ""),
    ("origem/index.html", "origem"),
    ("jogadores/index.html", "jogadores"),
    ("curiosidades/index.html", "curiosidades"),
    ("tecnicos/index.html", "tecnicos"),
    ("presidentes/index.html", "presidentes"),
    ("escalacoes/index.html", "escalacoes"),
    ("noticias/index.html", "noticias"),
    ("momentos-historicos/index.html", "momentos-historicos"),
    ("elenco/index.html", "elenco"),
    ("artilheiros/index.html", "artilheiros"),
    ("hino/index.html", "hino"),
    ("jogos-historicos/index.html", "jogos-historicos"),
    ("rivalidades/index.html", "rivalidades"),
    ("uniformes/index.html", "uniformes"),
    ("estadios/index.html", "estadios"),
    ("quiz/index.html", "quiz"),
    ("torcida/index.html", "torcida"),
    ("estatisticas/index.html", "estatisticas"),
    ("base/index.html", "base"),
    ("sobre/index.html", "sobre"),
    ("contato/index.html", "contato"),
    ("termos-de-uso/index.html", "termos-de-uso"),
    ("politica-privacidade/index.html", "politica-privacidade"),
    ("titulos/index.html", "titulos"),
    ("artigos/index.html", "artigos"),
]

# Manual biographies with ticker
bios = ['zico','gabigol','romario','junior','leonidas','garrincha','adriano',
        'petkovic','vinicius-junior','ronaldinho-gaucho','arrascaeta','pedro',
        'bruno-henrique','everton-ribeiro','adilio','leandro','nunes','mozer',
        'david-luiz','filipe-luis']

ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

# Deploy main pages
for local_file, remote_dir in pages:
    local_path = os.path.join(LOCAL_BASE, local_file)
    remote_path = "/public_html/" + remote_dir if remote_dir else "/public_html"
    try:
        ftp.cwd(remote_path)
    except:
        ftp.mkd(remote_path)
        ftp.cwd(remote_path)
    with open(local_path, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    print(f"OK: {local_file}")

# Deploy manual biographies
for slug in bios:
    local_path = os.path.join(LOCAL_BASE, "jogadores", slug, "index.html")
    if not os.path.exists(local_path):
        continue
    remote_path = f"/public_html/jogadores/{slug}"
    try:
        ftp.cwd(remote_path)
    except:
        ftp.cwd("/public_html/jogadores")
        try:
            ftp.mkd(slug)
        except:
            pass
        ftp.cwd(remote_path)
    with open(local_path, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    print(f"BIO OK: {slug}")

ftp.quit()
print("\nDeploy completo!")
