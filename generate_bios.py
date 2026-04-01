#!/usr/bin/env python3
"""
Gerador de biografias para TODOS os 756 jogadores do Portal Flamengo.
Gera páginas HTML individuais no padrão do template do Zico.
"""
import os, json, re, unicodedata, ftplib

LOCAL_BASE = os.path.expanduser("~/Claudinho/projetos/portal-flamengo")
JOGADORES_DIR = os.path.join(LOCAL_BASE, "jogadores")

# ============================================================
# DADOS DOS JOGADORES (756 da Wikipedia)
# ============================================================

# Jogadores que JÁ têm biografia manual (não sobrescrever)
SKIP = {
    'zico','gabigol','romario','junior','leonidas','garrincha',
    'adriano','petkovic','vinicius-junior','ronaldinho-gaucho',
    'arrascaeta','pedro','bruno-henrique','everton-ribeiro',
    'adilio','leandro','nunes','mozer','david-luiz','filipe-luis'
}

# Fotos locais disponíveis (slug -> filename)
PHOTOS = {
    'andreas-pereira':'andreas-pereira.jpg','arrascaeta':'arrascaeta.jpg',
    'arturo-vidal':'arturo-vidal.jpg','ayrton-lucas':'ayrton-lucas.jpg',
    'bebeto':'bebeto.jpg','cafu':'cafu.jpg','david-luiz':'david-luiz.jpg',
    'diego-alves':'diego-alves.jpg','diego-ribas':'diego-ribas.jpg',
    'djalminha':'djalminha.jpg','domingos-da-guia':'domingos-da-guia.jpg',
    'emerson-sheik':'emerson-sheik.jpg','everton-ribeiro':'everton-ribeiro.jpg',
    'felipe-melo':'felipe-melo.png','filipe-luis':'filipe-luis.jpg',
    'gabigol':'gabigol.jpg','garrincha':'garrincha.jpg',
    'jair-rosa-pinto':'jair-rosa-pinto.jpg','leo-moura':'leo-moura.jpg',
    'leonidas':'leonidas.jpg','lucas-paqueta':'lucas-paqueta.jpg',
    'matheus-franca':'matheus-franca.jpg','mozer':'mozer.jpg',
    'paolo-guerrero':'paolo-guerrero.jpg','petkovic':'petkovic.png',
    'rodrigo-caio':'rodrigo-caio.jpg','romario':'romario.jpg',
    'ronaldao':'ronaldao.jpg','ronaldinho-gaucho':'ronaldinho-gaucho.jpg',
    'ronaldo-angelim':'ronaldo-angelim.jpg','socrates':'socrates.jpg',
    'thiago-maia':'thiago-maia.jpg','vagner-love':'vagner-love.jpg',
    'vinicius-junior':'vinicius-junior.jpg','willian-arao':'willian-arao.jpg',
    'zico':'zico.jpg','zizinho':'zizinho.jpg',
}

# Dados detalhados dos jogadores mais conhecidos
PLAYER_DATA = {
    'bebeto': {'full':'José Roberto Gama de Oliveira','nick':'Bebeto','pos':'Atacante','born':'16 fev 1964, Salvador-BA','period':'1983-1989','games':'~250','goals':'~123','titles':'Carioca 1986','bio':'Revelado no Flamengo, Bebeto se tornou um dos maiores atacantes do Brasil. Campeão do mundo em 1994 pela Seleção. No Flamengo, formou dupla letal e foi artilheiro. Depois brilhou no Vasco, Deportivo La Coruña e Seleção.'},
    'cafu': {'full':'Marcos Evangelista de Moraes','nick':'Cafu','pos':'Lateral-direito','born':'7 jun 1970, São Paulo-SP','period':'2000-2001','games':'~30','goals':'~1','titles':'—','bio':'O Pendolino, maior lateral-direito da história. Passou brevemente pelo Flamengo em 2000-2001. Bicampeão mundial com a Seleção (1994, 2002). Carreira brilhante na Roma e Milan.'},
    'socrates': {'full':'Sócrates Brasileiro Sampaio de Souza Vieira de Oliveira','nick':'Sócrates','pos':'Meia','born':'19 fev 1954, Belém-PA','died':'4 dez 2011','period':'1986','games':'~16','goals':'~4','titles':'—','bio':'O Doutor. Ídolo do Corinthians e da Democracia Corinthiana. Passou brevemente pelo Flamengo em 1986. Intelectual, médico e gênio do futebol. Seleção Brasileira em 2 Copas do Mundo.'},
    'domingos-da-guia': {'full':'Domingos Antônio da Guia','nick':'Domingos da Guia','pos':'Zagueiro','born':'19 nov 1912, Rio de Janeiro','died':'18 mai 2000','period':'1935-1937, 1943-1948','games':'~200','goals':'~5','titles':'Carioca 1939, 1942, 1943, 1944','bio':'O Divino Mestre. Considerado o primeiro grande zagueiro do futebol brasileiro. Revolucionou a posição com elegância e técnica. Ídolo do Flamengo nos anos 1930-40.'},
    'zizinho': {'full':'Thomaz Soares da Silva','nick':'Zizinho','pos':'Meia','born':'14 set 1921, São Gonçalo-RJ','died':'8 fev 2002','period':'1939-1950','games':'~352','goals':'~148','titles':'Carioca 1939, 1942, 1943, 1944','bio':'Considerado por Pelé o maior jogador que já viu. Meia genial do Flamengo nos anos 1940. Artilheiro e craque absoluto. Copa do Mundo 1950 (vice). Um dos maiores da história do futebol brasileiro.'},
    'djalminha': {'full':'Djalma Feitosa Dias','nick':'Djalminha','pos':'Meia','born':'9 jan 1970, São Paulo-SP','period':'1993-1995','games':'~80','goals':'~20','titles':'—','bio':'Meia habilidoso e driblador nato. Passou pelo Flamengo antes de brilhar no Deportivo La Coruña na Espanha. Filho de Djalma Dias.'},
    'diego-ribas': {'full':'Diego Ribas da Cunha','nick':'Diego','pos':'Meia','born':'28 fev 1985, Ribeirão Preto-SP','period':'2016-2022','games':'~300','goals':'~50','titles':'Libertadores 2019, Brasileiro 2019, 2020, Cariocas','bio':'O camisa 10. Veio do Fenerbahçe. Líder dentro e fora de campo. Presente em todas as conquistas de 2019 a 2022. Elegância e visão de jogo.'},
    'vagner-love': {'full':'Vágner Silva de Souza','nick':'Vágner Love','pos':'Atacante','born':'11 jun 1984, Rio de Janeiro','period':'2012-2014','games':'~80','goals':'~30','titles':'Copa do Brasil 2013','bio':'Atacante veloz e goleador. Fez sucesso no CSKA Moscou antes de chegar ao Flamengo. Fundamental na Copa do Brasil 2013.'},
    'emerson-sheik': {'full':'Márcio Passos de Albuquerque','nick':'Emerson Sheik','pos':'Atacante','born':'14 dez 1978, Brasília-DF','period':'2011-2013','games':'~120','goals':'~45','titles':'Carioca 2011','bio':'Atacante polêmico e goleador. Passou por Flamengo, Corinthians, Al Ain e Botafogo. Faro de gol e personalidade forte.'},
    'felipe-melo': {'full':'Felipe Melo de Carvalho','nick':'Felipe Melo','pos':'Volante','born':'26 jun 1983, Volta Redonda-RJ','period':'2022-2024','games':'~80','goals':'~3','titles':'Libertadores 2022, Copa do Brasil 2022','bio':'Volante raçudo e polêmico. Carreira na Juventus, Inter de Milão, Galatasaray. Chegou ao Flamengo com experiência e garra.'},
    'arturo-vidal': {'full':'Arturo Erasmo Vidal Pardo','nick':'Arturo Vidal','pos':'Meia/Volante','born':'22 mai 1987, Santiago, Chile','period':'2022-2023','games':'~40','goals':'~3','titles':'Libertadores 2022','bio':'O King. Meio-campista chileno com passagem por Juventus, Bayern, Barcelona e Inter. Raça e liderança no Flamengo.'},
    'andreas-pereira': {'full':'Andreas Hugo Hoelgebaum Pereira','nick':'Andreas Pereira','pos':'Meia','born':'1 jan 1996, Duffel, Bélgica','period':'2022-presente','games':'~130','goals':'~15','titles':'Libertadores 2022, Copa do Brasil 2022, 2024','bio':'Meia belgo-brasileiro formado no Manchester United. Qualidade técnica e versatilidade. Peça importante do elenco atual.'},
    'lucas-paqueta': {'full':'Lucas Tolentino Coelho de Lima','nick':'Lucas Paquetá','pos':'Meia','born':'27 ago 1997, Rio de Janeiro','period':'2017-2019, 2026-presente','games':'~80','goals':'~15','titles':'—','bio':'Revelação da base do Flamengo. Vendido ao Milan, depois Lyon e West Ham. Retornou ao Flamengo em 2026. Seleção Brasileira.'},
    'ronaldo-angelim': {'full':'Ronaldo Angelim de Moura','nick':'Ronaldo Angelim','pos':'Zagueiro','born':'6 mar 1981, Quixadá-CE','period':'2004-2012','games':'~280','goals':'~10','titles':'Brasileiro 2009, Copa do Brasil 2006, Cariocas','bio':'Zagueiro raçudo e ídolo da torcida. Gol decisivo no Brasileiro 2009. Cearense que conquistou o Rio.'},
    'leo-moura': {'full':'Leonardo de Souza Moura','nick':'Léo Moura','pos':'Lateral-direito','born':'21 mai 1978, Rio de Janeiro','period':'2005-2015','games':'~480','goals':'~35','titles':'Brasileiro 2009, Copa do Brasil 2006, 2013, Cariocas','bio':'Um dos maiores laterais da história do Flamengo. Mais de 480 jogos. Raça e qualidade ofensiva. Ídolo da torcida.'},
    'ayrton-lucas': {'full':'Ayrton Lucas Dantas de Medeiros','nick':'Ayrton Lucas','pos':'Lateral-esquerdo','born':'19 jun 1997, Belford Roxo-RJ','period':'2023-presente','games':'~130','goals':'~10','titles':'Copa do Brasil 2024, Libertadores 2025, Carioca 2024','bio':'Lateral ofensivo com velocidade explosiva. Veio do Spartak Moscou. Titular absoluto do Flamengo atual.'},
    'diego-alves': {'full':'Diego Alves Carreira','nick':'Diego Alves','pos':'Goleiro','born':'24 jun 1985, São Paulo-SP','period':'2017-2023','games':'~260','goals':'0','titles':'Libertadores 2019, 2022, Brasileiro 2019, 2020','bio':'O paredão. Pegador de pênaltis. Veio do Valencia. Fundamental nas conquistas de 2019 e 2022. Um dos melhores goleiros da história do Flamengo.'},
    'rodrigo-caio': {'full':'Rodrigo Caio Coquette Russo','nick':'Rodrigo Caio','pos':'Zagueiro','born':'17 ago 1993, São Paulo-SP','period':'2019-2024','games':'~130','goals':'~5','titles':'Libertadores 2019, Brasileiro 2019, 2020','bio':'Zagueiro elegante e seguro. Peça fundamental da defesa de Jorge Jesus em 2019. Problemas com lesões marcaram sua passagem.'},
    'willian-arao': {'full':'Willian Souza Arão da Silva','nick':'Willian Arão','pos':'Volante','born':'12 mar 1992, Santo André-SP','period':'2016-2022','games':'~340','goals':'~30','titles':'Libertadores 2019, 2022, Brasileiro 2019, 2020','bio':'Volante versátil e inteligente. Mais de 340 jogos. Presente em todas as conquistas recentes. Também atuou como zagueiro.'},
    'thiago-maia': {'full':'Thiago Maia Alencar','nick':'Thiago Maia','pos':'Volante','born':'31 mar 1997, Boa Vista-RR','period':'2020-2024','games':'~200','goals':'~5','titles':'Brasileiro 2020, Libertadores 2022, Copa do Brasil 2022','bio':'Volante combativo e recuperador de bolas. Veio emprestado do Lille e foi comprado em definitivo. Peça importante do meio-campo.'},
    'ronaldao': {'full':'Ronaldo Alves Feitosa','nick':'Ronaldão','pos':'Zagueiro','born':'13 ago 1965, Areia Branca-RN','period':'1988-1992','games':'~150','goals':'~10','titles':'Copa do Brasil 1990, Brasileiro 1992','bio':'Zagueirão forte e seguro. Copa do Mundo 1994 pela Seleção. No Flamengo, foi titular na Copa do Brasil 1990 e no Brasileiro 1992.'},
    'matheus-franca': {'full':'Matheus Gonçalves França','nick':'Matheus França','pos':'Meia','born':'1 mai 2004, Rio de Janeiro','period':'2022-2023','games':'~50','goals':'~5','titles':'Libertadores 2022','bio':'Joia da base do Flamengo. Vendido ao Crystal Palace da Inglaterra. Talento precoce que chamou atenção de clubes europeus.'},
    'jair-rosa-pinto': {'full':'Jair Rosa Pinto','nick':'Jair','pos':'Atacante','born':'21 ago 1921, São Paulo-SP','died':'26 jan 2005','period':'1944-1950','games':'~150','goals':'~80','titles':'Carioca 1944','bio':'Um dos grandes atacantes do Flamengo nos anos 1940. Velocidade e faro de gol. Seleção Brasileira na Copa de 1950.'},
    'paolo-guerrero': {'full':'José Paolo Guerrero Gonzales','nick':'Paolo Guerrero','pos':'Centroavante','born':'1 jan 1984, Lima, Peru','period':'2018','games':'~4','goals':'~1','titles':'—','bio':'Ídolo peruano, artilheiro histórico da Seleção do Peru. Passagem breve pelo Flamengo em 2018 antes de ir para o Internacional.'},
}

# Lista COMPLETA de todos os 756 jogadores
ALL_PLAYERS = """Adalberto Machado,Adalberto Melo,Adão Nunes,Ademar Pantera,Adílio,Adílson Heleno,Adílson José Pinto,Adílton,Adriano Imperador,Adryan,Afonsinho,Afonso Guimarães,Agnelo dos Santos,Ailton Ferraz,Aírton Beleza,Airton Ravagniani,Airton Ribeiro Santos,Alan Patrick,Alanzinho,Alberto Borgerth,Alberto Leguelé,Alberto Pereira Pires,Alberto Valentim,Carlos Alcaraz,Alcindo Sartori,Alcir Fonseca,Aldair,Alecsandro,Aleílson,Alexsandro de Souza,Alessandro,Alessandro Nunes,Alex Cruz,Alex Sandro,Alex Sandro da Silva,Alexandre Gaúcho,Alfredo dos Santos,Alfredo Willemsens,Allan,Almir Luna,Almir Pernambuquinho,Aloísio Chulapa,Aluísio Francisco,Álvaro Aquino,Amarildo,Amauri da Silva,Américo Murolo,Amoroso,Ananias Cruz,Anderson Alves,Anderson Pico,Anderson Cardoso,André Bahia,André Cruz,André Gomes,André Gonçalves,André Lima Pedro,André Santos,Andreas Pereira,Andrei Frascarelli,Anselmo,Toninho,Antonio Caio,Antônio Capocasali,Toninho Baiano,Dourado,Antônio Marcos,Antônio Nunes,Araken Patusca,Ariel Nogueira,Arinélson,Armando de Almeida,Pablo Armero,Arnaldo Guimarães,Artêmio Sarcinelli,Arthur Caíke,Arthur Friedenreich,Arthur Maia,Artigas,Athirson,Augusto Recife,Mehmet Aurélio,Ayrton Lucas,Ayrton Ganino,Bala,Baltazar,Bebeto,Beijoca,Jorge Benítez,Natan Bernardo,Orlando Berrío,Beto Bacamarte,Maxi Biancucchi,Bigode,Bigu,Biguá,Bolero,Claudio Borghi,Cristian Borja,Darío Bottinelli,Branco,Bressan,Aluspah Brewah,Modesto Bría,Brito,Bruno Lazaroni,Bruno Cabrerizo,Bruninho,Bruno Carvalho,Bruno Henrique,Bruno Mezenga,Bruno Quadros,Bruno Viana,Fabrício Bruno,Buião,Cabralzinho,Cacaio,Víctor Cáceres,Cafu,Caíco,Caio Cambalhota,Caio Ribeiro,Camacho,Camilo Nogueira,Candiota,Héctor Canteros,Carlinhos,Carlinhos Violino,Carlos Alberto Junior,Carlos Alberto Dias,Carlos Alberto Sotelho,Carlos Alberto Torres,Carlos César,Dionísio,Carlos Eduardo,Carlos Honório,Carlos Kaiser,Chiquinho Carlos,Jorge Carrascal,Cássio José,Evanivaldo Castro,Pablo Castro,Célio Silva,César Dutra,César Martins,Charles Fabian,Charles Guerreiro,Chiquinho Carioca,Chiquinho Pastor,Claiton,Cláudio Adão,Cláudio Guadagno,Claudiomiro,Cléber Santana,Cleisson,Cleiton Santana,Cléo Hickman,Clodoaldo Caldeira,Cocada,Hugo Colace,Darío Conca,Coriolano Paula,Corrêa,Cristian Baroni,Gustavo Cuéllar,Da Silva,Dalbert,Danilo Luiz,Dadá Maravilha,David Braz,David Luiz,Giorgian de Arrascaeta,Nicolás de la Cruz,Décio Crespo,Deivid de Souza,Denílson,Dênis Marques,Dida,Dido,Diego da Silva,Diego Silva,Diego Maurício,Diego Ribas,Diego Souza,Diego Tardelli,Dill,Dimba,Dino,Diogo Luís Santo,Diogo Oliveira,Ditão,Djair Kaye,Djalminha,Doca,Domingos da Guia,Donah,Alejandro Donatti,Douglas Baggio,Douglas Silva,Éder Lopes,Éder Luiz,Ederson Campos,Edílson Capetinha,Baroninho,Edinho Nazareth,Edmar Bernardes,Edmundo,Eduardo Coimbra,Eduardo da Silva,Egídio,Elano,Eli Carlos,Elias Mendes,Eltinho,Elton Rodrigues,Emerson Moisés,Emerson Royal,Emerson Silva,Emerson Sheik,Emmanuel Nery,Frickson Erazo,Erick Flores,Espíndola,Evandro Gama,Evaristo de Macedo,Vevé,Éverton Cardoso,Everton Cebolinha,Éverton Ribeiro,Éverton Silva,Evertton Araújo,Fabão,Fabiano Viegas,Fabiano Eller,Fabiano Oliveira,Fabinho Soldado,Fábio Augusto,Fábio Júnior,Fábio Luciano,Fábio Azevedo,Fábio Baiano,Fabrício,Fausto dos Santos,Feijão,Felipe Dias,Felipe Maestro,Felipe Melo,Felipe Vizeu,Fellype Gabriel,Fernando Baiano,Fernando César,Fernando Diniz,Fernando Gomes,Fernando Henrique,Fernando Santos,Gonzalo Fierro,Cláudio Figueiredo,Filipe Luís,Ubaldo Fillol,Fio Maravilha,Flávio Barros,Flávio Campos,Flávio Costa,Flávio Pinho,Francisco Aramburu,Francisco Sousa,Frauches,Fred Rodrigues,Fumanchu,Gabigol,Gabriel,Carlos Gamarra,Garrincha,Gaúcho,Diego Gavilán,Gélson Baresi,Geraldo Assoviador,Geraldo José,Gérson Magrão,Gérson,Gerson Santos,Geuvânio,Gilberto Ribeiro,Gilberto Melo,Gildo Cunha,Gilmar Jorge,Gilmar Popoca,Gláucio,Alfredo González,Marcos González,Gradim,Paolo Guerrero,Guga,Walter Guimarães,Gustavo Henrique,Héctor Parra,Heitor Camarin,Heitor Canalli,Henrique Dourado,Henrique Frade,Henry Welfare,Hermínio de Brito,Hernane Brocador,Heyder Palheta,Hugo Henrique,Hugo Moura,Humberto,Humberto de Araújo,Humberto Monteiro,Ibson Barreto,Igor Jesus,Ígor Castro,Igor Sartori,Índio Ferreira,Iranildo,Irineu,Mauricio Isla,Itamar Batista,Ivo Soares,Jacenir Silva,Jadir,Jael,Jaime de Almeida,Jair Bala,Jair Pereira,Jair Rosa Pinto,Jajá Coelho,James Calvert,Jamir,Jarbas Batista,Jayme de Almeida,Jean Narde,Jean Lucas,João Crevelim,João Daniel,João Francisco,João Gomes,João Lucas,João Paulo Gomes,João Paulo,João Victor,Joel Martins,Jonas Gomes,Jônatas Domingos,Jordan da Costa,Jorge de Amorim,Jorge Ferreira,Jorge Luís Andrade,Jorge Luiz,Jorge Luiz Frello,Jorge Luiz Pereira,Jorge Marcelo,Jorge Marco Moraes,Júnior Carioca,José Carlos Nascimento,José Eurípedes,José Fernando Viana,Germano,José Ivanaldo,José Leandro,José Lodi Batalha,José Luiz Pereira,José Márcio,Dequinha,José Perácio,José Roberto Padilha,José Roberto de Oliveira,Joselino Martins,Josiel,Josimar Higino,Joubert Araújo,Joubert Meira,Juan Cely,Juan Maldonado,Juan Silveira,Juliano Elizeu,Julinho,Júlio César Moraes,Júlio César Garcia,Júlio César Gurjol,Júlio Kuntz,Peu,Juninho,Juninho Paulista,Júnior,Júnior Baiano,Júnior César,Junqueira,Juvenal Amarijo,Kanu,Kayke Moreno,Kelly,Kenedy,Kita,Kléberson,Ladislau da Guia,Lázaro Vinícius,Lê,Leandro Assumpção,Leandro Amaral,Leandro Ávila,Leandro Damião,Leandro Machado,Leandro Salino,Leandro Silva Neto,Lenon Fernandes,Leo Duarte,Leo Lima,Leo Matos,Léo Morais,Léo Moura,Leo Oliveira,Léo Ortiz,Léo Pereira,Caldeira,Leonardo Gonçalves,Leo Inácio,Leonardo,Leone,Leônidas da Silva,Liedson,Lima Sergipano,Lincoln Corrêa,Lira,Lopes Tigrão,Arcadio López,Lorran,Lucas Paquetá,Lucas Silva,Lúcio Bala,Luciano Baiano,Luciano Sorriso,Lúcio Alves,Val,Luís Antônio Venditti,Luís Carlos Galter,Luís Carlos Vasconcelos,Luís Carlos Winck,Luís Pereira,Luisinho das Arábias,Luisinho Lemos,Luiz Alberto,Luiz Antônio,Luiz Araújo,Luiz Fernando,Luiz Henrique,Luiz Henrique Byron,Luiz José Marques,Luizão,Luvanor Donizete,Claudio Maldonado,César Maluco,Federico Mancuello,Alejandro Mancuso,Manguito,Manoel José Dias,Marcelinho Carioca,Marcelinho Paraíba,Marcelo Augusto,Marcelo Cirino,Marcelo Gonçalves,Marcelinho Leite,Marcelo Macedo,Marcelo Ribeiro,Marcelo Rosa,Marcial,Márcio Araújo,Márcio Costa,Márcio José,Márcio Rafael,Márcio Rossini,Márcio Marabá,Marco Antônio Boiadeiro,Marco Antonio Souza,Marco Aurélio Jacozinho,Dida,Marcos Adriano,Marcos Antônio,Marcos Assunção,Marcos Corrêa,Marcos Cortez,Marcos Paulo,Marcos Rogério,Marquinhos Santos,Pablo Marí,Mário Caetano,Marinho Rodrigues,Mario Braga,Onça,Mário Sérgio,Mário Sérgio Santos,Marllon Borges,Marlon Ventura,Marques,Matheus Cunha,Matheus Dantas,Matheus França,Matheus Gonçalves,Matheus Thuler,Matheuzinho,Mattheus Oliveira,Maurício Azevedo,Mauricio Francisco,Maurinho Fonseca,Mauro de Barros,Maxwell,Médio da Guia,Merica,Michael,Milton Pessanha,Moacir Rodrigues,Moacyr,Moderato Wisintainer,Moisés Moura,Moreira,Fernando Morena,Marcelo Moreno,Marlos Moreno,Mozart Santos,Mozer,Lucas Mugni,Narciso Doval,Narciso dos Santos,Negreiros,Negueba,Nei Severiano,Nélio da Silva,Nelsinho Kerchner,Nelsinho Rosa,Nelson Amorim,Nelson Ricardo,Newton Canegal,Nílson Esídio,Bodinho,Nixon,Nonô,Norival Pereira,Nunes,Paulo Nunes,Obina,Onitlasi Moraes,Raimundo Orsi,Oscar Carregal,Osni Lopes,Osvaldo Nascimento,Otávio,Othon,Otto Bumbel,Paulinho,Paulo Amaral,Paulo César Arruda,Paulo César Carpegiani,Paulo César Lima,Paulo Choco,Paulo Emílio,Paulo Henrique Filho,Paulo Henrique Souza,Paulo Miranda,Paulo Murilo,Pedro Beda,Pedro,Pedro Omar,Pedro Rocha,Pennaforte,Pepê,Horacio Peralta,Darío Pereyra,Dejan Petković,Piá Carioca,Mariusz Piekarski,Pimentel,Píndaro de Carvalho,Pingo,Pintinho,Robert Piris da Motta,Gonzalo Plata,Erick Pulgar,Radar,Rafael Galhardo,Rafael Gaúcho,Rafael Lima,Rafael Pereira,Rafael Vaz,Bobô,César Ramírez,Sérgio Ramirez,Ramon de Morais,Ramón Osni,Ramon Ramos,Recife,Reinaldo da Cruz,Reinaldo Francisco,Reinier,Renato Abreu,Renato Augusto,Renato Gaúcho,Renato Santos,Renato Silva,Renê,Réver,Francisco Reyes,Rhodolfo,Ricardo Rocha,Richard Ríos,Roberto Oliveira,Roberto Emílio,Roberto Miranda,Zanata,Robson Alves,Rodinei,Rodrigo Alvim,Rodrigo Arroz,Rodrigo Baldasso,Rodrigo Caio,Rodrigo de Souza,Rodrigo Fabri,Rodrigo Gral,Rodrigo Longo,Rodrigo Mendes,Rodrigo Muniz,Rodrigo Broa,Rodrigues Neto,Roger Flores,Roger Guerreiro,Rogério Hetmanek,Rogério Lourenço,Roma,Romário,Rômulo Borges,Rômulo Noronha,Ronaldão,Ronaldinho Gaúcho,Ronaldo Angelim,Ronaldo da Silva,Ronaldo Felipe,Ronaldo Marques,Rondinelli,Roniéliton,Rubens Barbosa,Rubens Josué,Rui Rei,Rubens Sambueza,Samir,Samuel Lino,Sandro Becker,Sandro Hiroshi,Santana,Saúl Ñíguez,Sávio,Schneider Cordeiro,Segreto,Sérgio Araújo,Sérgio Cláudio,Sérgio Galocha,Shola Ogundana,Sidney Pullen,Sidney Tobias,Silva Batuta,Sócrates,Jorge Soto,Sylvio Pirillo,Tadeu Ricci,Telefone,Iago Teodoro,Thiago Gosling,Thiago Sales,Thiago Maia,Thiago Neves,Thomás Bedinelli,Tita,Toninho Guerreiro,Toró,Toto,Miguel Trauco,Tuta,Uendel,Uéslei,José Ufarte,Uidemar,Fernando Uribe,Vágner Love,Vagner Marcelino,Val Baiano,Válber Roel,Valdeir Celso,Valdomiro Duarte,Váldson Mendes,Agustín Valido,Vampeta,Vander,Vanderlei Luxemburgo,Vandick,Vandinho,Vantuir,Guillermo Varela,Andrew Ventura,Vicente Arenari,Vicente Rondinelli,Victor Hugo,Victor Simões,Arturo Vidal,Vander Vieira,Matías Viña,Vinícius de Abreu,Vinícius Júnior,Vinícius Pacheco,Vinícius Souza,Viola,Vitinho,Vitor Gabriel,Vitor Hugo Siqueira,Vítor Luís,Carlos Volante,Wagner Alves,Mazinho Oliveira,Waldemar de Brito,Waldomiro Jamal,Wallace Reis,Walter Casagrande,Walter Machado,Walter Minhoca,Wanderley,Washington,Welinton,Wellington Silva,Wendel Silva,Wesley David,Wesley França,Whelliton Silva,William Amendoim,William Kepler,Willian Arão,Willians Domingos,Wilson Costa,Wilson Gomes,Wilson Gottardo,Wilson Rodrigues,Xavier Camargo,Yan,Wallace Yan,Zagallo,Carlos Alberto Zanata,José Marcelo,Zé Mário,Zé Roberto,Zezé,Zezé Moreira,Zico,Zinho,Zizinho,Zózimo"""

def slugify(text):
    """Convert name to URL slug"""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

def get_photo_html(slug, name):
    """Return photo img or SVG placeholder"""
    if slug in PHOTOS:
        return f'<img src="../../img/jogadores/{PHOTOS[slug]}" alt="{name} - jogador do Flamengo" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentElement.innerHTML=\'<svg viewBox=&quot;0 0 200 200&quot; style=&quot;width:100%;height:100%&quot;><rect width=&quot;200&quot; height=&quot;200&quot; fill=&quot;#1a1a1a&quot;/><circle cx=&quot;100&quot; cy=&quot;75&quot; r=&quot;35&quot; fill=&quot;#333&quot;/><ellipse cx=&quot;100&quot; cy=&quot;170&quot; rx=&quot;55&quot; ry=&quot;45&quot; fill=&quot;#333&quot;/></svg>\'">'
    return '<svg viewBox="0 0 200 200" style="width:100%;height:100%"><rect width="200" height="200" fill="#1a1a1a"/><circle cx="100" cy="75" r="35" fill="#333"/><ellipse cx="100" cy="170" rx="55" ry="45" fill="#333"/></svg>'

def generate_bio_html(name, slug):
    """Generate a biography page HTML"""
    data = PLAYER_DATA.get(slug, {})
    full_name = data.get('full', name)
    nick = data.get('nick', name.split()[-1] if ' ' in name else name)
    pos = data.get('pos', 'Jogador')
    born = data.get('born', '—')
    period = data.get('period', '—')
    games = data.get('games', '—')
    goals = data.get('goals', '—')
    titles = data.get('titles', '—')
    bio = data.get('bio', f'{name} é um jogador que fez parte da história do Clube de Regatas do Flamengo, contribuindo para o legado rubro-negro no futebol brasileiro. Vestiu a camisa do maior clube do Brasil e deixou sua marca na história do Mengão.')
    died = data.get('died', '')

    photo_html = get_photo_html(slug, name)

    died_html = f'<div class="info-item"><span class="info-label">Falecimento</span><span class="info-value">{died}</span></div>' if died else ''

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - Jogador do Flamengo | Portal Flamengo</title>
<meta name="description" content="Biografia de {name} no Flamengo. {pos}. Período: {period}. Jogos: {games}. Gols: {goals}. Conheça a história completa.">
<meta name="robots" content="index, follow">
<meta name="author" content="Portal Flamengo">
<meta name="theme-color" content="#c3272b">
<link rel="canonical" href="https://www.portalflamengo.com.br/jogadores/{slug}/">
<link rel="icon" type="image/x-icon" href="../../favicon.ico">
<meta property="og:title" content="{name} - Jogador do Flamengo">
<meta property="og:description" content="Biografia de {name} no Flamengo. {pos}. {games} jogos, {goals} gols.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://www.portalflamengo.com.br/jogadores/{slug}/">
<meta property="og:site_name" content="Portal Flamengo">
<meta property="og:locale" content="pt_BR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1286595053228930" crossorigin="anonymous"></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Person","name":"{full_name}","alternateName":"{nick}","description":"Jogador do Flamengo. {pos}. {games} jogos, {goals} gols.","memberOf":{{"@type":"SportsTeam","name":"Clube de Regatas do Flamengo"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Portal Flamengo","item":"https://www.portalflamengo.com.br/"}},{{"@type":"ListItem","position":2,"name":"Jogadores","item":"https://www.portalflamengo.com.br/jogadores/"}},{{"@type":"ListItem","position":3,"name":"{name}","item":"https://www.portalflamengo.com.br/jogadores/{slug}/"}}]}}
</script>
<style>
:root{{--red:#c3272b;--red-dark:#9e1f22;--black:#0d0d0d;--black-soft:#1a1a1a;--gold:#d4a017;--gold-light:#e8c547;--white:#fff;--off-white:#faf9f7;--cream:#f5f0ea;--gray-100:#f3f3f3;--gray-200:#e5e5e5;--gray-300:#d4d4d4;--gray-500:#737373;--gray-700:#404040;--gray-900:#171717;--font-display:'Playfair Display',Georgia,serif;--font-body:'DM Sans','Inter',system-ui,sans-serif;--font-ui:'Inter',system-ui,sans-serif;--shadow-sm:0 1px 3px rgba(0,0,0,.08);--shadow-md:0 4px 12px rgba(0,0,0,.1);--shadow-lg:0 8px 30px rgba(0,0,0,.12);--radius:8px;--transition:.35s cubic-bezier(.4,0,.2,1)}}
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);color:var(--gray-900);background:var(--off-white);line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none;transition:color var(--transition)}}
img{{max-width:100%;display:block}}
button{{cursor:pointer;border:none;background:none;font-family:var(--font-body)}}
.container{{max-width:1240px;margin:0 auto;padding:0 24px}}
.topbar{{background:var(--black);padding:6px 0;font-size:.75rem;letter-spacing:.5px;text-transform:uppercase;color:rgba(255,255,255,.5);border-bottom:1px solid rgba(255,255,255,.06)}}
.topbar .container{{display:flex;justify-content:space-between;align-items:center}}
.topbar a{{color:rgba(255,255,255,.5)}}.topbar a:hover{{color:var(--gold)}}
.topbar-left{{display:flex;gap:20px}}.topbar-right{{display:flex;gap:16px;align-items:center}}
.topbar-date{{color:rgba(255,255,255,.35)}}
.header-ticker{{background:var(--red-dark);padding:5px 0;overflow:hidden;position:relative;border-bottom:1px solid rgba(0,0,0,.15)}}
.header-ticker-track{{display:flex;animation:htScroll 35s linear infinite}}
.header-ticker-item{{white-space:nowrap;color:rgba(255,255,255,.85);font-size:.75rem;padding:0 30px;font-weight:500;letter-spacing:.3px}}
.header-ticker-item::before{{content:'⚽';margin-right:6px;font-size:.65rem}}
@keyframes htScroll{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.header{{background:var(--red);position:sticky;top:0;z-index:100;border-bottom:3px solid var(--red-dark);box-shadow:0 2px 20px rgba(0,0,0,.15)}}
.header .container{{display:flex;align-items:center;justify-content:space-between;height:60px}}
.logo{{font-family:var(--font-display);font-size:1.7rem;font-weight:800;color:var(--white);display:flex;align-items:center;gap:10px;white-space:nowrap}}
.logo-icon{{width:38px;height:38px;background:var(--black);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0}}
.logo span{{color:var(--gold)}}
.nav{{display:flex;align-items:center;gap:4px}}
.nav a{{color:rgba(255,255,255,.9);font-size:.85rem;font-weight:500;padding:8px 14px;border-radius:6px;transition:all var(--transition);white-space:nowrap}}
.nav a:hover{{background:rgba(255,255,255,.12);color:var(--white)}}
.nav a.active{{background:rgba(0,0,0,.2);color:var(--gold)}}
.header-actions{{display:flex;align-items:center;gap:12px}}
.search-btn{{color:rgba(255,255,255,.8);font-size:1.1rem;padding:8px;border-radius:50%;transition:all var(--transition)}}
.search-btn:hover{{background:rgba(255,255,255,.12);color:var(--white)}}
.hamburger{{display:none;color:var(--white);font-size:1.4rem;padding:8px}}
.breadcrumb{{padding:16px 0;font-size:.82rem;color:var(--gray-500)}}
.breadcrumb a:hover{{color:var(--red)}}
.breadcrumb .sep{{margin:0 8px;color:var(--gray-300)}}
.player-hero{{background:var(--black);padding:60px 0;position:relative;overflow:hidden}}
.player-hero .container{{display:grid;grid-template-columns:280px 1fr;gap:40px;align-items:center}}
.player-photo{{width:280px;height:340px;border-radius:var(--radius);overflow:hidden;background:var(--black-soft);border:3px solid var(--red)}}
.player-info h1{{font-family:var(--font-display);font-size:clamp(2rem,3.5vw,3rem);font-weight:900;color:var(--white);line-height:1.15;margin-bottom:8px}}
.player-nick{{color:var(--gold);font-size:1.1rem;font-weight:600;margin-bottom:16px;font-style:italic}}
.player-pos{{display:inline-block;background:var(--red);color:var(--white);padding:4px 16px;border-radius:50px;font-size:.8rem;font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:20px}}
.player-meta{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.meta-item{{background:rgba(255,255,255,.06);padding:12px 16px;border-radius:6px}}
.meta-label{{font-size:.7rem;text-transform:uppercase;letter-spacing:1px;color:var(--gold);font-weight:600}}
.meta-value{{color:var(--white);font-size:.95rem;font-weight:500;margin-top:2px}}
.stats-bar{{background:var(--red);padding:20px 0}}
.stats-bar .container{{display:flex;justify-content:center;gap:60px}}
.stat-item{{text-align:center}}
.stat-num{{font-family:var(--font-display);font-size:2.2rem;font-weight:900;color:var(--white);line-height:1}}
.stat-lbl{{font-size:.75rem;color:rgba(255,255,255,.7);text-transform:uppercase;letter-spacing:1px;margin-top:4px}}
.bio-content{{padding:60px 0}}
.bio-content .container{{display:grid;grid-template-columns:1fr 320px;gap:48px}}
.bio-main h2{{font-family:var(--font-display);font-size:1.6rem;font-weight:800;color:var(--gray-900);margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid var(--red)}}
.bio-main h2:first-child{{margin-top:0}}
.bio-main p{{margin-bottom:16px;line-height:1.8;color:var(--gray-700)}}
.bio-sidebar{{position:sticky;top:80px;align-self:start}}
.info-card{{background:var(--white);border-radius:var(--radius);padding:24px;box-shadow:var(--shadow-sm);margin-bottom:20px}}
.info-card-title{{font-family:var(--font-display);font-size:1.1rem;font-weight:800;padding-bottom:12px;border-bottom:3px solid var(--red);margin-bottom:16px}}
.info-item{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--gray-100);font-size:.88rem}}
.info-label{{color:var(--gray-500);font-weight:500}}
.info-value{{color:var(--gray-900);font-weight:600;text-align:right}}
.titles-list{{list-style:none}}
.titles-list li{{padding:8px 0;border-bottom:1px solid var(--gray-100);font-size:.88rem;display:flex;align-items:center;gap:8px}}
.titles-list li::before{{content:'🏆';font-size:.75rem}}
.back-link{{display:inline-flex;align-items:center;gap:8px;color:var(--red);font-weight:600;font-size:.9rem;margin-top:20px;padding:10px 20px;background:var(--white);border-radius:50px;box-shadow:var(--shadow-sm);transition:all var(--transition)}}
.back-link:hover{{background:var(--red);color:var(--white)}}
.newsletter{{background:var(--red);padding:60px 0;position:relative;overflow:hidden}}
.newsletter::before{{content:'CRF';position:absolute;right:-40px;top:50%;transform:translateY(-50%);font-family:var(--font-display);font-size:20rem;font-weight:900;color:rgba(255,255,255,.04);pointer-events:none}}
.newsletter .container{{position:relative;z-index:1;text-align:center;max-width:640px}}
.newsletter h2{{font-family:var(--font-display);font-size:2rem;font-weight:800;color:var(--white);margin-bottom:12px}}
.newsletter p{{color:rgba(255,255,255,.7);margin-bottom:28px}}
.newsletter-form{{display:flex;gap:0;max-width:480px;margin:0 auto}}
.newsletter-form input{{flex:1;padding:14px 20px;border:none;border-radius:50px 0 0 50px;font-size:.95rem;font-family:var(--font-body);background:rgba(0,0,0,.25);color:var(--white);outline:none}}
.newsletter-form input::placeholder{{color:rgba(255,255,255,.4)}}
.newsletter-form button{{padding:14px 28px;background:var(--black);color:var(--gold);font-weight:700;font-size:.85rem;text-transform:uppercase;letter-spacing:1px;border-radius:0 50px 50px 0;transition:all var(--transition)}}
.newsletter-form button:hover{{background:var(--gold);color:var(--black)}}
.footer{{background:var(--black);padding:60px 0 0;color:rgba(255,255,255,.4);font-size:.88rem;border-top:3px solid var(--red)}}
.footer-grid{{display:grid;grid-template-columns:1.8fr 1fr 1fr 1fr;gap:40px;padding-bottom:40px}}
.footer-brand h3{{font-family:var(--font-display);font-size:1.5rem;font-weight:800;color:var(--white);margin-bottom:12px}}
.footer-brand h3 span{{color:var(--red)}}
.footer-brand p{{line-height:1.7;margin-bottom:16px}}
.footer-col h4{{color:var(--white);font-size:.82rem;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:20px;font-weight:700}}
.footer-col a{{display:block;color:rgba(255,255,255,.4);padding:6px 0;transition:color var(--transition)}}
.footer-col a:hover{{color:var(--red)}}
.footer-bottom{{border-top:1px solid rgba(255,255,255,.06);padding:20px 0;display:flex;justify-content:space-between;align-items:center;font-size:.78rem;color:rgba(255,255,255,.25)}}
.scroll-top{{position:fixed;bottom:30px;right:30px;width:48px;height:48px;background:var(--red);color:var(--white);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;z-index:50;opacity:0;visibility:hidden;transition:all var(--transition);box-shadow:var(--shadow-md)}}
.scroll-top.visible{{opacity:1;visibility:visible}}
.scroll-top:hover{{background:var(--black);transform:translateY(-3px)}}
.mobile-nav{{position:fixed;top:0;right:-300px;width:300px;height:100%;background:var(--black);z-index:150;padding:80px 30px 30px;transition:right var(--transition);overflow-y:auto}}
.mobile-nav.active{{right:0}}
.mobile-nav a{{display:block;color:rgba(255,255,255,.7);padding:14px 0;font-size:1.05rem;border-bottom:1px solid rgba(255,255,255,.06)}}
.mobile-nav a:hover{{color:var(--red)}}
.mobile-nav-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:140;display:none}}
.mobile-nav-overlay.active{{display:block}}
.mobile-nav-close{{position:absolute;top:20px;right:20px;color:rgba(255,255,255,.5);font-size:1.5rem}}
.search-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:200;display:none;align-items:flex-start;justify-content:center;padding-top:20vh;backdrop-filter:blur(8px)}}
.search-overlay.active{{display:flex}}
.search-box{{width:90%;max-width:640px}}
.search-box input{{width:100%;padding:20px 30px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.12);border-radius:60px;color:var(--white);font-size:1.3rem;font-family:var(--font-body);outline:none;transition:border-color var(--transition)}}
.search-box input:focus{{border-color:var(--red)}}
.search-box input::placeholder{{color:rgba(255,255,255,.3)}}
.search-close{{position:absolute;top:30px;right:30px;color:rgba(255,255,255,.5);font-size:2rem;cursor:pointer}}
.search-close:hover{{color:var(--white)}}
@media(max-width:1024px){{.player-hero .container{{grid-template-columns:220px 1fr;gap:24px}}.bio-content .container{{grid-template-columns:1fr}}.footer-grid{{grid-template-columns:1fr 1fr}}.nav a{{padding:8px 10px;font-size:.8rem}}}}
@media(max-width:768px){{.topbar{{display:none}}.nav{{display:none}}.hamburger{{display:block}}.player-hero .container{{grid-template-columns:1fr;text-align:center}}.player-photo{{margin:0 auto;width:200px;height:240px}}.player-meta{{grid-template-columns:1fr}}.stats-bar .container{{flex-wrap:wrap;gap:24px}}.footer-grid{{grid-template-columns:1fr}}.newsletter-form{{flex-direction:column}}.newsletter-form input{{border-radius:12px 12px 0 0}}.newsletter-form button{{border-radius:0 0 12px 12px;padding:16px}}}}
</style>
</head>
<body>
<div class="topbar"><div class="container"><div class="topbar-left"><a href="../../origem/">Origem</a><a href="../../curiosidades/">Curiosidades</a><a href="../../contato/">Contato</a></div><div class="topbar-right"><span class="topbar-date" id="currentDate"></span></div></div></div>
<header class="header"><div class="container"><a href="../../" class="logo"><div class="logo-icon">🔴</div>Portal <span>Flamengo</span></a><nav class="nav"><a href="../../">Início</a><a href="../" class="active">Jogadores</a><a href="../../tecnicos/">Técnicos</a><a href="../../escalacoes/">Escalações</a><a href="../../presidentes/">Presidentes</a><a href="../../curiosidades/">Curiosidades</a><a href="../../momentos-historicos/">Momentos</a><a href="../../noticias/">Notícias</a></nav><div class="header-actions"><button class="search-btn" onclick="toggleSearch()" aria-label="Buscar">🔍</button><button class="hamburger" onclick="toggleMobileNav()" aria-label="Menu">☰</button></div></div></header>
<div class="header-ticker"><div class="header-ticker-track"><span class="header-ticker-item">Flamengo campeão carioca 2026 — 40º título</span><span class="header-ticker-item">Leonardo Jardim é o novo técnico do Mengão</span><span class="header-ticker-item">Libertadores 2026: Grupo A</span><span class="header-ticker-item">Pedro artilheiro com 8 gols</span><span class="header-ticker-item">Lucas Paquetá de volta ao Flamengo</span><span class="header-ticker-item">Flamengo campeão carioca 2026 — 40º título</span><span class="header-ticker-item">Leonardo Jardim é o novo técnico do Mengão</span><span class="header-ticker-item">Libertadores 2026: Grupo A</span><span class="header-ticker-item">Pedro artilheiro com 8 gols</span><span class="header-ticker-item">Lucas Paquetá de volta ao Flamengo</span></div></div>

<div class="container"><div class="breadcrumb"><a href="../../">Início</a><span class="sep">›</span><a href="../">Jogadores</a><span class="sep">›</span><strong>{name}</strong></div></div>

<section class="player-hero">
<div class="container">
<div class="player-photo">{photo_html}</div>
<div class="player-info">
<span class="player-pos">{pos}</span>
<h1>{name}</h1>
<p class="player-nick">{nick}</p>
<div class="player-meta">
<div class="meta-item"><span class="meta-label">Nome Completo</span><span class="meta-value">{full_name}</span></div>
<div class="meta-item"><span class="meta-label">Nascimento</span><span class="meta-value">{born}</span></div>
<div class="meta-item"><span class="meta-label">Período no Flamengo</span><span class="meta-value">{period}</span></div>
<div class="meta-item"><span class="meta-label">Posição</span><span class="meta-value">{pos}</span></div>
</div>
</div>
</div>
</section>

<div class="stats-bar"><div class="container">
<div class="stat-item"><div class="stat-num">{games}</div><div class="stat-lbl">Jogos</div></div>
<div class="stat-item"><div class="stat-num">{goals}</div><div class="stat-lbl">Gols</div></div>
<div class="stat-item"><div class="stat-num">{period.split("-")[0] if "-" in period else "—"}</div><div class="stat-lbl">Início</div></div>
</div></div>

<section class="bio-content">
<div class="container">
<div class="bio-main">
<h2>Biografia</h2>
<p>{bio}</p>
<p>{name} faz parte do seleto grupo de jogadores que defenderam o Clube de Regatas do Flamengo, o maior e mais popular clube do Brasil. Com mais de 130 anos de história, o Flamengo é reconhecido mundialmente por sua torcida apaixonada de mais de 40 milhões de pessoas e por conquistas memoráveis como a Libertadores e o Mundial de 1981.</p>
<a href="../" class="back-link">← Voltar para Jogadores</a>
</div>
<div class="bio-sidebar">
<div class="info-card">
<h3 class="info-card-title">Ficha Técnica</h3>
<div class="info-item"><span class="info-label">Nome</span><span class="info-value">{full_name}</span></div>
<div class="info-item"><span class="info-label">Nascimento</span><span class="info-value">{born}</span></div>
{died_html}
<div class="info-item"><span class="info-label">Posição</span><span class="info-value">{pos}</span></div>
<div class="info-item"><span class="info-label">Período</span><span class="info-value">{period}</span></div>
<div class="info-item"><span class="info-label">Jogos</span><span class="info-value">{games}</span></div>
<div class="info-item"><span class="info-label">Gols</span><span class="info-value">{goals}</span></div>
</div>
<div class="info-card">
<h3 class="info-card-title">Títulos pelo Flamengo</h3>
<ul class="titles-list">{''.join(f"<li>{t.strip()}</li>" for t in titles.split(",")) if titles != "—" else "<li>—</li>"}
</ul>
</div>
</div>
</div>
</section>

<section class="newsletter"><div class="container"><h2>Fique por Dentro do Mengão</h2><p>Receba as melhores histórias do Flamengo direto no seu e-mail.</p><form class="newsletter-form" onsubmit="return false;"><input type="email" placeholder="Seu melhor e-mail" required><button type="submit">Assinar</button></form></div></section>

<footer class="footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><h3>Portal <span>Flamengo</span></h3><p>O maior portal sobre o Clube de Regatas do Flamengo.</p></div><div class="footer-col"><h4>Explore</h4><a href="../../jogadores/">Jogadores</a><a href="../../tecnicos/">Técnicos</a><a href="../../escalacoes/">Escalações</a><a href="../../presidentes/">Presidentes</a></div><div class="footer-col"><h4>Conteúdo</h4><a href="../../origem/">Origem</a><a href="../../noticias/">Notícias</a><a href="../../momentos-historicos/">Momentos</a><a href="../../artigos/">Artigos</a></div><div class="footer-col"><h4>Portal</h4><a href="../../sobre/">Sobre</a><a href="../../contato/">Contato</a><a href="../../termos-de-uso/">Termos</a><a href="../../politica-privacidade/">Privacidade</a></div></div><div class="footer-bottom"><span>&copy; 2025-2026 Portal Flamengo. Todos os direitos reservados.</span><span>Site não oficial.</span></div></div></footer>

<div class="search-overlay" id="searchOverlay"><span class="search-close" onclick="toggleSearch()">&times;</span><div class="search-box"><input type="text" placeholder="Buscar jogadores, técnicos..." autofocus></div></div>
<div class="mobile-nav-overlay" id="mobileOverlay" onclick="toggleMobileNav()"></div>
<nav class="mobile-nav" id="mobileNav"><span class="mobile-nav-close" onclick="toggleMobileNav()">&times;</span><a href="../../">Início</a><a href="../">Jogadores</a><a href="../../tecnicos/">Técnicos</a><a href="../../escalacoes/">Escalações</a><a href="../../presidentes/">Presidentes</a><a href="../../curiosidades/">Curiosidades</a><a href="../../momentos-historicos/">Momentos</a><a href="../../noticias/">Notícias</a></nav>
<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>

<script>
const d=new Date(),meses=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],dias=['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'];
document.getElementById('currentDate').textContent=dias[d.getDay()]+', '+d.getDate()+' de '+meses[d.getMonth()]+' de '+d.getFullYear();
function toggleSearch(){{document.getElementById('searchOverlay').classList.toggle('active')}}
function toggleMobileNav(){{document.getElementById('mobileNav').classList.toggle('active');document.getElementById('mobileOverlay').classList.toggle('active')}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape'){{document.getElementById('searchOverlay').classList.remove('active');document.getElementById('mobileNav').classList.remove('active');document.getElementById('mobileOverlay').classList.remove('active')}}}});
window.addEventListener('scroll',()=>{{const b=document.getElementById('scrollTop');if(window.scrollY>600)b.classList.add('visible');else b.classList.remove('visible')}});
</script>
</body>
</html>'''

# ============================================================
# GERAR TODAS AS BIOGRAFIAS
# ============================================================
players = [p.strip() for p in ALL_PLAYERS.split(',') if p.strip()]
print(f"Total de jogadores: {len(players)}")

generated = 0
skipped = 0

for name in players:
    slug = slugify(name)

    # Mapeamentos especiais de slug
    slug_map = {
        'adriano-imperador': 'adriano',
        'dejan-petkovic': 'petkovic',
        'vinicius-junior': 'vinicius-junior',
        'ronaldinho-gaucho': 'ronaldinho-gaucho',
        'giorgian-de-arrascaeta': 'arrascaeta',
        'leonidas-da-silva': 'leonidas',
        'jose-leandro': 'leandro',
        'domingos-da-guia': 'domingos-da-guia',
        'jair-rosa-pinto': 'jair-rosa-pinto',
        'vagner-love': 'vagner-love',
        'diego-ribas': 'diego-ribas',
        'david-luiz': 'david-luiz',
        'everton-ribeiro': 'everton-ribeiro',
        'bruno-henrique': 'bruno-henrique',
        'filipe-luis': 'filipe-luis',
        'lucas-paqueta': 'lucas-paqueta',
        'paolo-guerrero': 'paolo-guerrero',
        'willian-arao': 'willian-arao',
        'emerson-sheik': 'emerson-sheik',
        'felipe-melo': 'felipe-melo',
        'arturo-vidal': 'arturo-vidal',
        'andreas-pereira': 'andreas-pereira',
        'ayrton-lucas': 'ayrton-lucas',
        'ronaldo-angelim': 'ronaldo-angelim',
        'rodrigo-caio': 'rodrigo-caio',
        'diego-alves': 'diego-alves',
        'thiago-maia': 'thiago-maia',
        'matheus-franca': 'matheus-franca',
        'leo-moura': 'leo-moura',
        'fausto-dos-santos': 'fausto',
        'pablo-mari': 'pablo-mari',
    }

    slug = slug_map.get(slug, slug)

    if slug in SKIP:
        skipped += 1
        continue

    # Create directory
    dir_path = os.path.join(JOGADORES_DIR, slug)
    os.makedirs(dir_path, exist_ok=True)

    # Generate HTML
    html = generate_bio_html(name, slug)

    filepath = os.path.join(dir_path, 'index.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    generated += 1

print(f"Geradas: {generated} biografias")
print(f"Puladas (já existiam): {skipped}")
print(f"Total: {generated + skipped}")

# ============================================================
# DEPLOY VIA FTP
# ============================================================
print("\n=== DEPLOY VIA FTP ===")
ftp = ftplib.FTP("69.6.220.159")
ftp.login("portalflamengoco", "claude2026#")

count = 0
for name in players:
    slug = slugify(name)
    slug_map = {
        'adriano-imperador': 'adriano', 'dejan-petkovic': 'petkovic',
        'vinicius-junior': 'vinicius-junior', 'ronaldinho-gaucho': 'ronaldinho-gaucho',
        'giorgian-de-arrascaeta': 'arrascaeta', 'leonidas-da-silva': 'leonidas',
        'jose-leandro': 'leandro', 'domingos-da-guia': 'domingos-da-guia',
        'jair-rosa-pinto': 'jair-rosa-pinto', 'vagner-love': 'vagner-love',
        'diego-ribas': 'diego-ribas', 'david-luiz': 'david-luiz',
        'everton-ribeiro': 'everton-ribeiro', 'bruno-henrique': 'bruno-henrique',
        'filipe-luis': 'filipe-luis', 'lucas-paqueta': 'lucas-paqueta',
        'paolo-guerrero': 'paolo-guerrero', 'willian-arao': 'willian-arao',
        'emerson-sheik': 'emerson-sheik', 'felipe-melo': 'felipe-melo',
        'arturo-vidal': 'arturo-vidal', 'andreas-pereira': 'andreas-pereira',
        'ayrton-lucas': 'ayrton-lucas', 'ronaldo-angelim': 'ronaldo-angelim',
        'rodrigo-caio': 'rodrigo-caio', 'diego-alves': 'diego-alves',
        'thiago-maia': 'thiago-maia', 'matheus-franca': 'matheus-franca',
        'leo-moura': 'leo-moura', 'fausto-dos-santos': 'fausto',
    }
    slug = slug_map.get(slug, slug)

    if slug in SKIP:
        continue

    local_file = os.path.join(JOGADORES_DIR, slug, 'index.html')
    if not os.path.exists(local_file):
        continue

    remote_dir = f"/public_html/jogadores/{slug}"
    try:
        ftp.cwd(remote_dir)
    except:
        try:
            ftp.cwd("/public_html/jogadores")
            ftp.mkd(slug)
            ftp.cwd(remote_dir)
        except:
            continue

    with open(local_file, 'rb') as f:
        ftp.storbinary("STOR index.html", f)
    count += 1
    if count % 50 == 0:
        print(f"  Deploy: {count} páginas...")

ftp.quit()
print(f"\nDeploy completo! {count} biografias no ar.")
print(f"Total no portal: {count + len(SKIP)} biografias de jogadores")
