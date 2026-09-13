# NimbusFlow — Installation Guide

This guide walks through installing the NimbusFlow on-premise connector,
used when a pipeline needs to reach internal systems that aren't exposed
to the public internet.

## Prerequisites

- Docker 24+ installed on the host machine
- Outbound HTTPS access to `*.nimbusflow.example.com`
- A NimbusFlow **connector token**, generated from Settings → Connectors

## Step-by-Step Setup

1. Pull the connector image:
   ```
   docker pull nimbusflow/connector:latest
   ```
2. Create a config file `connector.yaml`:
   ```yaml
   token: YOUR_CONNECTOR_TOKEN
   region: us-east
   allowed_hosts:
     - internal-api.mycompany.local
   ```
3. Run the connector:
   ```
   docker run -v $(pwd)/connector.yaml:/etc/nimbusflow/connector.yaml nimbusflow/connector:latest
   ```
4. Verify the connection in the NimbusFlow dashboard — a green "Connected"
   badge should appear next to your connector name within 60 seconds.

![Connector status dashboard showing a connected badge](https://example.com/images/nimbusflow-connector-status.png)

## Network Architecture

The connector opens a single outbound connection to NimbusFlow's cloud
control plane and never accepts inbound traffic — this is what allows it
to run behind a corporate firewall without opening any inbound ports.

![Network diagram of the on-premise connector](https://example.com/images/nimbusflow-network-diagram.png)

## Troubleshooting Installation

If the dashboard shows "Disconnected" after 5 minutes:

- Confirm outbound HTTPS (port 443) isn't blocked by a proxy
- Re-check the connector token hasn't expired (tokens expire after 90 days)
- Look at connector logs: `docker logs <container_id>`
