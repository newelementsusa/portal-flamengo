#!/bin/bash
cd ~/Claudinho/projetos/portal-flamengo

FTP_HOST="69.6.220.159"
FTP_USER="newnewelements"
FTP_PASS='3b=[ffLU^VNs'
REMOTE_DIR="/public_html/portal-flamengo"

upload() {
  curl -s -T "$1" "ftp://$FTP_HOST$REMOTE_DIR/$2" --user "$FTP_USER:$FTP_PASS" --ftp-create-dirs && echo "OK: $1" || echo "FAIL: $1"
}

upload "index.html" ""
upload "origem/index.html" "origem/"
upload "jogadores/index.html" "jogadores/"
upload "curiosidades/index.html" "curiosidades/"
upload "tecnicos/index.html" "tecnicos/"
upload "presidentes/index.html" "presidentes/"
upload "escalacoes/index.html" "escalacoes/"

echo "Deploy completo!"
