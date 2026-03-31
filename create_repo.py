import subprocess, os

os.chdir(os.path.expanduser("~/Claudinho/projetos/portal-flamengo"))

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"$ {cmd}")
    if result.stdout:
        print(result.stdout[:500])
    if result.returncode != 0 and result.stderr:
        print(f"ERR: {result.stderr[:300]}")
    return result.returncode

# Create repo on GitHub using gh CLI
print("Criando repositório no GitHub...")
run('gh repo create newelementsusa/portal-flamengo --public --description "Portal Flamengo - A Maior Enciclopédia do Mengão" --source . --remote origin --push')

print("\nDone!")
