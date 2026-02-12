import os
import sys
from typing import Any
from dotenv import load_dotenv
import regru_api

def handle_api_response(response: Any, action_description: str) -> None:
    # Check overall method status
    if response.get('result') == 'error':
        error_code = response.get('error_code', 'UNKNOWN')
        error_text = response.get('error_text', 'Unknown error')
        print(f"ERROR: {action_description} — {error_code}: {error_text}", file=sys.stderr)
        sys.exit(1)

    # If there is an answer with domains, inspect each domain
    answer = response.get('answer', {})
    domains = answer.get('domains', [])
    for domain_info in domains:
        if domain_info.get('result') == 'error':
            dname = domain_info.get('dname', '<no domain>')
            error_code = domain_info.get('error_code', 'UNKNOWN')
            error_text = domain_info.get('error_text', '')
            print(f"WARNING: {action_description} for {dname}: {error_code} {error_text}")

usage = lambda x: f"""Removes current subdomain A record to replace it with new
Usage: 
  {x} domain subdomain new_ip
Where:
  - domain: managed domain, like "some-domain.ru"
  - subomain: part before ".some-domain.ru", like "a.b" for "a.b.some-domain.ru"
    define as "@" for managed domain itself, use "*" for any subdomain
  - new_ip: new A record, that will be created
"""

def updateDomainZoneIp(login: str, password: str, domain: str, subdomain: str, ip: str) -> None:
    api = regru_api.RegRuAPI(login, password)

    # 1. Remove existing A record (if any)
    remove_response = api.zone.remove_record({
        "domain_name": domain,
        "subdomain": subdomain,
        "record_type": "A"
    })
    handle_api_response(remove_response, f"removing A record for {domain}")

    # 2. Add new A record (alias)
    add_response = api.zone.add_alias({
        "domain_name": domain,
        "subdomain": subdomain,
        "ipaddr": ip
    })
    handle_api_response(add_response, f"adding A record for {domain}")

def main():
    load_dotenv()
    
    login = os.getenv("REGRU_LOGIN")
    password = os.getenv("REGRU_PASSWORD")
    if not login or not password:
        print("ERROR: REGRU_LOGIN and/or REGRU_PASSWORD not set in .env file", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) != 4:
        print(usage(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    domain = sys.argv[1]
    subdomain = sys.argv[2]
    ip = sys.argv[3]

    updateDomainZoneIp(login, password, domain, subdomain, ip)

if __name__ == "__main__":
    main()