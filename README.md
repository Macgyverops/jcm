# jcm
JumpCloud Manager

# Overview
The jumpcloud manager is a command line tool that streamlines pulling data out of jumpcloud's administration page such as getting system data or user data.

# config file .jcm.ini
\[DEFAULT\]<br/>x-api-key = your_api_key

# Commands
## users
In users you have the following options list-all, associations, info.

List all users<br/>
jcm users list-all

List user associations<br/>
jcm users associations <<user_id>>

List user information<br/>
jcm users info <<user_id>>

## systems
In systems you have the following options list-all, associations

Lists all systems<br/>
jcm systems list-all

List associations of one system_id<br/>
jcm systems associations <<system_id>>

## admin
In admin you have the following option get-logs

Returns last 24 hours of admin events in json format<br/>
jcm admin get-logs 
