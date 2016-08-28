FROM fusionapp/base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -qy fop css2xslfo
COPY wheelhouse /wheelhouse
COPY requirements.txt /application/requirements.txt
RUN /appenv/bin/pip install --no-index -f /wheelhouse -r /application/requirements.txt Documint
COPY bin/css2xslfo /usr/bin/
COPY bin/clj-neon /usr/bin/
ADD https://s3-eu-west-1.amazonaws.com/files.fusionapp.com/clj-neon-0.1.0-SNAPSHOT-standalone.jar /usr/share/clj-neon/clj-neon.jar
COPY docker/fop.xconf /root/.config/documint/fop.xconf
COPY fonts /appenv/fonts/
RUN /appenv/bin/trial --temp-directory=/tmp/_trial_temp --reporter=text documint \
  && rm -rf /tmp/_trial_temp

EXPOSE 8750
WORKDIR "/appenv"
ENTRYPOINT ["/appenv/bin/twistd", "-n", "--pidfile=", "documint"]
