# NimbusFlow — Product Overview

NimbusFlow is a fictional workflow-automation product used throughout this
RAG learning exercise. It is not a real product — all content in this
document set is synthetic, created for practicing chunking and retrieval.

## What NimbusFlow Does

NimbusFlow lets teams design multi-step automation pipelines that connect
internal tools, approve requests, and route notifications. A pipeline is
made up of **triggers**, **actions**, and **conditions**.

![NimbusFlow architecture diagram](https://example.com/images/nimbusflow-architecture.png)

The diagram above shows the three core services: the Trigger Service, the
Execution Engine, and the Notification Router. Requests enter through the
Trigger Service, get evaluated by the Execution Engine against any
conditions attached to the pipeline, and finally hand off to the
Notification Router if any action requires alerting a human.

## Core Concepts

- **Trigger** — an event that starts a pipeline (e.g. a form submission, a
  scheduled time, or an API call).
- **Action** — a step that does something (send an email, call an API,
  write a record).
- **Condition** — a branch point that decides whether to continue, skip,
  or route to a different action based on pipeline data.

## Pricing Tiers

| Tier       | Pipelines | Monthly Runs | Price/mo |
|------------|-----------|--------------|----------|
| Starter    | 5         | 1,000        | $29      |
| Team       | 25        | 10,000       | $99      |
| Enterprise | Unlimited | Unlimited    | Custom   |

See ![pricing comparison chart](https://example.com/images/nimbusflow-pricing-chart.png)
for a visual breakdown of tier features.

## Supported Integrations

NimbusFlow integrates with common workplace tools including Slack, email
(SMTP), generic REST APIs, and internal ticketing systems via webhook.
