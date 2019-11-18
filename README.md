https://docs.traefik.io/migration/v1-to-v2/
https://docs.traefik.io/providers/docker/
https://github.com/containous/traefik
https://docs.traefik.io/reference/dynamic-configuration/docker/
https://docs.traefik.io/v2.0/middlewares/overview/#provider-namespace
https://github.com/containous/traefik/blob/master/traefik.sample.toml
https://github.com/containous/traefik/issues/5032
https://github.com/containous/traefik/issues/5114
https://github.com/containous/traefik/issues/5507

https://github.com/jakubhajek/traefik-swarm
https://creekorful.me/how-to-install-traefik-2-docker-swarm/
https://dev.to/nflamel/how-to-have-https-on-development-with-docker-traefik-v2-and-mkcert-2jh3
https://chriswiegman.com/2019/10/serving-your-docker-apps-with-https-and-traefik-2/
https://www.grzegorowski.com/secure-docker-grafana-container-with-ssl-through-traefik-proxy
https://medium.com/@containeroo/traefik-2-0-wildcard-lets-encrypt-certificates-1658370adc68

# --

cat <<EOF > req.cnf
[req]
distinguished_name = subject
req_extensions = x509_ext
[subject]
CN = *.dev.mta4.ru
[x509_ext]
subjectKeyIdentifier = hash
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = *.dev.mta4.ru
DNS.2 = *.ws.dev.mta4.ru
EOF

openssl genrsa -out default.key 2048
openssl req -new -x509 -sha256 -key default.key -out default.crt -days 3650 -subj "/CN=*.dev.mta4.ru/C=RU/ST=Moscow/L=Moscow/O=MTA4RU/OU=IT" -config req.cnf -extensions x509_ext
openssl x509 -inform pem -in default.crt -noout -text
docker config create traefik_default.key.$(date +%F) default.key
docker config create traefik_default.crt.$(date +%F) default.crt
# docker secret create traefik_default.key.$(date +%F) default.key
# docker secret create traefik_default.crt.$(date +%F) default.crt

cat <<EOF > req.cnf
[req]
distinguished_name = subject
req_extensions = x509_ext
[subject]
CN = hello.dev.mta4.ru
[x509_ext]
subjectKeyIdentifier = hash
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = hello.dev.mta4.ru
DNS.2 = hello.ws.dev.mta4.ru
EOF

openssl genrsa -out hello.dev.mta4.ru.key 2048
openssl req -new -x509 -sha256 -key hello.dev.mta4.ru.key -out hello.dev.mta4.ru.crt -days 3650 -subj "/CN=hello.dev.mta4.ru/C=RU/ST=Moscow/L=Moscow/O=MTA4RU/OU=IT" -config req.cnf -extensions x509_ext
openssl x509 -inform pem -in hello.dev.mta4.ru.crt -noout -text
docker config create traefik_hello.dev.mta4.ru.key.$(date +%F) hello.dev.mta4.ru.key
docker config create traefik_hello.dev.mta4.ru.crt.$(date +%F) hello.dev.mta4.ru.crt
# docker secret create traefik_hello.dev.mta4.ru.key.$(date +%F) hello.dev.mta4.ru.key
# docker secret create traefik_hello.dev.mta4.ru.crt.$(date +%F) hello.dev.mta4.ru.crt

# --

# docker config rm traefik.toml.$(date +%F)
# docker config rm traefik.dynamic.toml.$(date +%F)
# docker config create traefik.toml.$(date +%F) traefik.toml
# docker config create traefik.dynamic.toml.$(date +%F) traefik.dynamic.toml

docker config rm traefik.yml.$(date +%F)
docker config rm traefik.dynamic.yml.$(date +%F)
docker config create traefik.yml.$(date +%F) traefik.yml
docker config create traefik.dynamic.yml.$(date +%F) traefik.dynamic.yml

docker pull traefik:latest

docker network create -d overlay proxy

docker node update --label-add "proxy=true" docker-srv1.mta4.ru
docker node inspect --format='{{json .Spec.Labels}}' docker-srv1.mta4.ru

docker stack deploy --compose-file docker-compose.yml traefik
docker stack rm traefik

docker build -t hello -f Dockerfile .
docker stack deploy --compose-file docker-compose.app.yml hello
docker stack rm hello

# --

hello.dev.mta4.ru
traefik.dev.mta4.ru:8080

