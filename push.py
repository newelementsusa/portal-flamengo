import subprocess, os
os.chdir(os.path.expanduser("~/Claudinho/projetos/portal-flamengo"))

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"$ {cmd}")
    if result.stdout: print(result.stdout[:500])
    if result.stderr: print(result.stderr[:300])
    return result.returncode

run("git remote set-url origin https://github.com/newelementsusa/portal-flamengo.git")
run("git push -u origin main")
