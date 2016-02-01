FROM fusionapp/base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -qy fop css2xslfo
COPY wheelhouse /wheelhouse
COPY requirements.txt /application/requirements.txt
RUN /appenv/bin/pip install --no-index -f /wheelhouse -r /application/requirements.txt Documint
COPY bin/css2xslfo /usr/bin/
COPY bin/clj-neon /usr/bin/
COPY bin/clj-neon.jar /usr/share/clj-neon/
COPY docker/fop.xconf /root/.config/documint/fop.xconf
COPY fonts /appenv/fonts/
RUN /appenv/bin/trial --temp-directory=/tmp/_trial_temp --reporter=text documint \
  && rm -rf /tmp/_trial_temp

EXPOSE 8750
WORKDIR "/appenv"
ENTRYPOINT ["/appenv/bin/twistd", "-n", "--pidfile=", "documint"]
