import os
d = os.path.expanduser('~/Claudinho/projetos/portal-flamengo/jogadores')
dirs = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)) and x != '.claude']
count = sum(1 for x in dirs if os.path.exists(os.path.join(d, x, 'index.html')))
print(f'Pastas: {len(dirs)} | Com index.html: {count}')
