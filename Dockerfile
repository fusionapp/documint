FROM fusionapp/base

ADD https://s3-eu-west-1.amazonaws.com/files.fusionapp.com/clj-neon-0.1.0-SNAPSHOT-standalone.jar /usr/share/clj-neon/clj-neon.jar
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -qy fop css2xslfo
COPY bin/css2xslfo /usr/bin/
COPY bin/clj-neon /usr/bin/
COPY docker/fop.xconf /root/.config/documint/fop.xconf
COPY fonts /appenv/fonts/
COPY requirements.txt /application/requirements.txt
RUN /appenv/bin/pip install --no-cache-dir --requirement /application/requirements.txt
COPY . /application
RUN /appenv/bin/pip install --no-cache-dir /application
RUN /appenv/bin/trial --temp-directory=/tmp/_trial_temp --reporter=text documint \
  && rm -rf /tmp/_trial_temp

EXPOSE 8750
WORKDIR "/appenv"
ENTRYPOINT ["/appenv/bin/twistd", "-n", "--pidfile=", "documint"]
CMD ["--keystore", "/srv/documint/keystore.jks", \
     "--password", "123456", \
     "--privateKeyPassword", "123456"]
