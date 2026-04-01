import ftplib, os, subprocess

BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")

# Pages that were SEO-fixed
fixed = [
    'proximo-jogo','classificacao','todos-os-titulos','ingressos',
    'goleadas','selecao-brasileira','confrontos','wallpapers','frases','memes',
    'mascote','artigos','sobre','contato','politica-privacidade','termos-de-uso'
]

ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

for page in fixed:
    local = os.path.join(BASE, page, "index.html")
    if not os.path.exists(local):
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
print(f"\nDeploy SEO: {len(fixed)} páginas")

# Git
os.chdir(BASE)
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "SEO audit: 24 fixes across 16 pages\n\n- Titles shortened to <60 chars (8 pages)\n- BreadcrumbList Schema added (14 pages)\n- og:image added (2 pages)\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"', shell=True)
subprocess.run("git push origin main", shell=True)
print("Git pushed!")
