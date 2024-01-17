# FormApp - DevOps Protfolio
This DevOps portfolio serves as a comprehensive demonstration of our academic journey, showcasing a variety of methodologies and skills that we've learnt during our studies.

[![CI](https://github.com/sbendarsky/flask/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sbendarsky/flask/actions/workflows/ci.yml)

## Technical Overview
Our project kicks off with the development of the web application with Python, using the Flask library. To enhance deployment effciency and shareabillity, we encapsulated the application within Docker containers.

### Infrastructure as Code and GitOps Manifest
The heart of our project lies in the [manifest-repo](https://github.com/sbendarsky/manifet-formapp), housing both Infrastructure as Code and the complete GitOps manifest. This repository embodies the GitOps methodologies, facilitating streamlined management and version control.

### CI/CD Pipeline
Powered by GitHub Actions, our Continuous Intergration (CI) pipeline presents itself as a sturdy and automated serverless framework. Triggered on each push to the main branch, the CI proccess starts with building the Docker image. -afterwards the jobs starts a comprehensive testing, utilizing pytest and pylint to ensure code quality and reliability standards. Upon successful completion of all tests, the updated Docker images seamlessly intergrates with Docker Hub. Simultaneously, the CI job orchestrates the synchronization of the manifest-repo with the latest configuration.

### Production Deployment with ArgoCD on AWS EKS
In the production environment, we've deployed ArgoCD on an AWS EKS cluster, upon identification of modfications, ArgoCD initates a synchronization phase, orchestrating a smooth transiton to the updated configuration.

### Repositories
* [Source Code](https://github.com/sbendarsky/formapp-portfolio)
* [manifest-repo](https://github.com/sbendarsky/manifet-formapp)

## Documentation Sources
* [Docker & Docker-Compose](https://docs.docker.com/)
* [Nginx](https://nginx.org/en/docs/)
* [K8S](https://kubernetes.io/docs/home/)
* [Helm](https://helm.sh/docs/)
* [MySQL](https://dev.mysql.com/doc/)
* [Bitnami-Charts](https://github.com/bitnami/charts)
* [Terraform](https://www.terraform.io/docs)
* [AWS](https://docs.aws.amazon.com/)
* [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)
* [GitHub Actions](https://docs.github.com/en/actions)



