# ELTEX DHCP PULLER



## Pelda az inditashoz:

### .env Generalasa
 Az `.env` fajlba kerulnek az erzekeny adatok amiket a script hasznal (username-password stb), ez nelkulozhetetlen a biztonsagos inditashoz, es szukseges legeneralnunk.
 Konnyeden letudod generalni;

 Commandline:

 `cd /path/to/project`

 Majd futtasd ezt:

 `python env_generator.py`

 Vidd be az adatokat amiket ker: (ezek megszokott adatok, kollegaknak nem reszletezem)

 routeruser=felhasznalonev
 routerpass=ontjelszo
 teluser=telnetfelhasznalonev
 telpass=telnetjelszo

 Majd ha bevitted az adatokat akkor o legeneralja a `.env` fajlt ez fontos hogy generald le magadnak es ne add oda senkinek!!! Foleg NE pushold github-ra!!!

 ### Futtatas
 Futtathatod direkt python-bol/terminalbol:

 Root folderban futtasd:

 `python app.py`

 Docker buildelese es futtatasa:

 `docker build -t eltex_dhcp_puller . `

 `docker run -d -p 5055:5055 --env-file .env --name eltex_dhcp eltex_dhcp_puller`

  Fontos hogy az `--env-file .env` legyen hozzaadva mivel az erzekeny adatokat a bejelentkezeshez innen fogja behuzni a docker