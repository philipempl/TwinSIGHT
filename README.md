# TwinSIGHT

[![Branch master](https://github.com/philipempl/TwinSIGHT/actions/workflows/master.yml/badge.svg)](https://github.com/philipempl/TwinSIGHT/actions/workflows/master.yml)
[![Branch experimental](https://github.com/philipempl/TwinSIGHT/actions/workflows/experimental.yml/badge.svg)](https://github.com/philipempl/TwinSIGHT/actions/workflows/experimental.yml)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/philipempl/TwinSIGHT.svg)](http://isitmaintained.com/project/philipempl/TwinSIGHT "Percentage of issues still open")
[![GitHub forks](https://img.shields.io/github/forks/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/network)
[![GitHub stars](https://img.shields.io/github/stars/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT/stargazers)
[![GitHub license](https://img.shields.io/github/license/philipempl/TwinSIGHT)](https://github.com/philipempl/TwinSIGHT)

## Introduction
The internet of things produces a massive flood of data due to the vast amount of underlying heterogeneous devices. The heterogeneity is a result of the multitude of vendors and diverse upcoming standards and protocols. From a cybersecurity perspective, this heterogeneity presents an enormous challenge. Analyses must cover all temporal dimensions to recognize incidents in real-time. These incidents are based on so-called indicators of compromise, and by identifying and reacting to them, potential damage can be minimized or completely ward off.  Thus, from the underlying data, information must be created, which can lead to knowledge and wisdom. By processing stream and batch data, descriptive, diagnostic, detective, predictive and prescriptive analytics can be engaged.   

## Pipeline
The pipeline shows a visualization of the Docker Compose file. The Viz repository [pmsipilot/docker-compose-viz](https://github.com/pmsipilot/docker-compose-viz) was used for this with the following command:
```docker
docker run --rm -it --name dc -v ${pwd}:/input pmsipilot/docker-compose-viz render -m image docker-compose.yml -f --horizontal --no-volumes
```
![alt text](https://github.com/philipempl/TwinSIGHT/blob/master/resources/docker-compose.png)

## Tech stack
| Technology      | Version | Description | Task     |
| -       |    :-:   |      -  |       ---- |
| [Apache Kafka](https://kafka.apache.org/)      | latest  | Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.       |  Message broker cluster to structure the amount of heterogeneous data by topics and distribute it to various consumers, including Logstash.   |
| [Apache Zookeeper](https://zookeeper.apache.org/) |   latest    | ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them, which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.  |   Apache Zookeeper takes care of the administration of the distributed systems in the pipeline. In particular, this acts as a coordinator for Apache Kafka.    |
| [Docker](https://www.docker.com/) |       latest  |   Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels.    |Serves the underlying infrastructure to link the individual technologies in a modular way to make their use platform-independent and straightforward. This makes the deployment of the "Analytics Pipeline" a breeze.
| [Elasticsearch](https://www.elastic.co/elasticsearch/)    | 7.10.1    | Elasticsearch is a distributed, RESTful search and analytics engine capable of addressing a growing number of use cases. As the heart of the Elastic Stack, it centrally stores your data for lightning fast search, fine‑tuned relevancy, and powerful analytics that scale with ease.  |    Elasticsearch represents the data store to index all the data based on a particular topic. Moreover, the use of Elasticsearch in IoT is appropriate to make the data search more efficient.   |
| [EMQ X](https://www.emqx.io/) |        latest  |   Scalable and Reliable Real-time MQTT Message Broker for IoT in the 5G Era. EMQ X connects any IoT device via all major IoT communication protocols, including MQTT v5.0, CoAP/LwM2M 1.1 and even LoraWAN, over 3G/4G/5G&NB-IoT networks, and ensures security via TLS/DTLS, X.509 certificate, and diverse authentication mechanism.    |EMQ X is the messaging broker and the gateway into the analytics pipeline. EMQ X acts as a broker and connects all IoT devices and edge nodes using the MQTT protocol and specific topics.|
| [Kafka UI](https://github.com/provectus/kafka-ui) |        latest  |   Kafka UI is a free open-source web UI for monitoring and management of Apache Kafka clusters. Kafka UI is a simple tool that makes your data flows observable, helps find and troubleshoot issues faster and deliver optimal performance. Its lightweight dashboard makes it easy to track key metrics of your Kafka clusters - Brokers, Topics, Partitions, Production, and Consumption. | Kafka UI simplifies the administration of a Kafka cluster by visualizing the Topics, Consumers, Producers and Brokers.
| [Kibana](https://www.elastic.co/kibana) |        7.10.1  |  Kibana is a free and open user interface that lets you visualize your Elasticsearch data and navigate the Elastic Stack. Do anything from tracking query load to understanding the way requests flow through your apps.     |Kibana is used for pure visualization of incoming data streams and batch data. Besides, users could also use machine learning algorithms to gain essential insights from the data. |
| [Logstash](https://www.elastic.co/logstash) |        7.10.1 |   Logstash is a free and open server-side data processing pipeline that ingests data from a multitude of sources, transforms it, and then sends it to your favorite stash.    | Logstash collects the messages from the individual Kafka topics and, using various filters, can preprocess the data before it is stored in Elasticsearch. |
| [MQTT-Kafka-Bridge](https://github.com/maechler/mqtt2kafkabridge) TO BE REPLACED |       latest  |  This is an extremely primitive MQTT to Kafka bridge, consisting of around 100 lines of code. It is not optimized for extensibility, performance nor stability and should not be used in a production environment. All it does is reading messages from an MQTT broker, replacing topic separators (e.g. home/outside/humidity -> home.outside.humidity) and forwarding the message to Kafka.     | This bridge is used to efficiently transfer the topics of the MQTT broker to the topics of the Kafka broker and synchronize their contents. |
| [Redis](https://redis.io/) TO BE INTEGRATED | latest | Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache, and message broker. Redis provides data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes, and streams. Redis has built-in replication, Lua scripting, LRU eviction, transactions, and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster. | Redis is used for the authenatication of IoT devices inside the EMQ X message broker. |

## Deploy

### Build the infrastructure
The simple variant of deployment without changing the configuration files:
```docker
docker-compose up
```
If the Logstash pipeline files or the installation commands of individual plugins for Logstash have changed, it is recommended to initiate a rebuild of the infrastructure:
```docker
docker-compose up --build --force-recreate
```
### Run the MQTT message producer
#### Dependencies
TODO
#### Command
```python
py /python-mqtt-client/client.py
```

### Call the UIs
```html
http://localhost:5601 (Kibana)
http://localhost:9000 (Kafka UI)
http://localhost:18083 (EMQ X)
```

Happy analyzing!
## Authors
* **Philip Empl** - [Department of Information Systems](https://www.uni-regensburg.de/wirtschaftswissenschaften/wi-pernul/team/philip-empl/index.html)  *@ University of Regensburg*

## License
This project is available under the MIT license.
