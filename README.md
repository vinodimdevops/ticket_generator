# Ticket Generator

This project, `ticket_generator`, is designed to generate event tickets with a Dockerized application. Follow the steps below to set up an EC2 instance on AWS, install Docker, and deploy the application.

## Prerequisites

- **AWS EC2 Instance**: Ensure you have an EC2 instance set up on AWS.
- **Ubuntu**: The instructions assume you are using an Ubuntu-based EC2 instance.

## Installation Guide

### 1. Connect to the EC2 Instance
Log in to your EC2 instance using SSH.

### 2. Install Docker
Run the following commands to install Docker on your EC2 instance:

```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
```
####  Verify Docker Installation
Check if Docker is running with:
```bash
sudo systemctl status docker
```
#### Add User to Docker Group
To run Docker without sudo, add your user to the Docker group:
```bash
sudo usermod -aG docker ${USER}
```

### 3. Clone the Repository
Clone this repository to your EC2 instance:

```bash
git clone https://github.com/vinodimdevops/ticket_generator.git
cd ticket_generator
```

### 4. Build and Run the Docker Container
Build the Docker image:
```bash
docker build -t ticket_generator .
```
Run the Docker container, mapping port 5000:
```bash
docker run -d -p 5000:5000 ticket_generator
```
Access the Application
You can access the application in your browser at:
```bash
http://<public-ip>:5000/
```

### 5. Optional: Access Docker Container Shell
To open an interactive shell within the running container, use:
```bash
docker exec -it <container_id> bash
```
Replace <container_id> with the actual ID of the running container, which you can find using:
```bash
docker ps
```
