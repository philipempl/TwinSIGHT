# TwinSIGHT

[![Percentage of issues still open](http://isitmaintained.com/badge/open/philipempl/TwinSIGHT.svg)](http://isitmaintained.com/project/philipempl/TwinSIGHT "Percentage of issues still open")
[![GitHub forks](https://img.shields.io/github/forks/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/network)
[![GitHub stars](https://img.shields.io/github/stars/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/stargazers)
[![GitHub license](https://img.shields.io/github/license/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/blob/master/LICENSE.md)

## Introduction

 Although there are numerous advantages of the IoT in industrial use, there are also some security problems, such as insecure supply chains or vulnerabilities. These lead to a threatening security posture in organizations. Security analytics is a collection of capabilities and technologies systematically processing and analyzing data to detect or predict threats and imminent incidents. As digital twins improve knowledge generation and sharing, they are an ideal foundation for security analytics in the IoT. Digital twins map physical assets to their respective virtual counterparts along the lifecycle. They leverage the connection between the physical and virtual environments and manage semantics, i.e., ontologies, functional relationships, and behavioral models. This paper presents the DT2SA model that aligns security analytics with digital twins to generate shareable cybersecurity knowledge. The model relies on a formal model resulting from previously defined requirements. We validated the DT2SA model with a microservice architecture called Twinsight, which is publicly available, open-source, and based on a real industry project. The results highlight challenges and strategies for leveraging cybersecurity knowledge in IoT using digital twins.

## Tech stack

| Technology                                             | Version |                                                                                                          Task                                                                                                         |
| ------------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Docker](https://www.docker.com/)                      | latest  | Serves the underlying infrastructure to link the individual technologies in a modular way to make their use platform-independent and straightforward. This makes the deployment of the "Analytics Pipeline" a breeze. |
| [HiveMQ](https://www.hivemq.com/)                          | latest  |               HiveMQ's MQTT broker makes it easy to move data to and from connected devices in an efficient, fast and reliable manner.              |
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

### Eclipse Ditto Connections & Policies  
First you need to run the DevOps-Commands for Eclipse Ditto, namely Kafka and MQTT. You can find these commands under [Eclipse Ditto DevOps](https://www.eclipse.org/ditto/connectivity-manage-connections.html).

To enable curl in Windows, you need to run following command (optional: Windows only):
```console
Remove-item alias:curl
```
Then push the main policy to Eclipse Ditto:
```console
 curl -X PUT 'http://localhost:8080/api/2/policies/twin.sight:policy' -u 'ditto:ditto' -H 'Content-Type: application/json' -d '@./volumes/ditto/policies/policy-main.json'
 ```
 Afterwards you need to create the drill and mill machine LENZDRGB610 in Eclipse Ditto:
 ```console
  curl -X PUT 'http://localhost:8080/api/2/things/twin.sight:LENZDRGB610' -u 'ditto:ditto' -H 'Content-Type: application/json' -d '@./volumes/ditto/policies/thing-LENZDRGB610.json'
  ```
You also need to connect to the HiveMQ broker:
```console
 curl -X POST 'http://localhost:8080/devops/piggyback/connectivity?timeout=60' -u 'devops:foobar' -H 'Content-Type: application/json' -d '@./volumes/ditto/policies/connector-mqtt.json'
 ```
 Last you need to connect to Apache Kafka:
 ```console
  curl -X POST 'http://localhost:8080/devops/piggyback/connectivity?timeout=60' -u 'devops:foobar' -H 'Content-Type: application/json' -d '@./volumes/ditto/policies/connector-kafka.json'
  ```
### Run the Drill & Mill Machine Client

#### Dependencies

```python
pip install -r requirements.txt
```

#### Command

```python
py ./machine_client/client.py
```

### Call the UIs

```html
http://localhost:5601 (Kibana/Wazuh)
http://localhost:9000 (Kafka UI)
http://localhost:8080 (Eclipse Ditto [username=ditto, password=ditto])
```

Happy analyzing!
![alt text](https://raw.githubusercontent.com/philipempl/TwinSIGHT/main/resources/screenshot.png)
The template can be found in /volumes/kibana/dashboards.

## Research and Citation
Please consider citing our publication if you are using our **TwinSIGHT** prototype for your research: https://www.doi.org/10.3390/info14020095 

```bib
@Article{Empl2023,
author = {Empl, Philip and Pernul, G{\"u}nther},
title = {Digital-Twin-Based Security Analytics for the Internet of Things},
journal = {Information},
volume = {14},
year = {2023},
number = {2},
article-number = {95},
url = {https://www.mdpi.com/2078-2489/14/2/95},
issn = {2078-2489},
doi = {10.3390/info14020095}
}
```

## Authors
-   **Philip Empl** - [Department of Information Systems](https://www.uni-regensburg.de/wirtschaftswissenschaften/wi-pernul/team/philip-empl/index.html)  *@ University of Regensburg*

## License

This project is available under the MIT license.
