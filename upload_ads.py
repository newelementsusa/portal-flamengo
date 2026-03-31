import ftplib, os

LOCAL = os.path.expanduser("~/Claudinho/projetos/portal-flamengo/ads.txt")

# Upload to production
ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")
ftp.cwd("/public_html")
with open(LOCAL, "rb") as f:
    ftp.storbinary("STOR ads.txt", f)
print("OK: ads.txt -> portalflamengo.com.br/ads.txt")

# Upload to preview too
ftp2 = ftplib.FTP("69.6.220.159")
ftp2.login("newnewelements", "3b=[ffLU^VNs")
ftp2.cwd("/public_html/portal-flamengo")
with open(LOCAL, "rb") as f:
    ftp2.storbinary("STOR ads.txt", f)
print("OK: ads.txt -> new.newelements.com/portal-flamengo/ads.txt")

ftp.quit()
ftp2.quit()
print("Done!")
