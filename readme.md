docker build -t eltex_dhcp_puller . 

docker run -d -p 5055:5055 --env-file .env --name eltex_dhcp_container eltex_dhcp_puller
