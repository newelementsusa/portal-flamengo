import ftplib, os

BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")
files = ["sitemap.xml", "robots.txt"]

ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")
ftp.cwd("/public_html")

for f in files:
    with open(os.path.join(BASE, f), "rb") as fp:
        ftp.storbinary(f"STOR {f}", fp)
    print(f"OK: {f}")

ftp.quit()
print("Done!")
