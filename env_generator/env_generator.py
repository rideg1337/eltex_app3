import secrets
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"

routeruser = input('ONT Username:')
routerpass = input('ONT Password:')
teluser = input('Telnet Username:')
telpass = input('Telnet Password:')

secret_key = secrets.token_hex(16)

with open(env_path, "w") as f:
    f.write(f"routeruser={routeruser}\n")
    f.write(f"routerpass={routerpass}\n")
    f.write(f"teluser={teluser}\n")
    f.write(f"telpass={telpass}\n")
    f.write(f"appseckey={secret_key}\n")