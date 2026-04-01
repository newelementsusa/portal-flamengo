import ftplib, os, subprocess

BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")

# Deploy home + noticias
ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

ftp.cwd("/public_html")
with open(os.path.join(BASE, "index.html"), "rb") as f:
    ftp.storbinary("STOR index.html", f)
print("OK: index.html")

ftp.cwd("/public_html/noticias")
with open(os.path.join(BASE, "noticias/index.html"), "rb") as f:
    ftp.storbinary("STOR index.html", f)
print("OK: noticias/index.html")

ftp.quit()

# Git
os.chdir(BASE)
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "Add 3 new news: Léo Pereira Seleção, Luiz Henrique Zenit, Libertadores debut\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"', shell=True)
subprocess.run("git push origin main", shell=True)
print("Done!")
