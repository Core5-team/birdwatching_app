# Birdwatching Application & Automation

This repository contains the Birdwatching Flask application and automation used to deploy and configure the platform.

**Deployment is triggered via Jenkins.**

Jenkins pipelines defined in this repository must be created and run in Jenkins. Executing these pipelines provisions and configures the system using Ansible, Consul and Nginx.

## Jenkins Pipelines

Jenkinsfiles in this repository are the entry point for deployment:

- Each Jenkinsfile represents a pipeline to configure part of the system
- Pipelines are created in Jenkins and executed there
- Running the pipelines launches and configures the environment
- This is the supported deployment model.

## Repository Content

- Flask application code
- Ansible playbooks and roles
- Jenkins pipelines
- Consul configuration and templates
- Load balancer configuration
- Monitoring templates
- Legacy Documentation

Vagrant-based documentation is legacy and kept for reference only.

See: [docs/README.md](https://github.com/Core5-team/birdwatching_app/blob/main/docs/README.md)

Sections titled Vagrant Setup and Jenkins & Ansible Setup for BirdWatchingFlask
