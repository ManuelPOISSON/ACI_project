FROM registry.gitlab.com/assassyn__v/aci_project/pulsar:latest

COPY conf/ /conf
COPY scripts/ /scripts

RUN chmod u+x /scripts/*.sh
RUN chmod u+x /conf/*.sh
