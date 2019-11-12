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

@users.command('listall')
#Pulls the user list and dumps it as json, it only pulls the results and not the total.
def list_all_users():
  user_data = requests.get('https://console.jumpcloud.com/api/systemusers', headers=headers)
  user_dump = user_data.json()['results']
  for user in user_dump:
    print('\"'+user.get('firstname')+" "+user.get('lastname')+'\", '+user.get('email'))

@users.command('associations')
def list_user_associations():
  print('wip')

@cli.group('systems')
def systems():
  """Commands for Systems"""

@systems.command('list-all')
#Pulls the system list and dumps it as json, it only pulls the results and not the total.
def list_all_systems():
  """Lists all systems"""
  system_data = requests.get('https://console.jumpcloud.com/api/systems', headers=headers)
  system_dump = system_data.json()['results']
  for system in system_dump:
    print(system.get('displayName')+', '+system.get('id'))

@systems.command('associations')
@click.argument('system_id')
def list_system_associations(system_id):
  """Lists known associations of a system. e.g. system groups and user groups"""
  requests_url='https://console.jumpcloud.com/api/v2/systems/'+system_id+'/usergroups'
  try:
    system_data = requests.get(requests_url,headers=headers,timeout=3)
    system_data.raise_for_status()
  except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh); return
  except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc); return
  except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt);return
  except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err); return
  system_dump = system_data.json()
  print(system_id+' has been assigned the following user groups')
  for item in system_dump:
    print(item['compiledAttributes']['ldapGroups'][0]['name'])

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
