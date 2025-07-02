# ELTEX DHCP PULLER



## Pelda az inditashoz:

### Commandlineba

 `python`
 `import secrets; print(secrets.token_hex(16))`


 `cd /path/to/app`

 `touch .env` vagy egyszeruen hozz letre a fajlt majd vigyuk fel a parametereket igy:

 ```
 debug=True
 routeruser=felhasznalonev
 routerpass=jelszo
 teluser=felhasznalonev
 telpass=telnetjelszo
 appseckey=nagyontitkosappseckey
 ```

 `docker build -t eltex_dhcp_puller . `

 `docker run -d -p 5055:5055 --env-file .env --name eltex_dhcp eltex_dhcp_puller`
 ### fontos hogy az `--env-file .env` legyen hozzaadva mivel az erzekeny adatokat innen fogja behuzni a docker