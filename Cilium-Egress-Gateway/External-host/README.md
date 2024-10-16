# Routing Pod Traffic with External host

In some cases, we need to whitelist an IP address. However, when using a CaaS (Container as a Service) provider that doesn’t offer a specific IP for your scenario, this becomes problematic. In such situations, we can use an external host to forward the traffic and whitelist the external host's IP address as an alternative solution.

## What's in app.py

In this Flask application, we can handle two types of HTTP requests:

- **POST**: Used when we want to send a request with data.
- **GET**: Used to retrieve something from the destination (or a default response).

All you need to do is set your destination in the application.

```bash
# Replace your destination URL in the app.py file
destination_url = "http://188.1xx.xxx.xx:8080"
```

## Proxy Application in Docker

In this scenario, we create a Python app to proxy traffic, which we will run in Docker.

```bash
# Build the Flask app image
docker build -t flask-app .

# Run the Docker Compose file
docker compose up --build
```

The proxy app listens on port 5000. We can send requests to it, and it will forward them to the specified destination.

## Pod and Testing

We create a curl pod to send requests to the external host.

```bash
# Create the pod
kubectl apply -f deployment.yaml

# Send a request
kubectl exec -it curl-deployment-xxxx -- curl http://external-host-ip:5000/
```

This setup allows us to route traffic through the external host and work around IP whitelisting limitations.
