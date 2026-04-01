import ftplib, os

HOST = "69.6.220.159"
LOCAL_BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")

# Get all biography folders
bio_dir = os.path.join(LOCAL_BASE, "jogadores")
bios = [d for d in os.listdir(bio_dir) if os.path.isdir(os.path.join(bio_dir, d)) and d != '.claude']

# Deploy to production
ftp = ftplib.FTP(HOST)
ftp.login("portalflamengoco", "claude2026#")
print(f"Conectado produção. {len(bios)} biografias para deploy.")

for slug in sorted(bios):
    local_file = os.path.join(bio_dir, slug, "index.html")
    if not os.path.exists(local_file):
        continue

    remote_path = f"/public_html/jogadores/{slug}"
    try:
        ftp.cwd(remote_path)
    except:
        try:
            ftp.cwd("/public_html/jogadores")
        except:
            ftp.mkd("/public_html/jogadores")
            ftp.cwd("/public_html/jogadores")
        ftp.mkd(slug)
        ftp.cwd(remote_path)

    with open(local_file, "rb") as f:
        ftp.storbinary("STOR index.html", f)
    print(f"OK: jogadores/{slug}/")

# Also re-upload the main jogadores index
main_file = os.path.join(LOCAL_BASE, "jogadores", "index.html")
ftp.cwd("/public_html/jogadores")
with open(main_file, "rb") as f:
    ftp.storbinary("STOR index.html", f)
print("OK: jogadores/index.html (main)")

ftp.quit()
print(f"\nDeploy completo! {len(bios)} biografias no ar.")
