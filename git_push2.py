import subprocess, os
os.chdir(os.path.expanduser("~/Claudinho/projetos/portal-flamengo"))

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"$ {cmd}")
    if r.stdout: print(r.stdout[:500])
    if r.returncode != 0 and r.stderr: print(f"ERR: {r.stderr[:300]}")

run("git add -A")
run('git commit -m "Add 6 new pages + image fixes + AdSense + sitemap\n\n- Sobre, Contato, Termos, Privacidade, Títulos, Artigos\n- 163 images fixed (football-only)\n- AdSense ca-pub-1286595053228930\n- Sitemap 25 URLs\n- Header ticker\n- ads.txt, robots.txt\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"')
run("git push origin main")
