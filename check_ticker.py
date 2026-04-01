import os

dirs = ['origem','jogadores','tecnicos','escalacoes','presidentes','curiosidades','noticias',
        'momentos-historicos','elenco','artilheiros','hino','jogos-historicos','rivalidades',
        'uniformes','estadios','quiz','torcida','estatisticas','base','sobre','contato',
        'termos-de-uso','politica-privacidade','artigos']

base = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")
missing = []
for d in dirs:
    f = os.path.join(base, d, "index.html")
    if os.path.exists(f):
        with open(f, 'r') as fp:
            if 'header-ticker' in fp.read():
                print(f"OK: {d}")
            else:
                print(f"FALTA: {d}")
                missing.append(d)
    else:
        print(f"MISSING FILE: {d}")

print(f"\nFaltam: {len(missing)} páginas: {missing}")
