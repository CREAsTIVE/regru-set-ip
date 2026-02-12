# regru-set-ip

CLI tool to update an A record (alias) on REG.RU via their API.

---

## Requirements
- Python 3.6+
- `regru-api`, `python-dotenv`

## Installation
```bash
sudo curl -sSL https://raw.githubusercontent.com/CREAsTIVE/regru-set-ip/master/install.sh | bash
```

## Configuration
Edit `.env` in the installation directory:
```ini
REGRU_LOGIN=your-email@example.com
REGRU_PASSWORD=your-password
```

## Uninstall
```bash
sudo curl -sSL https://raw.githubusercontent.com/CREAsTIVE/regru-set-ip/master/uninstall.sh | bash
```

## Usage
```bash
regru-set-ip <domain> <subdomain> <new_ip>
```
- `domain` – domain managed at REG.RU (e.g., `example.ru`)
- `subdomain` – part before the domain.  
  - `@` – the domain itself  
  - `*` – wildcard (any subdomain)  
  - `www` – `www.example.ru`  
  - `a.b` – `a.b.example.ru`
- `new_ip` – IPv4 address for the A record

## License
MIT