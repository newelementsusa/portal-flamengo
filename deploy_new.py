import ftplib, os

LOCAL_BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")
new_pages = [
    'jogos-2026', 'proximo-jogo', 'onde-assistir', 'classificacao',
    'todos-os-titulos', 'ingressos', 'mascote', 'goleadas',
    'selecao-brasileira', 'confrontos', 'wallpapers', 'frases', 'memes'
]

ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

for page in new_pages:
    local = os.path.join(LOCAL_BASE, page, "index.html")
    if not os.path.exists(local):
        print(f"SKIP: {page} (não existe)")
        continue
    remote = f"/public_html/{page}"
    try:
        ftp.cwd(remote)
    except:
        ftp.mkd(remote)
        ftp.cwd(remote)
    with open(local, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    print(f"OK: {page}")

ftp.quit()
print(f"\nDeploy completo! {len(new_pages)} páginas.")
