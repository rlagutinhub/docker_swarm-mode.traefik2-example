# Traefik 2 example configure for Docker Swarm Mode
```
```
In this tutorial you'll learn how to deploy Traefik 2 with HTTP/HTTPS/TCP support including examples on a docker swarm mode.

FYI https://docs.traefik.io/

***

## Install Traefik

### Generating a self-signed certificates:

```bash
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
```
```bash
openssl genrsa -out default.key 2048
openssl req -new -x509 -sha256 -key default.key -out default.crt -days 3650 -subj "/CN=*.dev.mta4.ru/C=RU/ST=Moscow/L=Moscow/O=MTA4RU/OU=IT" -config req.cnf -extensions x509_ext
openssl x509 -inform pem -in default.crt -noout -text
docker config create traefik_default.key.$(date +%F) default.key
docker config create traefik_default.crt.$(date +%F) default.crt
# docker secret create traefik_default.key.$(date +%F) default.key
# docker secret create traefik_default.crt.$(date +%F) default.crt
```
```bash
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
```
```bash
openssl genrsa -out hello.dev.mta4.ru.key 2048
openssl req -new -x509 -sha256 -key hello.dev.mta4.ru.key -out hello.dev.mta4.ru.crt -days 3650 -subj "/CN=hello.dev.mta4.ru/C=RU/ST=Moscow/L=Moscow/O=MTA4RU/OU=IT" -config req.cnf -extensions x509_ext
openssl x509 -inform pem -in hello.dev.mta4.ru.crt -noout -text
docker config create traefik_hello.dev.mta4.ru.key.$(date +%F) hello.dev.mta4.ru.key
docker config create traefik_hello.dev.mta4.ru.crt.$(date +%F) hello.dev.mta4.ru.crt
# docker secret create traefik_hello.dev.mta4.ru.key.$(date +%F) hello.dev.mta4.ru.key
# docker secret create traefik_hello.dev.mta4.ru.crt.$(date +%F) hello.dev.mta4.ru.crt
```

### Create traefik static and dynamic configs:

```bash
# docker config rm traefik.toml.$(date +%F)
# docker config rm traefik.dynamic.toml.$(date +%F)
# docker config create traefik.toml.$(date +%F) traefik.toml
# docker config create traefik.dynamic.toml.$(date +%F) traefik.dynamic.toml

docker config rm traefik.yml.$(date +%F)
docker config rm traefik.dynamic.yml.$(date +%F)
docker config create traefik.yml.$(date +%F) traefik.yml
docker config create traefik.dynamic.yml.$(date +%F) traefik.dynamic.yml
```

### Pull latest traefik image:

```bash
docker pull traefik:latest
```

### Create overlay network for traefik:

```bash
docker network create -d overlay proxy
```

### Add node label for run traefik:

```bash
docker node update --label-add "proxy=true" docker01
docker node inspect --format='{{json .Spec.Labels}}' docker01
```

### Add node label for restricting run traefik:

```bash
docker stack deploy --compose-file docker-compose.traefik.yml traefik
# docker stack rm traefik
```

***

## Examples

### HTTP/HTTPS proxying:

```bash
# build docker image hello
docker build -t hello -f Dockerfile .
```
```bash
docker stack deploy --compose-file docker-compose.app.v1.yml hello # http
docker stack deploy --compose-file docker-compose.app.v2.yml hello # https
docker stack deploy --compose-file docker-compose.app.v3.yml hello # http+https
docker stack deploy --compose-file docker-compose.app.v4.yml hello # http+redirect+https
docker stack deploy --compose-file docker-compose.app.v5.yml hello # http+redirect+https+auth
docker stack deploy --compose-file docker-compose.app.v6.yml hello # http+sticky
docker stack deploy --compose-file docker-compose.app.v7.yml hello # http+https+sticky
docker stack deploy --compose-file docker-compose.app.v8.yml hello # http+redirect+https+auth+sticky
```

### TCP proxying:

```bash
docker stack deploy --compose-file docker-compose.app.v9.yml mysql # tcp 3306to30000
docker stack deploy --compose-file docker-compose.app.v10.yml vnc # tcp 5901to30001
```

***

![alt text](https://raw.githubusercontent.com/rlagutinhub/docker_swarm-mode.traefik2-example/master/screen1.png)
![alt text](https://raw.githubusercontent.com/rlagutinhub/docker_swarm-mode.traefik2-example/master/screen2.png)
![alt text](https://raw.githubusercontent.com/rlagutinhub/docker_swarm-mode.traefik2-example/master/screen3.png)
![alt text](https://raw.githubusercontent.com/rlagutinhub/docker_swarm-mode.traefik2-example/master/screen4.png)

