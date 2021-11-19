# https://www.docker.elastic.co/
FROM docker.elastic.co/logstash/logstash:7.10.2

# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-integration-kafka
RUN logstash-plugin install logstash-output-elasticsearch
RUN logstash-plugin install logstash-output-stdout
RUN logstash-plugin install logstash-filter-json