# jcm
JumpCloud Manager

# Overview
The jumpcloud manager is a command line tool that streamlines pulling data out of jumpcloud's administration page such as getting system data or user data.

# config file .jcm.ini
\[DEFAULT\]<br/>x-api-key = your_api_key

# Commands
## users
In users you have the following options list-all, associations, info.

List all users
jcm users list-all

List user associations
jcm users associations <<user_id>>

List user information
jcm users info <<user_id>>

## systems
In systems you have the following options list-all, associations

Lists all systems
jcm systems list-all

List associations of one system_id
jcm systems associations <<system_id>>

## admin
In admin you have the following option get-logs

Returns last 24 hours of admin events in json format
jcm admin get-logs 
