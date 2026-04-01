"""Upload sitemap + push to git"""
import ftplib, os, subprocess

BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")

# 1. Upload sitemap
print("=== UPLOAD SITEMAP ===")
ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")
ftp.cwd("/public_html")
with open(os.path.join(BASE, "sitemap.xml"), "rb") as f:
    ftp.storbinary("STOR sitemap.xml", f)
print("OK: sitemap.xml (38 URLs)")
ftp.quit()

# 2. Git push
print("\n=== GIT PUSH ===")
os.chdir(BASE)
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "Portal Flamengo: 39 páginas + 810 biografias + 13 SEO pages\n\n- 39 páginas principais\n- 751 biografias de jogadores\n- 59 biografias de presidentes\n- Sitemap atualizado (38 URLs)\n- AdSense, SSL, Schema.org\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"', shell=True)
subprocess.run("git push origin main", shell=True)
print("\nTudo sincronizado!")
