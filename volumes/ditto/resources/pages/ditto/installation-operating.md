---
title: Operating Ditto
tags: [installation]
keywords: operating, docker, docker-compose, devops, logging, logstash, elk, monitoring, prometheus, grafana
permalink: installation-operating.html
---

[pubsubmediator]: https://doc.akka.io/docs/akka/current/distributed-pub-sub.html

Once you have successfully started Ditto, proceed with setting it up for continuous operation.

This page shows the basics for operating Ditto.

## Configuration

Ditto has many config parameters which can be set in the config files or via environment variables.
This section will cover some of Ditto's config parameters.

### MongoDB configuration
If you choose not to use the MongoDB container and instead use a dedicated MongoDB you can use
the following environment variables in order to configure the connection to the MongoDB.

* MONGO_DB_URI: Connection string to MongoDB
* MONGO_DB_SSL_ENABLED: Enabled SSL connection to MongoDB
* MONGO_DB_CONNECTION_MIN_POOL_SIZE: Configure MongoDB minimum connection pool size
* MONGO_DB_CONNECTION_POOL_SIZE: Configure MongoDB connection pool size
* MONGO_DB_READ_PREFERENCE: Configure MongoDB read preference
* MONGO_DB_WRITE_CONCERN: Configure MongoDB write concern
* AKKA_PERSISTENCE_MONGO_JOURNAL_WRITE_CONCERN: Configure Akka Persistence MongoDB journal write concern
* AKKA_PERSISTENCE_MONGO_SNAPS_WRITE_CONCERN: Configure Akka Persistence MongoDB snapshot write concern

### Ditto configuration

Each of Ditto's microservice has many options for configuration, e.g. timeouts, cache sizes, etc.

In order to have a look at all possible configuration options and what default values they have, here are the 
configuration files of Ditto's microservices:
* Policies: [policies.conf](https://github.com/eclipse/ditto/blob/master/policies/service/src/main/resources/policies.conf)
* Things: [things.conf](https://github.com/eclipse/ditto/blob/master/things/service/src/main/resources/things.conf)
* Things-Search: [things-search.conf](https://github.com/eclipse/ditto/blob/master/thingsearch/service/src/main/resources/things-search.conf)
* Concierge: [concierge.conf](https://github.com/eclipse/ditto/blob/master/concierge/service/src/main/resources/concierge.conf)
* Connectivity: [connectivity.conf](https://github.com/eclipse/ditto/blob/master/connectivity/service/src/main/resources/connectivity.conf)
* Gateway: [gateway.conf](https://github.com/eclipse/ditto/blob/master/gateway/service/src/main/resources/gateway.conf)

Whenever you find the syntax `${?UPPER_CASE_ENV_NAME}` in the configuration files, you may overwrite the default value
by specifying that environment variable when running the container.

When no environment variable is defined in the config, you may change the default value anyway by specifying a
"System property" you pass to the Java process.

The following example configures the devops password of the gateway-service started via docker-compose. In order
to supply additional configuration one has to add the variable in the corresponding `command` section of the
`docker-compose.yml` file.

```yml
...
# Alternative approach for configuration of the service
command: java -Dditto.gateway.authentication.devops.password=foobar -jar starter.jar
```

The executable for the microservice is called `starter.jar`. The configuration variables have to be set before
the `-jar` option.

### Pre-authentication

HTTP API calls to Ditto may be authenticated with a reverse proxy (e.g. a nginx) which:
* authenticates a user/subject
* passes the authenticated username as HTTP header
* ensures that this HTTP header can never be written by the end-user

By default, `pre-authentication` is **disabled** in the Ditto [gateway](architecture-services-gateway.html) services.
It can however be enabled by configuring the environment variable `ENABLE_PRE_AUTHENTICATION` to the value `true`.

When it is enabled, the reverse proxy has to set the HTTP header `x-ditto-pre-authenticated`.<br/>
The format of the "pre-authenticated" string is: `<issuer>:<subject>`. The issuer defines which system authenticated 
the user and the subject contains e.g. the user-id or -name.

This string must then be used in [policies](basic-policy.html#subjects) as "Subject ID".

Example for a nginx "proxy" configuration:
```
auth_basic                    "Authentication required";
auth_basic_user_file          nginx.htpasswd;
...
proxy_set_header              x-ditto-pre-authenticated "nginx:${remote_user}";
```


### OpenID Connect

The authentication provider must be added to the ditto-gateway configuration.
`auth-subjects`, an optional field, takes a list of placeholders that will be
evaluated against incoming JWT's.
For each entry in `auth-subjects` and authorization subject will be generated.
If the entry contains unresolvable placeholders, it will be ignored in full.
When `auth-subjects` is not provided, the “sub” claim (`{%raw%}{{ jwt:sub }}{%endraw%}`) is used by default.


```
ditto.gateway.authentication {
    oauth {
      openid-connect-issuers = {
        myprovider = {
          issuer = "localhost:9000"
          auth-subjects = [
            "{%raw%}{{ jwt:sub }}{%endraw%}",
            "{%raw%}{{ jwt:sub }}/{{ jwt:scp }}{%endraw%}",
            "{%raw%}{{ jwt:sub }}/{{ jwt:scp }}@{{ jwt:client_id }}{%endraw%}",
            "{%raw%}{{ jwt:sub }}/{{ jwt:scp }}@{{ jwt:non_existing }}{%endraw%}",
            "{%raw%}{{ jwt:roles/support }}{%endraw%}"
          ]
        }
      }
    }
}
```

In order to do this by specifying a Java system property, use the following:

```shell
-Dditto.gateway.authentication.oauth.openid-connect-issuers.myprovider.issuer=localhost:9000
-Dditto.gateway.authentication.oauth.openid-connect-issuers.myprovider.auth-subjects.0='{%raw%}{{ jwt:sub }}/{{ jwt:scp }}{%endraw%}'

```

The configured subject-issuer will be used to prefix the value of each individual `auth-subject`.

```json
{
  "subjects": {
    "<provider>:<auth-subject-0>": {
      "type": "generated"
    }
    ...
    "<provider>:<auth-subject-n>": {
      "type": "generated"
    }
  }
}
```

As of the OAuth2.0 and OpenID Connect standards Ditto expects the headers `Authorization: Bearer <JWT>` and
`Content-Type: application/json`, containing the issued token of the provider.

**The token has to be issued beforehand. The required logic is not provided by Ditto.** When using
the OIDC provider [keycloak](https://www.keycloak.org/), a project like [keycloak-gatekeeper](https://github.com/keycloak/keycloak-gatekeeper)
may be put in front of Ditto to handle the token-logic.

**If the chosen OIDC provider uses a self-signed certificate**, the certificate has to be retrieved and configured for 
the akka-http ssl configuration.

```
ssl-config {
  trustManager = {
    stores = [
      { type = "PEM", path = "/path/to/cert/globalsign.crt" }
    ]
  }
}
```

## Logging

Gathering logs for a running Ditto installation can be achieved by:

* sending logs to STDOUT/STDERR: this is the default
   * can be disabled by setting the environment variable `DITTO_LOGGING_DISABLE_SYSOUT_LOG`
   * Benefits: simple, works with all Docker logging drivers (e.g. "awslogs", "splunk", etc.)

* pushing logs into ELK stack: this can be done by setting the environment variable `DITTO_LOGGING_LOGSTASH_SERVER`
   * configure `DITTO_LOGGING_LOGSTASH_SERVER` to contain the endpoint of a logstash server
    
* writing logs to log files: this can be done by setting the environment variable `DITTO_LOGGING_FILE_APPENDER` to `true`
   * configure the amount of log files, and the total amount of space used for logs files via these two environment 
     variables:
       * `DITTO_LOGGING_FILE_NAME_PATTERN` (default: /var/log/ditto/<service-name>.log.%d{yyyy-MM-dd}.gz)
       * `DITTO_LOGGING_MAX_LOG_FILE_HISTORY_IN_DAYS` (default: 10) 
       * `DITTO_LOGGING_TOTAL_LOG_FILE_SIZE` (default: 1GB)
   * the format in which logging is done is "LogstashEncoder" format - that way the logfiles may easily be imported into
     an ELK stack
   * when running Ditto in Kubernetes apply the `ditto-log-files.yaml` to your Kubernetes cluster in order to 
     mount log files to the host system.

## Monitoring

In addition to logging, the Ditto images include monitoring features. Specific metrics are
automatically gathered and published on an HTTP port. There it can be scraped by a [Prometheus](https://prometheus.io)
backend, from where the metrics can be accessed to display in dashboards (e.g. with [Grafana](https://grafana.com)).

### Monitoring configuration

In the default configuration, each Ditto service opens a HTTP endpoint, where it provides the Prometheus metrics 
on port `9095`. This can be changed via the environment variable `PROMETHEUS_PORT`.

Ditto will automatically publish gathered metrics at the endpoint `http://<container-host-or-ip>:9095/`.

Further, Prometheus can be configured to poll on all Ditto service endpoints in order to persist the historical metrics.
Grafana can add a Prometheus server as its data source and can display
the metrics based on the keys mentioned in section ["Gathered metrics"](#gathered-metrics).

### Gathered metrics

In order to inspect which metrics are exported to Prometheus, just visit the Prometheus HTTP endpoint of a Ditto service:
`http://<container-host-or-ip>:9095/`.

The following example shows an excerpt of metrics gathered for the
[gateway-service](architecture-services-gateway.html).

```
#Kamon Metrics
# TYPE jvm_threads gauge
jvm_threads{component="system-metrics",measure="total"} 72.0
# TYPE jvm_memory_buffer_pool_count gauge
jvm_memory_buffer_pool_count{component="system-metrics",pool="direct"} 14.0
# TYPE jvm_class_loading gauge
jvm_class_loading{component="system-metrics",mode="loaded"} 10491.0
# TYPE jvm_memory_buffer_pool_usage gauge
jvm_memory_buffer_pool_usage{component="system-metrics",pool="direct",measure="used"} 396336.0
# TYPE roundtrip_http_seconds histogram
roundtrip_http_seconds_bucket{le="0.05",ditto_request_path="/api/2/things/x",ditto_request_method="PUT",ditto_statusCode="201",segment="overall"} 1.0
roundtrip_http_seconds_sum{ditto_request_path="/api/2/things/x",ditto_statusCode="201",ditto_request_method="PUT",segment="overall"} 0.038273024
roundtrip_http_seconds_bucket{le="0.001",ditto_request_path="/api/2/things/x",ditto_request_method="PUT",ditto_statusCode="204",segment="overall"} 0.0
roundtrip_http_seconds_bucket{le="0.1",ditto_request_path="/api/2/things/x",ditto_request_method="PUT",ditto_statusCode="204",segment="overall"} 7.0
roundtrip_http_seconds_sum{ditto_request_path="/api/2/things/x",ditto_statusCode="204",ditto_request_method="PUT",segment="overall"} 0.828899328
# TYPE jvm_gc_promotion histogram
jvm_gc_promotion_sum{space="old"} 7315456.0
# TYPE jvm_gc_seconds histogram
jvm_gc_seconds_count{component="system-metrics",collector="scavenge"} 9.0
jvm_gc_seconds_sum{component="system-metrics",collector="scavenge"} 0.063
# TYPE jvm_memory_bytes histogram
jvm_memory_bytes_count{component="system-metrics",measure="used",segment="miscellaneous-non-heap-storage"} 54.0
jvm_memory_bytes_sum{component="system-metrics",measure="used",segment="miscellaneous-non-heap-storage"} 786350080.0
```

To put it in a nutshell, Ditto reports:

* JVM metrics for all services
    * amount of garbage collections + GC times
    * memory consumption (heap + non-heap)
    * amount of threads + loaded classes
* HTTP metrics for [gateway-service](architecture-services-gateway.html)
    * roundtrip times from request to response
    * amount of HTTP calls
    * status code of HTTP responses
* MongoDB metrics for [things-service](architecture-services-things.html),
[policies-service](architecture-services-policies.html), [things-search-service](architecture-services-things-search.html)
    * inserts, updates, reads per second
    * roundtrip times
* cache metrics for [concierge-service](architecture-services-concierge.html)
* connection metrics for [connectivity-service](architecture-services-connectivity.html)
    * processed messages
    * mapping times

Have a look at the 
[example Grafana dashboards](https://github.com/eclipse/ditto/tree/master/deployment/operations/grafana-dashboards)
and build and share new ones back to the Ditto community.

## Tracing

Ditto supports reading and propagating [W3C trace context](https://www.w3.org/TR/trace-context/) headers at the 
edges of the Ditto service (e.g. Gateway and Connectivity service). Several spans are generated when a request is  
processed and the tracing data is exported in [OpenTelemetry](https://opentelemetry.io/) format using 
kamon-opentelemetry library.

Adjust the following environment variables to configure the Ditto services to produce traces:
* `DITTO_TRACING_ENABLED`: determines whether tracing is enabled (default:`false`) 
* `DITTO_TRACING_SAMPLER`: defines the used sampler
  * `always`: report all traces 
  * `never`:  don't report any trace (default)
  * `random`: randomly decide using the probability defined in the `DITTO_TRACING_RANDOM_SAMPLER_PROBABILITY` environment variable
  * `adaptive`: keeps dynamic samplers for each operation while trying to achieve a set throughput goal (`DITTO_TRACING_ADAPTIVE_SAMPLER_THROUGHPUT`) 
* `OTEL_EXPORTER_OTLP_ENDPOINT`: the OTLP endpoint where to report the gathered traces (default: `http://localhost:4317`)

## DevOps commands

The "DevOps commands" API allows Ditto operators to make changes to a running installation without restarts.

The following DevOps commands are supported:

* Dynamically retrieve and change log levels
* Dynamically retrieve service configuration
* Piggyback commands

{% include note.html content="The default credentials for the `/devops` HTTP endpoint are username: `devops`, password: `foobar`. The password can be changed by setting the environment variable `DEVOPS_PASSWORD` in the gateway service." %}


### Dynamically adjust log levels

Changing the log levels dynamically is very useful when debugging an accidental problem,
since the cause of the problem could be lost on service restart.

#### Retrieve all log levels

Example for retrieving all currently configured log levels:<br/>
`GET /devops/logging`

Response:

```json
{
    "gateway": {
        "1": {
            "type": "devops.responses:retrieveLoggerConfig",
            "status": 200,
            "serviceName": "gateway",
            "instance": 1,
            "loggerConfigs": [{
                "level": "info",
                "logger": "ROOT"
            }, {
                "level": "info",
                "logger": "org.eclipse.ditto"
            }, {
                "level": "warn",
                "logger": "org.mongodb.driver"
            }]
        }
    },
    "things-search": {
        ...
    },
    "policies": {
        ...
    },
    "things": {
        ...
    },
    "connectivity": {
        ...
    }
}
```

#### Change a specific log level for all services

Example request payload to change the log level of logger `org.eclipse.ditto` in all services to `DEBUG`:<br/>
`PUT /devops/logging`

```json
{
    "logger": "org.eclipse.ditto",
    "level": "debug"
}
```

#### Retrieve log levels of a service

Example response for retrieving all currently configured log levels of gateways services:<br/>
`GET /devops/logging/gateway`

Response:

```json
{
    "1": {
        "type": "devops.responses:retrieveLoggerConfig",
        "status": 200,
        "serviceName": "gateway",
        "instance": 1,
        "loggerConfigs": [{
            "level": "info",
            "logger": "ROOT"
        }, {
            "level": "info",
            "logger": "org.eclipse.ditto"
        }, {
            "level": "warn",
            "logger": "org.mongodb.driver"
        }]
    }
}
```

#### Change a specific log level for one service

Example request payload to change the log level of logger `org.eclipse.ditto` in all
instances of gateway-service to `DEBUG`:

`PUT /devops/logging/gateway`

```json
{
    "logger": "org.eclipse.ditto",
    "level": "debug"
}
```

### Dynamically retrieve configurations

Runtime configurations of services are available for the Ditto operator at
`/devops/config/` with optional restrictions by service name, instance ID and configuration path.
The entire runtime configuration of a service may be dozens of kilobytes big. If it exceeds the cluster message size
of 250 kB, then it can only be read piece by piece via the `path` query parameter.

#### Retrieve all service configurations

Retrieve the configuration at the path `ditto.info` thus:

`GET /devops/config?path=ditto.info`

It is recommended to not omit the query parameter `path`. Otherwise, the full configurations of all services are
aggregated in the response, which can become megabytes big.

The path `ditto.info` points to information on service name, service instance index, JVM arguments and environment
variables. Response example:

```json
{
  "gateway": {
    "1": {
      "type": "common.responses:retrieveConfig",
      "status": 200,
      "config": {
        "env": {
          "PATH": "/usr/games:/usr/local/games"
        },
        "service": {
          "instance-index": "1",
          "service-name": "gateway"
        },
        "vm-args": [
          "-Dfile.encoding=UTF-8"
        ]
      }
    }
  },
  "connectivity": {
    "1": {
      "type": "common.responses:retrieveConfig",
      "status": 200,
      "config": {
        "env": {
          "CONNECTIVITY_FLUSH_PENDING_RESPONSES_TIMEOUT": "3d"
        },
        "service": {
          "instance-index": "1",
          "service-name": "connectivity"
        },
        "vm-args": [
          "-Dditto.connectivity.connection.snapshot.threshold=2"
        ]
      }
    }
  }
}
```

#### Retrieve the configuration of a service instance

Retrieving the configuration of a specific service instance is much faster
because the response is not aggregated from an unknown number of respondents
over the duration given in the query parameter `timeout`.

To retrieve `ditto` configuration from Gateway instance `1`:

`GET /devops/config/gateway/1?path=ditto`

Response example:

```json
{
  "gateway": {
    "1": {
      "type": "common.responses:retrieveConfig",
      "status": 200,
      "config": {
        "cluster": {
          "number-of-shards": 20
        },
        "gateway": {
          "authentication": {
            "devops": {
              "password": "foobar",
              "secured": false
            }
          }
        }
      }
    }
  }
}
```

### Piggyback commands

You can use a DevOps command to send a command to another actor in the cluster.
Those special commands are called piggyback commands.
A piggyback command must conform to the following schema:

{% include docson.html schema="jsonschema/piggyback-command.json" %}

Example:

```json
{
    "targetActorSelection": "/system/sharding/connection",
    "headers": {
        "aggregate": false
    },
    "piggybackCommand": {
        "type": "connectivity.commands:createConnection",
        ...
    }
}
```

#### Managing connections

Piggybacks are used to configure Dittos connectivity service. More information on this can be found in
the [Manage Connections](connectivity-manage-connections.html) section.

#### Managing background cleanup

Ditto deletes unnecessary events and snapshots in the background according to database load. Each Things, Policies and
Connectivity instance has an actor coordinating a portion of the background cleanup process. The actor responds to
piggyback-commands to query its state and configuration, modify its configuration, and restart the background cleanup
process.

Each command is sent to the actor selection `/user/<SERVICE_NAME>Root/persistenceCleanup`, where
`SERVICE_NAME` is `things`, `policies` or `connectivity`:

`POST /devops/piggygack/<SERVICE_NAME>?timeout=10s`

##### Query background cleanup coordinator state

`POST /devops/piggygack/<SERVICE_NAME>?timeout=10s`

```json
{
  "targetActorSelection": "/user/<SERVICE_NAME>Root/persistenceCleanup",
  "headers": {},
  "piggybackCommand": {
    "type": "status.commands:retrieveHealth"
  }
}
```

The response has the following details:

- `state`: The current state of the actor.
- `pid`: The last persistence ID being cleaned up. It has the form `<entity-type>:<entity-id>`.

```json
{
  "things": {
    "1": {
      "type": "status.responses:retrieveHealth",
      "status": 200,
      "statusInfo": {
        "status": "UP",
        "details": [
          {
            "INFO": {
              "state": "RUNNING",
              "pid": "thing:org.eclipse.ditto:fancy-thing_53"
            }
          }
        ]
      }
    }
  }
}
```

##### Query background cleanup coordinator configuration

`POST /devops/piggygack/<SERVICE_NAME>?timeout=10s`

```json
{
  "targetActorSelection": "/user/<SERVICE_NAME>Root/persistenceCleanup",
  "headers": {},
  "piggybackCommand": {
    "type": "common.commands:retrieveConfig"
  }
}
```

Response example:

```json
{
  "things": {
    "1": {
      "type": "common.responses:retrieveConfig",
      "status": 200,
      "config": {
        "enabled": true,
        "interval": "3s",
        "quiet-period": "5m",
        "timer-threshold": "150ms",
        "credits-per-batch": 3,
        "reads-per-query": 100,
        "writes-per-credit": 100,
        "delete-final-deleted-snapshot": false
      }
    }
  }
}
```

##### Modify background cleanup coordinator configuration

Send a piggyback command of type `common.commands:modifyConfig` to change the configuration of the persistence cleanup
process. All subsequent cleanup processes will use the new configuration. The ongoing cleanup process is aborted.
Configurations absent in the payload of the piggyback command remain unchanged.
Set the special key `last-pid` to set the lower bound of PIDs to clean up in the next run.

`POST /devops/piggygack/<SERVICE_NAME>?timeout=10s`

```json
{
  "targetActorSelection": "/user/<SERVICE_NAME>Root/persistenceCleanup",
  "headers": {
    "aggregate": false,
    "is-grouped-topic": true
  },
  "piggybackCommand": {
    "type": "common.commands:modifyConfig",
    "config": {
      "quiet-period": "240d",
      "last-pid": "thing:namespace:PID-lower-bound"
    }
  }
}
```

The response contains the effective configuration of the background cleanup coordinator. If the configuration in the
piggyback command contains any error, then an error is logged and the actor's configuration is unchanged.
The field `last-pid` is not a part of the configuration.

```json
{
  "things": {
    "1": {
      "type": "common.responses:modifyConfig",
      "status": 200,
      "config": {
        "enabled": true,
        "interval": "3s",
        "quiet-period": "240d",
        "timer-threshold": "150ms",
        "credits-per-batch": 3,
        "reads-per-query": 100,
        "writes-per-credit": 100,
        "delete-final-deleted-snapshot": false
      }
    }
  }
}
```

##### Shutdown background cleanup coordinator

Send a piggyback command of type `common.commands:shutdown` to stop the background cleanup process. The next process is
scheduled after the `quiet-period` duration in the coordinator's configuration.

`POST /devops/piggygack/concierge/<INSTANCE_INDEX>?timeout=10s`

```json
{
  "targetActorSelection": "/user/conciergeRoot/eventSnapshotCleanupCoordinatorProxy",
  "headers": {
    "aggregate": false,
    "is-grouped-topic": true
  },
  "piggybackCommand": {
    "type": "common.commands:shutdown"
  }
}
```

Response example:

```json
{
  "concierge": {
    "1": {
      "type": "common.responses:shutdown",
      "status": 200,
      "message": "Restarting stream in <PT5760H30M5S>."
    }
  }
}
```

##### Cleanup events and snapshots of an entity

Send a cleanup command by piggyback to the entity's service and shard region to trigger removal of stale events and
snapshots manually. Here is an example for things. Change the service name and shard region name accordingly for
policies and connections. Typically in a docker based environment, use `INSTANCE_INDEX=1`.


`POST /devops/piggygack/things/<INSTANCE_INDEX>?timeout=10s`

```json
{
  "targetActorSelection": "/system/sharding/thing",
  "headers": {
    "aggregate": false
  },
  "piggybackCommand": {
    "type": "cleanup.commands:cleanupPersistence",
    "entityId": "ditto:thing1"
  }
}
```

Response example:

```json
{
  "things": {
    "1": {
      "type": "cleanup.responses:cleanupPersistence",
      "status": 200,
      "entityId": "thing:ditto:thing1"
    }
  }
}
```

#### Managing background synchronization

A background sync actor goes over thing snapshots and search index entries slowly to ensure eventual consistency
of the search index. The actor operates in the same manner as the background cleanup coordinator and responds to
the same commands.

`POST /devops/piggygack/things-search/<INSTANCE_INDEX>?timeout=10s`

```json
{
  "targetActorSelection": "/user/thingsSearchRoot/searchUpdaterRoot/backgroundSyncProxy",
  "headers": {
    "aggregate": false,
    "is-grouped-topic": true
  },
  "piggybackCommand": {
    "type": "<COMMAND-TYPE>"
  }
}
```

`COMMAND-TYPE` can be:
- `common.commands:shutdown` to shutdown or restart a background sync stream,
- `common.commands:retrieveConfig` to retrieve the current configuration,
- `common.commands:modifyConfig` to modify the current configuration, or
- `status.commands:retrieveHealth` to query the current progress and event log.

For each command type, please refer to the corresponding segment of "Managing background cleanup" for the exact format.

#### Force search index update for one thing

The search index should rarely become out-of-sync for a long time, and it can repair itself
of any inconsistencies detected at query time. Nevertheless, you can trigger search index update
for a particular thing by a DevOp-command and bring the entry up-to-date immediately.

`POST /devops/piggygack/things-search/<INSTANCE_INDEX>?timeout=0`

```json
{
  "targetActorSelection": "/user/thingsSearchRoot/searchUpdaterRoot/thingsUpdater",
  "headers": {
    "aggregate": false,
    "is-grouped-topic": true
  },
  "piggybackCommand": {
    "type": "thing-search.commands:updateThing",
    "thingId": "<THING-ID>"
  }
}
```

There is no response. Things-search service will log a warning upon receiving this message
and continue to log warnings should the search index update fail on the persistence.

#### Erasing data within a namespace

Ditto supports erasure of _all_ data within a namespace during live operations.
To do so safely, perform the following steps in sequence.

1. [Block all messages to the namespace](#block-all-messages-to-a-namespace)
   so that actors will not spawn in the namespace.
2. [Shutdown all actors in the namespace](#shutdown-all-actors-in-a-namespace)
   so that no actor will generate data in the namespace.
3. [Erase data from the persistence](#erase-all-data-in-a-namespace-from-the-persistence).
4. [Unblock messages to the namespace](#unblock-messages-to-a-namespace)
   so that the old namespace could be reused at a later point in time.

##### Block all messages to a namespace

Send a piggyback command to [Akka's pub-sub-mediator][pubsubmediator] with type `namespaces.commands:blockNamespace`
to block all messages sent to actors belonging to a namespace.

`PUT /devops/piggygack?timeout=10s`

```json
{
  "targetActorSelection": "/system/distributedPubSubMediator",
  "headers": {
    "aggregate": false
  },
  "piggybackCommand": {
    "type": "namespaces.commands:blockNamespace",
    "namespace": "namespaceToBlock"
  }
}
```

Once a namespace is blocked on all members of the Ditto cluster, you will get a response
similar to the one below. The namespace will remain blocked for the lifetime of the Ditto cluster,
or until you proceed with [step 4](#unblock-messages-to-a-namespace), which unblocks it.

```json
{
  "?": {
    "?": {
      "type": "namespaces.responses:blockNamespace",
      "status": 200,
      "namespace": "namespaceToBlock",
      "resourceType": "namespaces"
    }
  }
}
```

##### Shutdown all actors in a namespace

Send a piggyback command to [Akka's pub-sub-mediator][pubsubmediator] with type `common.commands:shutdown`
to request all actors in a namespace to shut down. The value of `piggybackCommand/reason/type` must be
`purge-namespace`; otherwise, the namespace's actors will not stop themselves.

`PUT /devops/piggygack?timeout=0`

```json
{
  "targetActorSelection": "/system/distributedPubSubMediator",
  "piggybackCommand": {
    "type": "common.commands:shutdown",
    "reason": {
      "type": "purge-namespace",
      "details": "namespaceToShutdown"
    }
  }
}
```

The shutdown command has no response because the number of actors shutting down can be very large.
The response will always be `408` timeout.
Feel free to send the shutdown command several times to make sure.

##### Erase all data in a namespace from the persistence

Send a piggyback command to [Akka's pub-sub-mediator][pubsubmediator] with type `namespaces.commands:purgeNamespace`
to erase all data from the persistence.
It is better to purge a namespace after
[blocking](#block-all-messages-to-a-namespace) it and
[shutting down](#shutdown-all-actors-in-a-namespace)
all its actors so that no data is written in the namespace while erasing is ongoing.

The erasure may take a long time if the namespace has a lot of data associated with it or if the persistent storage is
slow. Set the timeout to a safe margin above the estimated erasure time in milliseconds.

`PUT /devops/piggygack?timeout=10s`

```json
{
  "targetActorSelection": "/system/distributedPubSubMediator",
  "headers": {
    "aggregate": true,
    "is-group-topic": true
  },
  "piggybackCommand": {
    "type": "namespaces.commands:purgeNamespace",
    "namespace": "namespaceToPurge"
  }
}
```

The response contains results of the data purge, one for each resource type.
Note that to see responses from multiple resource types, the header `aggregate` must not be `false`.

```json
{
  "?": {
    "?": {
      "type": "namespaces.responses:purgeNamespace",
      "status": 200,
      "namespace": "namespaceToPurge",
      "resourceType": "thing",
      "successful": true
    },
    "?1": {
      "type": "namespaces.responses:purgeNamespace",
      "status": 200,
      "namespace": "namespaceToPurge",
      "resourceType": "policy",
      "successful": true
    },
    "?2": {
      "type": "namespaces.responses:purgeNamespace",
      "status": 200,
      "namespace": "namespaceToPurge",
      "resourceType": "thing-search",
      "successful": true
    }
  }
}
```

##### Unblock messages to a namespace

Send a piggyback command to [Akka's pub-sub-mediator][pubsubmediator] with type `namespaces.commands:unblockNamespace`
to stop blocking messages to a namespace.

`PUT /devops/piggygack?timeout=10s`

```json
{
  "targetActorSelection": "/system/distributedPubSubMediator",
  "headers": {
    "aggregate": false
  },
  "piggybackCommand": {
    "type": "namespaces.commands:unblockNamespace",
    "namespace": "namespaceToUnblock"
  }
}
```

A response will come once the namespace's blockade is released on all members of the Ditto cluster.

```json
{
  "?": {
    "?": {
      "type": "namespaces.responses:unblockNamespace",
      "status": 200,
      "namespace": "namespaceToUnblock",
      "resourceType": "namespaces"
    }
  }
}
```
