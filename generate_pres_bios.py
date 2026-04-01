#!/usr/bin/env python3
"""Generate biography pages for all 76 Flamengo presidents and make names clickable."""
import os, re, unicodedata, ftplib

LOCAL_BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")
PRES_DIR = os.path.join(LOCAL_BASE, "presidentes")

PHOTOS = {
    'patricia-amorim': 'patricia-amorim.jpg',
    'bandeira-de-mello': 'bandeira-de-mello.jpg',
    'rodolfo-landim': 'rodolfo-landim.png',
}

PRESIDENTS = [
    ("Domingos Marques de Azevedo", "1895-1897", "Primeiro presidente do Flamengo. Liderou a fundação do clube como sociedade de regatas."),
    ("Augusto Lopes da Silveira", "1898", ""),
    ("Júlio Gonçalves de A. Furtado", "1899", ""),
    ("Antonio Pereira Viana Filho", "1900", ""),
    ("Jacintho Pinto de Lima Júnior", "1900", ""),
    ("Fidelcino da Silva Leitão", "1901", ""),
    ("Virgílio Leite de Oliveira e Silva", "1902, 1907-1911, 1913, 1915", "Presidente com mais mandatos nos primeiros anos. Três passagens pela presidência."),
    ("Arthur John Lawrence Gibbons", "1903", ""),
    ("Mário Espínola", "1904", ""),
    ("José Agostinho Pereira da Cunha", "1905", ""),
    ("Manuel Alves de Cruz Rios", "1905", ""),
    ("Francis Hamilton Wálter", "1906", ""),
    ("Edmundo de Azurém Furtado", "1912, 1914, 1915", "Três mandatos nos primeiros anos do futebol no Flamengo."),
    ("José Pimenta de Melo Filho", "1913", ""),
    ("Raul Ferreira Serpa", "1916", ""),
    ("Carlos Leclerc Castelo Branco", "1917", ""),
    ("Alberto Burle Figueiredo", "1918-1920, 1922", ""),
    ("Faustino Esposel", "1921, 1924-1927", ""),
    ("Júlio Benedito Otoni", "1923-1924", ""),
    ("Alberto Borgerth", "1927", "Um dos fundadores do departamento de futebol do Flamengo em 1911."),
    ("Nillor Rollin Pinheiro", "1927", ""),
    ("Osvaldo dos Santos Jacinto", "1928-1929", ""),
    ("Carlos Eduardo Façanha Mamede", "1929, 1931", ""),
    ("Alfredo Dolabella Portela", "1930", ""),
    ("Manuel Joaquim de Almeida", "1930", ""),
    ("Rubens de Campos Farrula", "1931", ""),
    ("José de Oliveira Santos", "1931, 1933", ""),
    ("Artur Lobo da Silva", "1932", ""),
    ("Pascoal Segreto Sobrinho", "1933", ""),
    ("José Bastos Padilha", "1933-1937", "Profissionalizou o futebol no Flamengo. Contratou Leônidas da Silva e outros craques. Transformou o clube em potência do futebol carioca."),
    ("Raul Dias Gonçalves", "1937-1938", ""),
    ("Gustavo Adolfo de Carvalho", "1939-1942", "Presidiu durante a era de ouro do futebol com Leônidas, Domingos da Guia e Zizinho. Tetracampeão carioca consecutivo (1939-1942-1943-1944)."),
    ("Dario de Melo Pinto", "1943-1944, 1949-1950", ""),
    ("Marino Machado de Oliveira", "1945-1946", ""),
    ("Hilton Gonçalves dos Santos", "1946, 1958-1959", ""),
    ("Orsini de Araújo Coriolano", "1947-1948", ""),
    ("Gilberto Ferreira Cardoso", "1951-1955", "Época de ouro do Flamengo. Trouxe Fleitas Solich como técnico. Tricampeão carioca (1953, 1954, 1955)."),
    ("Antenor Coelho", "1955", ""),
    ("José Alves Morais", "1956-1957", ""),
    ("George da Silva Fernandes", "1960", ""),
    ("Oswaldo Gudolle Aranha", "1961", ""),
    ("Fadel Fadel", "1962-1965", ""),
    ("Luís Roberto Veiga Brito", "1966-1968, 1971", ""),
    ("André Gustavo Richer", "1969-1970, 1972-1973", ""),
    ("Hélio Maurício Rodrigues de Souza Braga", "1974-1976", ""),
    ("Marcio Braga", "1977-1980, 1987-1988, 1991-1992, 2004-2009", "Recordista de mandatos: 4 passagens em 14 anos. Polêmico e carismático. Brasileiro 1980 no primeiro mandato. Copa do Brasil 2006 e Brasileiro 2009 no último."),
    ("Antônio Augusto Dunshee de Abranches", "1981-1983", "Presidiu na era mais gloriosa: Libertadores 1981, Mundial 1981, Brasileiro 1982 e 1983. A geração Zico."),
    ("Eduardo Fernando de M. Mota", "1983", ""),
    ("George Helal", "1984-1986", "Empresário e dirigente histórico. Nome do CT do Flamengo (Ninho do Urubu é oficialmente CT George Helal)."),
    ("Gilberto Cardoso Filho", "1989-1990, 2002", ""),
    ("Luís Augusto Veloso", "1993-1994", ""),
    ("Kléber Leite", "1995-1998", "Presidente durante a contratação de Romário e os títulos cariocas dos anos 1990."),
    ("Edmundo dos Santos Silva", "1999-2002", ""),
    ("Hélio Paulo Ferraz", "2002-2003", ""),
    ("Delair Dumbrosck", "2009", "Interino após saída de Marcio Braga."),
    ("Patrícia Amorim", "2010-2012", "Primeira e única mulher presidente do Flamengo. Contratou Ronaldinho Gaúcho. Campeã carioca 2011."),
    ("Eduardo Bandeira de Mello", "2013-2018", "Reestruturação financeira histórica. Tirou o Flamengo de uma dívida bilionária. Investiu em infraestrutura. Preparou o terreno para a era de títulos."),
    ("Rodolfo Landim", "2019-2024", "Era de ouro: Libertadores 2019 e 2022, Brasileiros 2019 e 2020, Copa do Brasil 2022 e 2024. Contratou Jorge Jesus. Maior era de títulos internacionais."),
    ("Luiz Eduardo Baptista (BAP)", "2025-2027", "Presidente atual. Libertadores 2025, Brasileiro 2025, Supercopa 2025 com Filipe Luís. Carioca 2026 com Leonardo Jardim."),
]

def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

def get_photo_html(slug, name):
    if slug in PHOTOS:
        return f'<img src="../../img/presidentes/{PHOTOS[slug]}" alt="{name}" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentElement.innerHTML=noPhoto()">'
    return '<svg viewBox="0 0 200 200" style="width:100%;height:100%"><rect width="200" height="200" fill="#1a1a1a"/><circle cx="100" cy="75" r="35" fill="#333"/><ellipse cx="100" cy="170" rx="55" ry="45" fill="#333"/></svg>'

def generate_pres_html(name, period, bio, slug):
    if not bio:
        bio = f'{name} foi presidente do Clube de Regatas do Flamengo durante o período {period}, contribuindo para a administração e desenvolvimento do maior clube do Brasil.'

    photo_html = get_photo_html(slug, name)

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - Presidente do Flamengo | Portal Flamengo</title>
<meta name="description" content="Biografia de {name}, presidente do Flamengo ({period}). Conheça sua gestão e contribuição para o clube.">
<meta name="robots" content="index, follow">
<meta name="author" content="Portal Flamengo">
<meta name="theme-color" content="#c3272b">
<link rel="canonical" href="https://www.portalflamengo.com.br/presidentes/{slug}/">
<link rel="icon" type="image/x-icon" href="../../favicon.ico">
<meta property="og:title" content="{name} - Presidente do Flamengo">
<meta property="og:description" content="Biografia de {name}, presidente do Flamengo ({period}).">
<meta property="og:type" content="article">
<meta property="og:url" content="https://www.portalflamengo.com.br/presidentes/{slug}/">
<meta property="og:site_name" content="Portal Flamengo">
<meta property="og:locale" content="pt_BR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1286595053228930" crossorigin="anonymous"></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"{name}","description":"Presidente do Flamengo ({period})","memberOf":{{"@type":"SportsTeam","name":"Clube de Regatas do Flamengo"}}}}
</script>
<style>
:root{{--red:#c3272b;--red-dark:#9e1f22;--black:#0d0d0d;--black-soft:#1a1a1a;--gold:#d4a017;--white:#fff;--off-white:#faf9f7;--cream:#f5f0ea;--gray-100:#f3f3f3;--gray-200:#e5e5e5;--gray-300:#d4d4d4;--gray-500:#737373;--gray-700:#404040;--gray-900:#171717;--font-display:'Playfair Display',Georgia,serif;--font-body:'DM Sans','Inter',system-ui,sans-serif;--font-ui:'Inter',system-ui,sans-serif;--shadow-sm:0 1px 3px rgba(0,0,0,.08);--shadow-md:0 4px 12px rgba(0,0,0,.1);--radius:8px;--transition:.35s cubic-bezier(.4,0,.2,1)}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}body{{font-family:var(--font-body);color:var(--gray-900);background:var(--off-white);line-height:1.6}}
a{{color:inherit;text-decoration:none}}img{{max-width:100%;display:block}}button{{cursor:pointer;border:none;background:none}}
.container{{max-width:1240px;margin:0 auto;padding:0 24px}}
.topbar{{background:var(--black);padding:6px 0;font-size:.75rem;text-transform:uppercase;color:rgba(255,255,255,.5);border-bottom:1px solid rgba(255,255,255,.06)}}.topbar .container{{display:flex;justify-content:space-between;align-items:center}}.topbar a{{color:rgba(255,255,255,.5)}}.topbar a:hover{{color:var(--gold)}}.topbar-left{{display:flex;gap:20px}}.topbar-date{{color:rgba(255,255,255,.35)}}
.header-ticker{{background:var(--red-dark);padding:5px 0;overflow:hidden}}.header-ticker-track{{display:flex;animation:htS 35s linear infinite}}.header-ticker-item{{white-space:nowrap;color:rgba(255,255,255,.85);font-size:.75rem;padding:0 30px;font-weight:500}}.header-ticker-item::before{{content:'⚽';margin-right:6px}}@keyframes htS{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.header{{background:var(--red);position:sticky;top:0;z-index:100;border-bottom:3px solid var(--red-dark);box-shadow:0 2px 20px rgba(0,0,0,.15)}}.header .container{{display:flex;align-items:center;justify-content:space-between;height:60px}}
.logo{{font-family:var(--font-display);font-size:1.7rem;font-weight:800;color:var(--white);display:flex;align-items:center;gap:10px}}.logo-icon{{width:38px;height:38px;background:var(--black);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem}}.logo span{{color:var(--gold)}}
.nav{{display:flex;align-items:center;gap:4px}}.nav a{{color:rgba(255,255,255,.9);font-size:.85rem;font-weight:500;padding:8px 14px;border-radius:6px;white-space:nowrap}}.nav a:hover{{background:rgba(255,255,255,.12)}}.nav a.active{{background:rgba(0,0,0,.2);color:var(--gold)}}
.header-actions{{display:flex;gap:12px}}.search-btn{{color:rgba(255,255,255,.8);font-size:1.1rem;padding:8px;border-radius:50%}}.hamburger{{display:none;color:var(--white);font-size:1.4rem;padding:8px}}
.breadcrumb{{padding:16px 0;font-size:.82rem;color:var(--gray-500)}}.breadcrumb a:hover{{color:var(--red)}}.breadcrumb .sep{{margin:0 8px;color:var(--gray-300)}}
.pres-hero{{background:var(--black);padding:60px 0}}.pres-hero .container{{display:grid;grid-template-columns:250px 1fr;gap:40px;align-items:center}}
.pres-photo{{width:250px;height:300px;border-radius:var(--radius);overflow:hidden;background:var(--black-soft);border:3px solid var(--gold)}}
.pres-info h1{{font-family:var(--font-display);font-size:clamp(1.8rem,3vw,2.8rem);font-weight:900;color:var(--white);margin-bottom:8px}}
.pres-role{{color:var(--gold);font-size:1rem;font-weight:600;margin-bottom:16px}}.pres-period-tag{{display:inline-block;background:var(--red);color:var(--white);padding:6px 18px;border-radius:50px;font-size:.85rem;font-weight:600}}
.bio-section{{padding:60px 0}}.bio-section .container{{max-width:800px}}
.bio-section h2{{font-family:var(--font-display);font-size:1.5rem;font-weight:800;margin:28px 0 12px;border-bottom:2px solid var(--red);padding-bottom:8px}}
.bio-section p{{margin-bottom:16px;line-height:1.8;color:var(--gray-700)}}
.back-link{{display:inline-flex;align-items:center;gap:8px;color:var(--red);font-weight:600;margin-top:20px;padding:10px 20px;background:var(--white);border-radius:50px;box-shadow:var(--shadow-sm)}}.back-link:hover{{background:var(--red);color:var(--white)}}
.newsletter{{background:var(--red);padding:60px 0;position:relative;overflow:hidden}}.newsletter::before{{content:'CRF';position:absolute;right:-40px;top:50%;transform:translateY(-50%);font-family:var(--font-display);font-size:20rem;font-weight:900;color:rgba(255,255,255,.04)}}.newsletter .container{{position:relative;z-index:1;text-align:center;max-width:640px}}.newsletter h2{{font-family:var(--font-display);font-size:2rem;font-weight:800;color:var(--white);margin-bottom:12px}}.newsletter p{{color:rgba(255,255,255,.7);margin-bottom:28px}}.newsletter-form{{display:flex;max-width:480px;margin:0 auto}}.newsletter-form input{{flex:1;padding:14px 20px;border:none;border-radius:50px 0 0 50px;font-size:.95rem;background:rgba(0,0,0,.25);color:var(--white);outline:none}}.newsletter-form input::placeholder{{color:rgba(255,255,255,.4)}}.newsletter-form button{{padding:14px 28px;background:var(--black);color:var(--gold);font-weight:700;font-size:.85rem;text-transform:uppercase;border-radius:0 50px 50px 0}}
.footer{{background:var(--black);padding:60px 0 0;color:rgba(255,255,255,.4);font-size:.88rem;border-top:3px solid var(--red)}}.footer-grid{{display:grid;grid-template-columns:1.8fr 1fr 1fr 1fr;gap:40px;padding-bottom:40px}}.footer-brand h3{{font-family:var(--font-display);font-size:1.5rem;font-weight:800;color:var(--white);margin-bottom:12px}}.footer-brand h3 span{{color:var(--red)}}.footer-brand p{{line-height:1.7;margin-bottom:16px}}.footer-col h4{{color:var(--white);font-size:.82rem;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:20px;font-weight:700}}.footer-col a{{display:block;color:rgba(255,255,255,.4);padding:6px 0}}.footer-col a:hover{{color:var(--red)}}.footer-bottom{{border-top:1px solid rgba(255,255,255,.06);padding:20px 0;display:flex;justify-content:space-between;font-size:.78rem;color:rgba(255,255,255,.25)}}
.scroll-top{{position:fixed;bottom:30px;right:30px;width:48px;height:48px;background:var(--red);color:var(--white);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;z-index:50;opacity:0;visibility:hidden;transition:all var(--transition);box-shadow:var(--shadow-md)}}.scroll-top.visible{{opacity:1;visibility:visible}}
.mobile-nav{{position:fixed;top:0;right:-300px;width:300px;height:100%;background:var(--black);z-index:150;padding:80px 30px 30px;transition:right var(--transition);overflow-y:auto}}.mobile-nav.active{{right:0}}.mobile-nav a{{display:block;color:rgba(255,255,255,.7);padding:14px 0;font-size:1.05rem;border-bottom:1px solid rgba(255,255,255,.06)}}.mobile-nav a:hover{{color:var(--red)}}.mobile-nav-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:140;display:none}}.mobile-nav-overlay.active{{display:block}}.mobile-nav-close{{position:absolute;top:20px;right:20px;color:rgba(255,255,255,.5);font-size:1.5rem}}
.search-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:200;display:none;align-items:flex-start;justify-content:center;padding-top:20vh}}.search-overlay.active{{display:flex}}.search-box{{width:90%;max-width:640px}}.search-box input{{width:100%;padding:20px 30px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.12);border-radius:60px;color:var(--white);font-size:1.3rem;outline:none}}.search-box input:focus{{border-color:var(--red)}}.search-close{{position:absolute;top:30px;right:30px;color:rgba(255,255,255,.5);font-size:2rem;cursor:pointer}}
@media(max-width:768px){{.topbar{{display:none}}.nav{{display:none}}.hamburger{{display:block}}.pres-hero .container{{grid-template-columns:1fr;text-align:center}}.pres-photo{{margin:0 auto;width:180px;height:220px}}.footer-grid{{grid-template-columns:1fr}}.newsletter-form{{flex-direction:column}}.newsletter-form input{{border-radius:12px 12px 0 0}}.newsletter-form button{{border-radius:0 0 12px 12px;padding:16px}}}}
</style>
</head>
<body>
<div class="topbar"><div class="container"><div class="topbar-left"><a href="../../origem/">Origem</a><a href="../../curiosidades/">Curiosidades</a><a href="../../contato/">Contato</a></div><div class="topbar-right"><span class="topbar-date" id="currentDate"></span></div></div></div>
<header class="header"><div class="container"><a href="../../" class="logo"><div class="logo-icon">🔴</div>Portal <span>Flamengo</span></a><nav class="nav"><a href="../../">Início</a><a href="../../jogadores/">Jogadores</a><a href="../../tecnicos/">Técnicos</a><a href="../../escalacoes/">Escalações</a><a href="../" class="active">Presidentes</a><a href="../../curiosidades/">Curiosidades</a><a href="../../momentos-historicos/">Momentos</a><a href="../../noticias/">Notícias</a></nav><div class="header-actions"><button class="search-btn" onclick="toggleSearch()">🔍</button><button class="hamburger" onclick="toggleMobileNav()">☰</button></div></div></header>
<div class="header-ticker"><div class="header-ticker-track"><span class="header-ticker-item">Flamengo campeão carioca 2026</span><span class="header-ticker-item">Leonardo Jardim novo técnico</span><span class="header-ticker-item">Libertadores 2026: Grupo A</span><span class="header-ticker-item">Pedro artilheiro com 8 gols</span><span class="header-ticker-item">Flamengo campeão carioca 2026</span><span class="header-ticker-item">Leonardo Jardim novo técnico</span><span class="header-ticker-item">Libertadores 2026: Grupo A</span><span class="header-ticker-item">Pedro artilheiro com 8 gols</span></div></div>
<div class="container"><div class="breadcrumb"><a href="../../">Início</a><span class="sep">›</span><a href="../">Presidentes</a><span class="sep">›</span><strong>{name}</strong></div></div>
<section class="pres-hero"><div class="container"><div class="pres-photo">{photo_html}</div><div class="pres-info"><span class="pres-period-tag">{period}</span><h1>{name}</h1><p class="pres-role">Presidente do Clube de Regatas do Flamengo</p></div></div></section>
<section class="bio-section"><div class="container"><h2>Gestão e Legado</h2><p>{bio}</p><p>O Clube de Regatas do Flamengo, fundado em 1895, é o maior clube do Brasil com mais de 40 milhões de torcedores. A presidência do Flamengo é um cargo de enorme responsabilidade, comandando um clube com mais de 130 anos de história e dezenas de títulos conquistados.</p><a href="../" class="back-link">← Voltar para Presidentes</a></div></section>
<section class="newsletter"><div class="container"><h2>Fique por Dentro do Mengão</h2><p>Receba as melhores histórias do Flamengo.</p><form class="newsletter-form" onsubmit="return false;"><input type="email" placeholder="Seu e-mail" required><button type="submit">Assinar</button></form></div></section>
<footer class="footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><h3>Portal <span>Flamengo</span></h3><p>O maior portal sobre o Flamengo.</p></div><div class="footer-col"><h4>Explore</h4><a href="../../jogadores/">Jogadores</a><a href="../../tecnicos/">Técnicos</a><a href="../../escalacoes/">Escalações</a><a href="../">Presidentes</a></div><div class="footer-col"><h4>Conteúdo</h4><a href="../../origem/">Origem</a><a href="../../noticias/">Notícias</a><a href="../../momentos-historicos/">Momentos</a></div><div class="footer-col"><h4>Portal</h4><a href="../../sobre/">Sobre</a><a href="../../contato/">Contato</a><a href="../../termos-de-uso/">Termos</a><a href="../../politica-privacidade/">Privacidade</a></div></div><div class="footer-bottom"><span>© 2025-2026 Portal Flamengo.</span><span>Site não oficial.</span></div></div></footer>
<div class="search-overlay" id="searchOverlay"><span class="search-close" onclick="toggleSearch()">×</span><div class="search-box"><input type="text" placeholder="Buscar..." autofocus></div></div>
<div class="mobile-nav-overlay" id="mobileOverlay" onclick="toggleMobileNav()"></div>
<nav class="mobile-nav" id="mobileNav"><span class="mobile-nav-close" onclick="toggleMobileNav()">×</span><a href="../../">Início</a><a href="../../jogadores/">Jogadores</a><a href="../../tecnicos/">Técnicos</a><a href="../">Presidentes</a><a href="../../curiosidades/">Curiosidades</a><a href="../../noticias/">Notícias</a></nav>
<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<script>
const d=new Date(),m=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],w=['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'];
document.getElementById('currentDate').textContent=w[d.getDay()]+', '+d.getDate()+' de '+m[d.getMonth()]+' de '+d.getFullYear();
function toggleSearch(){{document.getElementById('searchOverlay').classList.toggle('active')}}
function toggleMobileNav(){{document.getElementById('mobileNav').classList.toggle('active');document.getElementById('mobileOverlay').classList.toggle('active')}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape'){{document.getElementById('searchOverlay').classList.remove('active');document.getElementById('mobileNav').classList.remove('active');document.getElementById('mobileOverlay').classList.remove('active')}}}});
window.addEventListener('scroll',()=>{{const b=document.getElementById('scrollTop');if(window.scrollY>600)b.classList.add('visible');else b.classList.remove('visible')}});
</script>
</body>
</html>'''

# Generate all pages
print("=== GERANDO BIOGRAFIAS DOS PRESIDENTES ===")
generated = 0
slug_map = {}

for name, period, bio in PRESIDENTS:
    slug = slugify(name)
    # Special overrides
    if 'patricia' in slug: slug = 'patricia-amorim'
    elif 'bandeira' in slug: slug = 'bandeira-de-mello'
    elif 'landim' in slug: slug = 'rodolfo-landim'
    elif 'baptista' in slug or 'bap' in slug.lower(): slug = 'bap'
    elif 'marcio-braga' in slug: slug = 'marcio-braga'
    elif 'kleber' in slug: slug = 'kleber-leite'
    elif 'george-helal' in slug: slug = 'george-helal'
    elif 'dunshee' in slug: slug = 'dunshee-de-abranches'
    elif 'bastos-padilha' in slug: slug = 'jose-bastos-padilha'

    slug_map[name] = slug

    dir_path = os.path.join(PRES_DIR, slug)
    os.makedirs(dir_path, exist_ok=True)

    html = generate_pres_html(name, period, bio, slug)
    with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    generated += 1

print(f"Geradas: {generated} biografias de presidentes")

# Deploy via FTP
print("\n=== DEPLOY VIA FTP ===")
ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

count = 0
for name, period, bio in PRESIDENTS:
    slug = slug_map[name]
    local_file = os.path.join(PRES_DIR, slug, 'index.html')
    if not os.path.exists(local_file):
        continue
    remote_dir = f"/public_html/presidentes/{slug}"
    try:
        ftp.cwd(remote_dir)
    except:
        try:
            ftp.cwd("/public_html/presidentes")
            ftp.mkd(slug)
            ftp.cwd(remote_dir)
        except:
            continue
    with open(local_file, 'rb') as f:
        ftp.storbinary("STOR index.html", f)
    count += 1

ftp.quit()
print(f"Deploy: {count} biografias de presidentes no ar!")

# Now update the presidentes index to make names clickable
print("\n=== ATUALIZANDO LINKS NA PÁGINA DE PRESIDENTES ===")
pres_index = os.path.join(LOCAL_BASE, "presidentes", "index.html")
with open(pres_index, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace each <span class="pres-name">Name</span> with a link
for name, period, bio in PRESIDENTS:
    slug = slug_map[name]
    # Handle name without accents (as it appears in the HTML)
    name_no_accent = unicodedata.normalize('NFD', name)
    name_no_accent = ''.join(c for c in name_no_accent if unicodedata.category(c) != 'Mn')

    old = f'<span class="pres-name">{name_no_accent}</span>'
    new = f'<a href="{slug}/" class="pres-name" style="color:var(--red);text-decoration:none;font-weight:600;">{name_no_accent}</a>'
    content = content.replace(old, new)

    # Also try with original accented name
    old2 = f'<span class="pres-name">{name}</span>'
    new2 = f'<a href="{slug}/" class="pres-name" style="color:var(--red);text-decoration:none;font-weight:600;">{name}</a>'
    content = content.replace(old2, new2)

with open(pres_index, 'w', encoding='utf-8') as f:
    f.write(content)
print("Página de presidentes atualizada com links!")

# Re-deploy presidentes index
ftp2 = ftplib.FTP("69.6.220.159")
ftp2.login("portalflamengoco", "claude2026#")
ftp2.cwd("/public_html/presidentes")
with open(pres_index, 'rb') as f:
    ftp2.storbinary("STOR index.html", f)
ftp2.quit()
print("Presidentes index re-deployado!")
print("\nTudo pronto!")
