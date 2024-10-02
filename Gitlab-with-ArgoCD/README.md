# Gitlab with ArgoCD UI

in this scenario we use ArgoCD for Gitlab to use it for CD.

in this argo docs:
[ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)

the best practice is the create separate repo for ArgoCD.

we build an image and push it on our gitlab registry and after that update deployment file and push it to ArgoCD repo.

## Code change Repo

the tree of this repo:

```bash
.
├── .gitlab-ci.yaml
├── Dockerfile
├── README.md
├── ci-template
│   ├── build.yaml
│   └── deploy.yaml
├── kubernetes
│   ├── deployment.yaml
│   └── service.yaml
└── nginx
    └── index.html
```
<br>

and the `ArgoCD-repo` directory is the repository where is the ArgoCD read the manifest and updated application.

<br>

<details close>
<summary>Deploy with ArgoCD-CLI</summary>
<br>
it means we create our application with CLI and after that we can see our application from GUI ArgoCD panel.

<br>

- Create new user in ArgoCD
- Create and set role for new user
- Set password for new user

```bash
# edit configMap
kubectl edit configmap argocd-cm -n argocd

# add this command
data:
  accounts.<username>: apiKey,login

# edit ArgoCd rbac configMap
kubectl edit configmap argocd-rbac-cm -n argocd

# add role and assign it to user
data:
  policy.csv: |
    p, role:newrole, applications, get, */*, allow
    p, role:newrole, applications, create, */*, allow
    p, role:newrole, applications, delete, */*, allow
    g, <username>, role:newrole

# set password
argocd account update-password --account <username>
```

add job for create application with argoCD cli:

```yaml
# .gitlab-ci.yaml
include:
  - /ci-template/release.yaml

# create release.yaml file in ci-template directory
release:
  stage: release
  image: alpine:3.18
  dependencies:
    - deploy
  before_script:
    - apk add --no-cache curl git envsubst bash
    - curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
    - install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
    - rm argocd-linux-amd64
    - git clone https://gitlab.{{ DOMAIN }}.ir/test/argocd-runner-test.git
    - argocd login $ARGO_SERVER --username $ARGO_USERNAME --password $ARGO_PASSWORD
  script:
    - cd argocd-runner-test
    - argocd app create cdclitest --repo https://gitlab.{{ DOMAIN }}.ir/test/argocd-runner-test.git --path . --dest-server https://kubernetes.default.svc --dest-namespace default --sync-policy auto
```

</details>
