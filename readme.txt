"""
SUMMARY

The purpose of mail.py script is to find someone's email address. 
Please use it responsibly.

First, it reads a csv file categorized 
with first name, last name, and website domain. 

It then provides different email possibilities based on that information 
and feeds the different email possibilities to a server that determines
if the email address is real or not. All valid email addresses are outputted to 
a separate csv file called email_dump.csv.



INSTRUCTIONS

1. Execute mail.py from terminal 
2. Include a people.csv file in same directory with three separate columns (first name, last name, domain) 

SOURCES 

possible_emails and complile_emails are functions
pulled from https://github.com/Nateliason/Find-Email-Python repository 
by Nate Liason

request_server uses a server application created by Graham Hunter.
To learn more visit: 
http://marketergraham.com/turning-data-into-leads/

"""