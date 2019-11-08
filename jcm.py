#!/usr/bin/env python

#Author Joshua Goldman
#Date Created 11/6/2019
#Purpose simple command line tool for jumpcloud management

#Imports
import requests
import configparser
import click
import json

@click.group()
def cli():
  """JCM List Jumpcloud Objects"""

@cli.group('users')
def users():
  """Commands for Users"""

@users.command('list')
#Pulls the user list and dumps it as json, it only pulls the results and not the total.
def list_all_users():
  user_data = requests.get('https://console.jumpcloud.com/api/systemusers', headers=headers)
  user_dump = user_data.json()['results']
  for user in user_dump:
    print('\"'+user.get('firstname')+" "+user.get('lastname')+'\", '+user.get('email'))


@cli.group('systems')
def systems():
  """Commands for Systems"""

@systems.command('list')
#Pulls the system list and dumps it as json, it only pulls the results and not the total.
def list_all_systems():
  system_data = requests.get('https://console.jumpcloud.com/api/systems', headers=headers)
  system_dump = system_data.json()['results']
  for system in system_dump:
    print('\"'+system.get('displayName')+'\"')

#Lets pull the config data
def init_config():
  config = configparser.ConfigParser()
  config.read('.jcm.ini')
  global x_api_key 
  x_api_key = config['DEFAULT']['x-api-key']
  global headers
  headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': x_api_key }

#Main
if __name__ == '__main__':
  init_config()
  cli()
  for user in userdump:
    print('\"'+user.get('firstname')+" "+user.get('lastname')+'\", '+user.get('email'))
