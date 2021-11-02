FROM registry.gitlab.com/assassyn__v/aci_project/pulsar:latest

COPY conf/ /conf
COPY scripts/ /scripts

ENV JAVA_OPTS "-Xms256m -Xmx512m -XX:CompressedClassSpaceSize=256m"
ENV _JAVA_OPTIONS "-Xms256m -Xmx512m -XX:CompressedClassSpaceSize=256m"

RUN chmod u+x /scripts/*.sh
RUN chmod u+x /conf/*.sh
