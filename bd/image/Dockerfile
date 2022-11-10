# readme: https://github.com/docker-library/docs/blob/master/postgres/README.md

FROM postgres:12-alpine


# Define as variáveis de ambiente
ENV POSTGRES_PASSWORD          mudar123
#ENV POSTGRES_USER              tempox
ENV POSTGRES_HOST_AUTH_METHOD  md5


# Definir Locale
RUN apk add --no-cache --update musl musl-utils musl-locales tzdata

ENV TZ    America/Sao_Paulo
ENV LANG  pt_BR.UTF-8

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo 'export LC_ALL=$LANG' >> /etc/profile.d/locale.sh && \
    sed -i 's|LANG=C.UTF-8|LANG=$LANG|' /etc/profile.d/locale.sh

#COPY ./initialization /docker-entrypoint-initdb.d