#!/bin/bash
# Commita os containers atuais preservando tudo que foi configurado
# Roda no HOST (fora dos containers)

echo "=== Commitando containers ==="

docker commit 7fb15deafc57 monitoring-lab/mon01:v1
echo "mon01 commitado"

docker commit 29ba54585ca9 monitoring-lab/web01:v1
echo "web01 commitado"

docker commit 7e0bb3e5dee4 monitoring-lab/db01:v1
echo "db01 commitado"

docker commit ac2d117afabf monitoring-lab/bkp01:v1
echo "bkp01 commitado"

echo ""
echo "=== Imagens criadas ==="
docker images | grep monitoring-lab

echo ""
echo "Pronto! Agora pode fazer deploy da stack no Portainer."
echo "Copie a pasta monitoring-lab pro servidor e use o docker-compose.yml"
