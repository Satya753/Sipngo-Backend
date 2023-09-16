
FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=Password
ENV MYSQL_DATABASE=sipngo

COPY create_new_user.sql SipngoBackup.sql /docker-entrypoint-initdb.d/ 

EXPOSE 3307
