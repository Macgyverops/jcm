#!/usr/bin/env python
import requests
import configparser
import click
import json

def init_config():
  #import the config mainly need just the api key but there may be more to configure later like system groups
  config = configparser.ConfigParser()
  config.read('jcm.ini')
  global x_api_key 
  x_api_key = config['DEFAULT']['x-api-key']
  global headers
  headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': x_api_key }

def list_users():
  user_data = requests.get('https://console.jumpcloud.com/api/systemusers', headers=headers)
  return user_data.content

if __name__ == '__main__':
  init_config()
  print(list_users())
