# regru-set-ip

CLI tool to update an A record (alias) on REG.RU via their API.

---

## Requirements
- Python 3.6+
- `regru-api`, `python-dotenv`

## Installation
```bash
pip install regru-api python-dotenv
```
Save script as `regru-set-ip`, `chmod +x` (Linux/macOS).

## Configuration
Create `.env` in the same directory:
```ini
REGRU_LOGIN=your-email@example.com
REGRU_PASSWORD=your-password
```
**Never commit `.env`.** Use `.env.example` as a template.

## Usage
```bash
regru-set-ip <domain> <subdomain> <new_ip>
```

**Arguments:**
- `domain` – domain managed at REG.RU (e.g., `example.ru`)
- `subdomain` – part before the domain.  
  - `@` – the domain itself  
  - `*` – wildcard (any subdomain)  
  - `www` – `www.example.ru`  
  - `a.b` – `a.b.example.ru`
- `new_ip` – IPv4 address for the A record

## Example
```bash
regru-set-ip cyberbiology.ru test 46.146.112.201
```
Output:
```
WARNING: removing A record for cyberbiology.ru: RR_NOT_FOUND ...
adding A record for cyberbiology.ru
```
(Warning is normal if no A record existed.)

## How it works
1. Reads credentials from `.env`.
2. Removes existing A record for the subdomain.
3. Adds a new A record (alias) with the given IP.
4. Handles API errors:
   - Method‑level errors → `ERROR: …` and exit.
   - Domain‑level errors → `WARNING: …` and continue.

## License
MIT