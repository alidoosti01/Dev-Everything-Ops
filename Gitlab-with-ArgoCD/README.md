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
