# ticket_generator

Create a ec2 instance on aws cloud

Connect to ec2 instance and run install docker.
install docker:
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
docker ps
sudo docker ps
docker ps

Clone this repo 
git clone https://github.com/vinodimdevops/ticket_generator.git


cd ticket_generator

Build and run docker:
docker build -t ticket_generator .
docker run -d -p 5000:5000 ticket_generator

to login inside docker:
docker exec -it cont_Id bash

Use url to access : http://publicIp:5000/

