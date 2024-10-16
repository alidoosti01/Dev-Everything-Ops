# Cilium Egress Gateway Policy

In this scenario, we want to route traffic from a node to specific destinations. For example, we may need to whitelist an IP address to send traffic to a specific destination.
In Kubernetes, if a pod is rescheduled on a different node, the traffic from this pod will be routed through the new node.
However, if we whitelist an IP address while the pod is on the old node, and the pod gets rescheduled, its egress IP will change, which can cause issues.

To solve this problem, we use the `CiliumEgressGatewayPolicy` to define how to route specific pod traffic to specific destinations, ensuring the correct IP address is used.

## Install Cilium

We use Helm to install Cilium. In the Helm values file, we need to enable three features: `egressGateway`, `bpf masquerade`, and `kubeproxy replacement`:

```bash
# Enable the required features

helm install cilium cilium/cilium --version 1.16.2 --namespace kube-system --set egressGateway.enabled=true --set bpf.masquerade=true --set kubeProxyReplacement=true
```

**Note**: If Cilium is already installed, you only need to upgrade it by setting these three parameters using the `--reuse-values` command.

After the upgrade, restart the agent pod and operator pod to make the changes effective:

```bash
kubectl rollout restart ds cilium -n kube-system

kubectl rollout restart deploy cilium-operator -n kube-system
```

## Writing the Egress Gateway Policy and Testing It

Here is an example of an egress gateway policy:

```yaml
# Cilium egress gateway policy

apiVersion: cilium.io/v2
kind: CiliumEgressGatewayPolicy
metadata:
  name: egress-sample
spec:
  egressGateway:
    nodeSelector:
      matchLabels:
        # We set the egress-node=true label on the node we want to be the egress gateway
        egress-node: "true"
        kubernetes.io/hostname: "k8s-worker-2"

    # If a node has multiple interfaces, we can set a specific interface to route the traffic
    interface: eth0

  destinationCIDRs:
    - a.b.0.0/16
    - a.b.c.0/24
  selectors:
  - podSelector:
      matchLabels:
        app: my-app
```

An application for testing:

```yaml
# Curl pod

apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
  - name: my-app
    image: curlimages/curl
    command: ["sleep", "3600"]
  nodeSelector:
    # Ensure this pod is scheduled on another node
    kubernetes.io/hostname: k8s-worker-1
```

To test the policy, you can run the following command:

```bash
kubectl exec -it my-app -- curl http://destination-ip:port
```

## Adding a Label to the Node and Troubleshooting

To add a label to a node:

```bash
kubectl label nodes k8s-worker-2 egress-node=true
```

You can view the egress configuration on the Cilium agent with:

```bash
kubectl -n kube-system exec ds/cilium -- cilium-dbg bpf egress list

# Example output
Source IP       Destination CIDR    Egress IP   Gateway IP
192.168.1.126   188.1xx.xxx.xx/32   0.0.0.0     37.1xx.xxx.xxx
```

The `Source IP` address matches the IP address of the pod that corresponds to the `podSelector` policy.
The `Gateway IP` matches the (internal) IP address of the egress node that corresponds to the policy's `nodeSelector`.
The `Egress IP` is `0.0.0.0` on all agents except for the one running on the egress gateway node, where you should see the Egress IP address being used for the traffic. If an `egressIP` is specified in the policy, this will be reflected in the output.
