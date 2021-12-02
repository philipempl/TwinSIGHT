# TwinSIGHT

[![Percentage of issues still open](http://isitmaintained.com/badge/open/philipempl/TwinSIGHT.svg)](http://isitmaintained.com/project/philipempl/TwinSIGHT "Percentage of issues still open")
[![GitHub forks](https://img.shields.io/github/forks/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/network)
[![GitHub stars](https://img.shields.io/github/stars/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/stargazers)
[![GitHub license](https://img.shields.io/github/license/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/blob/master/LICENSE.md)

## Introduction

Digital Twins map physical artifacts to virtual representations with a pre-defined fidelity and sharpen the bidirectional communication of the physical and virtual world in the Industrial IoT. Digital Twins also manage semantics, i.e., ontologies and relations between functional components and data. The Digital Twin is an ideal foundation to perform security analytics in the Industrial IoT. Security analytics is Big Data analytics from a cybersecurity perspective and aims at protecting devices by analyzing and correlating data from various data sources. Analytical results can be shared among lifecycles participants through Digital Twins to communicate the overall security state of a physical artifact. This repository presents a framework that integrates security analytics into a Digital Twin, enables the contextualization of data, and thus, converts data to knowledge about incidents. Thereby, this repository aims at providing insights through detective-analytical operations. 

## Tech stack

| Technology                                             | Version |                                                                                                          Task                                                                                                         |
| ------------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Docker](https://www.docker.com/)                      | latest  | Serves the underlying infrastructure to link the individual technologies in a modular way to make their use platform-independent and straightforward. This makes the deployment of the "Analytics Pipeline" a breeze. |
| [EMQ X](https://www.emqx.io/)                          | latest  |               EMQ X is the messaging broker and the gateway into the analytics pipeline. EMQ X acts as a broker and connects all IoT devices and edge nodes using the MQTT protocol and specific topics.              |
| [Eclipse Ditto](https://www.eclipse.org/ditto)         | 2.2.0   |                                  Abstract the device into a digital twin providing synchronous and asynchronous APIs and use the digital twin API to work with your physical device.                                  |
| [Apache Zookeeper](https://zookeeper.apache.org/)      | latest  |                               Apache Zookeeper takes care of the administration of the distributed systems in the pipeline. In particular, this acts as a coordinator for Apache Kafka.                               |
| [Apache Kafka](https://kafka.apache.org/)              | latest  |                                       Message broker cluster to structure the amount of heterogeneous data by topics and distribute it to various consumers, including Logstash.                                      |
| [Kafka UI](https://github.com/provectus/kafka-ui)      | latest  |                                                 Kafka UI simplifies the administration of a Kafka cluster by visualizing the Topics, Consumers, Producers and Brokers.                                                |
| [Logstash](https://www.elastic.co/logstash)            | 7.10.1  |                               Logstash collects the messages from the individual Kafka topics and, using various filters, can preprocess the data before it is stored in Elasticsearch.                               |
| [Elasticsearch](https://www.elastic.co/elasticsearch/) | 7.10.1  |              Elasticsearch represents the data store to index all the data based on a particular topic. Moreover, the use of Elasticsearch in IoT is appropriate to make the data search more efficient.              |
| [Kibana](https://www.elastic.co/kibana)                | 7.10.1  |                   Kibana is used for pure visualization of incoming data streams and batch data. Besides, users could also use machine learning algorithms to gain essential insights from the data.                  |
| [Wazuh](https://wazuh.com/)                            | 4.1.2   |                                   Wazuh is used to collect, aggregate, index and analyze security data and helps this framework detect intrusions, threats and behavioral anomalies.                                  |

## Pipeline

The pipeline shows a visualization of the Docker Compose file. The Viz repository [pmsipilot/docker-compose-viz](https://github.com/pmsipilot/docker-compose-viz) was used for this with the following command:

```docker
docker run --rm -it --name dc -v ${pwd}:/input pmsipilot/docker-compose-viz render -m image docker-compose.yml -f --horizontal --no-volumes
```

![alt text](https://github.com/philipempl/TwinSIGHT/blob/master/resources/docker-compose.png)

## Deployment

### Build the infrastructure

The simple variant of deployment without changing the configuration files:

```docker
docker-compose up
```

If the Logstash pipeline files or the installation commands of individual plugins for Logstash have changed, it is recommended to initiate a rebuild of the infrastructure:

```docker
docker-compose up --build --force-recreate
```

### Connections

First you need to run the DevOps-Commands for Eclipse Ditto, namely Kafka and MQTT. You can find these commands under [Eclipse Ditto DevOps](https://www.eclipse.org/ditto/connectivity-manage-connections.html).

### Run the drill & mill machine client

#### Dependencies

```python
pip install -r requirements.txt
```

#### Command

```python
py /machine_client/client.py
```

### Call the UIs

```html
http://localhost:5601 (Kibana/Wazuh)
http://localhost:9000 (Kafka UI)
http://localhost:18083 (EMQ X)
http://localhost:8080 (Eclipse Ditto)
```

Happy analyzing!

## Authors

-   **Philip Empl** - [Department of Information Systems](https://www.uni-regensburg.de/wirtschaftswissenschaften/wi-pernul/team/philip-empl/index.html)  *@ University of Regensburg*

## License

This project is available under the MIT license.
