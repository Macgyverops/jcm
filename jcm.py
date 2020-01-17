#!/usr/bin/env python

#Author Joshua Goldman
#Date Created 11/6/2019
#Purpose simple command line tool for jumpcloud management

#Imports
import requests
import configparser
import click
import json
import datetime
from datetime import timedelta


@click.group()
def cli():
  """JCM List Jumpcloud Objects"""

@cli.group('users')
def users():
  """Commands for Users"""

@users.command('list-all')
#Pulls the user list and dumps it as json, it only pulls the results and not the total.
def list_all_users():
  """List all users"""
  user_data = run_request('https://console.jumpcloud.com/api/systemusers?limit=0')
  user_dump = user_data['results']
  print("\nListing all users:\n")
  for user in user_dump:
    print('\"'+user.get('firstname')+" "+user.get('lastname')+'\", '+user.get('email')+", username: "+user.get('username')+", user_id: "+user.get('id'))
  print("\n")

@users.command('info')
@click.argument('user_id')
def list_user(user_id):
  """Displays user info (user_id)"""
  user_info = get_user(user_id)
  print("All information on the user "+user_info.get('firstname')+" "+user_info.get('lastname')+".\n")
  for item,val in user_info.items():
    print(json.dumps(item)+": "+json.dumps(val))
  print("\n")


@users.command('associations')
@click.argument('user_id')
def list_user_associations(user_id):
  """Lists user associations (user_id)"""
  user_info = get_user(user_id)
  requests_url = 'https://console.jumpcloud.com/api/v2/users/'+user_id+'/memberof'
  user_dump = run_request(requests_url)
  print("\nThe supplied user \""+user_info.get('displayname')+'\" has been assigned the following user groups')
  for item in user_dump:
    print(item['compiledAttributes']['ldapGroups'][0]['name'])
  print("\n")

@cli.group('systems')
def systems():
  """Commands for Systems"""

@systems.command('list-all')
#Pulls the system list and dumps it as json, it only pulls the results and not the total.
def list_all_systems():
  """Lists all systems"""
  system_data = run_request('https://console.jumpcloud.com/api/systems')
  system_dump = system_data['results']
  print("\nListing all systems:\n")
  for system in system_dump:
    print(system.get('displayName')+', '+system.get('id'))

@systems.command('associations')
@click.argument('system_id')
def list_system_associations(system_id):
  """Lists known associations of a system. e.g. system groups and user groups"""
  requests_url='https://console.jumpcloud.com/api/v2/systems/'+system_id+'/usergroups'
  system_dump = run_request(requests_url)
  print("\nThe supplied system_id "+system_id+' has been assigned the following user groups')
  for item in system_dump:
    print(item['compiledAttributes']['ldapGroups'][0]['name'])
  print("\nThe supplied system_id "+system_id+' system is a member of the following system groups')
  requests_url='https://console.jumpcloud.com/api/v2/systems/'+system_id+'/memberof'
  memberof_dump = run_request(requests_url)
  for members in memberof_dump:
    print(get_system_group_name(members.get('id')))
  print("\n")

@cli.group('admin')
def admin():
  """Administrative Commands"""

@admin.command('get-logs')
def get_logs():
  """Retrieves administrative events log from Jumpcloud, 24hrs by default"""
  requests_url='https://events.jumpcloud.com/events'
  # Need to add starttime and endtime to payload
  endtime=datetime.datetime.utcnow().replace(microsecond=0).isoformat()
  starttime=datetime.datetime.isoformat(datetime.datetime.utcnow().replace(microsecond=0) - timedelta(hours = 24))
  payload = "startDate="+starttime+"Z&endDate="+endtime+"Z"
  #payload="startDate=2020-01-16T19:57:14Z&endDate=2020-01-17T19:57:14Z"
  logs_dump = run_request(requests_url,payload)
  print(json.dumps(logs_dump,indent=4))

#Lets pull the config data
def init_config():
  config = configparser.ConfigParser()
  config.read('.jcm.ini')
  global x_api_key 
  x_api_key = config['DEFAULT']['x-api-key']
  global headers
  headers = { 'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': x_api_key }
  global payload
  payload = ''

def get_system_group_name(system_group_id):
  system_group_url = 'https://console.jumpcloud.com/api/v2/systemgroups/'+system_group_id
  system_group = run_request(system_group_url)
  return system_group.get('name')

def get_user(user_id):
  user_url = 'https://console.jumpcloud.com/api/systemusers/'+user_id
  user = run_request(user_url)
  return user

def run_request(re_url,payload = ''):
  try:
    re = requests.get(re_url,params=payload,headers=headers,timeout=3)
    re.raise_for_status()
  except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh); return
  except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc); return
  except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt);return
  except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err); return  
  return re.json()

#Main
if __name__ == '__main__':
  init_config()
  cli()
