---
title: Policies service
keywords: architecture, service, policies
tags: [architecture]
permalink: architecture-services-policies.html
---

The "policies" service takes care of persisting [Policies](basic-policy.html).

## Model

The model of the policies service is defined around the entity `Policy`:


* [Policy model](https://github.com/eclipse/ditto/tree/master/policies/model/src/main/java/org/eclipse/ditto/policies/model)

## Signals

Other services can communicate with the policies service via:


* [commands](https://github.com/eclipse/ditto/tree/master/policies/model/src/main/java/org/eclipse/ditto/policies/model/signals/commands):
  containing commands and command responses which are processed by this service
* [events](https://github.com/eclipse/ditto/tree/master/policies/model/src/main/java/org/eclipse/ditto/policies/model/signals/events):
  containing events which are emitted when entities managed by this service were modified

## Persistence

The policies service uses [Akka persistence](https://doc.akka.io/docs/akka/current/persistence.html?language=java) and 
with that [Event sourcing](basic-signals.html#architectural-style) in order to persist changes to  
and restore persisted [policies](basic-policy.html).

