from __future__ import annotations
from typing import Any
import requests
import urllib
import json

class RegRuAPIChain:
  def __init__(self, base: RegRuAPI, thisName: str, parentNames: list[str] = []):
    self.names = [*parentNames, thisName]
    self.base = base

  def __getattr__(self, name: str) -> RegRuAPIChain:
    return RegRuAPIChain(self.base, name, self.names)
  
  def __call__(self, data) -> Any:
    return self.base.post(
      self.base.get_url(self.names),
      data
    )

class RegRuAPI:
  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

  def get_url(self, names: list[str]):
    return f"https://api.reg.ru/api/regru2/{'/'.join(names)}"
  
  def post(self, url: str, data: Any):
    result = requests.post(
      url=url,
      data=urllib.parse.urlencode({
        "input_format": "json",
        "output_format": "json",
        "input_data": json.dumps(data),
        "password": self.password,
        "username": self.username,
      }),
      headers= {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      timeout=60
    )
    return result.json()
  
  def __getattr__(self, name: str) -> RegRuAPIChain:
    return RegRuAPIChain(self, name)