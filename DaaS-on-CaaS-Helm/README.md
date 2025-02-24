# DaaS on CaaS

This project enables you to deploy and run KasmWeb images on a CaaS (Container as a Service) provider, such as ArvanCloud CaaS. KasmWeb provides a variety of pre-configured container images for desktops, browsers, and tools, making it easy to spin up isolated environments for development, testing, or general use.

## Features

- **Pre-configured Images**: Use tested and verified container images like `ubuntu-bionic-desktop`, `chrome`, `tor-browser`, `vlc`, and more.
- **Customizable Resources**: Adjust CPU, memory, and storage limits/requests based on your requirements.
- **Easy Deployment**: Deploy on any CaaS provider with minimal configuration.

## Supported Images

The following images have been tested and are confirmed to work without issues:

- `ubuntu-focal-dind-rootless`
- `terminal`
- `desktop`
- `chrome`
- `tor-browser`
- `vlc`
- `edge`
- `only-office`
- `discord`
- `postman`
- `insomnia`
- `ubuntu-bionic-desktop:1.10.0`

## Configuration

The `values.yaml` file contains the configuration for deploying KasmWeb. Below is an example configuration:

```yaml
env:
  VNC_PW: "password"  # Set your VNC password here
replicaCount: 1
image:
  repository: kasmweb/ubuntu-bionic-desktop  # Image repository
  tag: 1.16.0                                # Image tag
  pullPolicy: IfNotPresent
resources:
  limits:
    cpu: "1"                                 # CPU limit
    ephemeral-storage: 1G                    # Ephemeral storage limit
    memory: 2G                               # Memory limit
  requests:
    cpu: "1"                                 # CPU request
    ephemeral-storage: 1G                    # Ephemeral storage request
    memory: 2G                               # Memory request
service:
  clusterIP: ""                              # Cluster IP (leave empty for dynamic assignment)
  loadBalancerIP: ""                         # Load balancer IP (if applicable)
