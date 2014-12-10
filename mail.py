"""
Mail.py is a script that reads a csv file categorized 
with first name, last name, and website domain. 

It then provides different email possiblities based on that information 
and feeds the different email possibilities to a server that determines
if the email address is real or not. All valid email addresses are outputed to 
a seperate csv file called email_dump.csv.

The purpose of this script is to find someone's email address. 
Please use it responsibly.

To execute the program. Run it form terminal. Make sure people.csv is in the same directory as 
mail.py.

Please note: 

pulled from https://github.compossible_emails and complile_emails are functions
/Nateliason/Find-Email-Python repository 
by Nate Liason

request_server uses a server application created by Graham Hunter.
To learn more visit: 
http://marketergraham.com/turning-data-into-leads/

"""

import sys, csv, os, requests, re, time

#Persons defines each row in the csv file as a set of variables
class Persons(): 
  def __init__(self, first_name, last_name, domain):
    self.first_name = first_name
    self.last_name = last_name
    self.domain = domain


class Aggregate():

  #Reads people.csv file 
  def start(self):
    people = []

    try:
      with open('people.csv', 'rb') as f:
          reader = csv.reader(f)
          reader.next()
          for row in reader:
              people.append(row) 
    except IOError:
      print "Did not find people.csv. Please place csv in same folder as mail.py."
      raise SystemExit


    return people

  #Creates list of different email possibilities for each row from people.csv
  def compile_list(self, people):  
    
    email_list = []

    try:
      for i in range(len(people)):
        person = Persons(people[i][0], people[i][1], people[i][2])
        email = Index()
        email_list.append(email.complile_emails(person))
    except IndexError:
      print "It looks like people.csv is formatted incorrectly. Make sure you have a first name, last name, and domian for each row."
      raise SystemExit
      
    return email_list
 

class Index():

  #Called within "complile_emails" and returns a string in email format
  def possible_emails(self, possible_name_combos, at_domain):
    return [item + '@' + at_domain for item in possible_name_combos]


  # All of the basic possible email combinations. Called within compile_list in Aggregate class
  def complile_emails(self, person):
    
    first_name = person.first_name
    last_name = person.last_name
    at_domain = person.domain


    possible_name_combos = []
    possible_emails_list = []
    first_initial        = first_name[:1]
    last_initial         = last_name[:1]


    if first_name != "" and last_name != "":
      possible_name_combos.append(first_name + "." + last_name)
      possible_name_combos.append(first_name + "." + last_initial)
      possible_name_combos.append(first_name)
      possible_name_combos.append(first_name + last_name)
      possible_name_combos.append(first_name + last_initial)
      possible_name_combos.append(first_initial + "." + last_name)
      possible_name_combos.append(first_initial + last_name)
      possible_name_combos.append(last_name + "." + first_name)
      possible_name_combos.append(last_name + "." + first_initial)
      possible_name_combos.append(last_name)
      possible_name_combos.append(last_name + first_name)
      possible_name_combos.append(last_name + first_initial)
    
    if at_domain != '':
      possible_emails_list = self.possible_emails(possible_name_combos, at_domain) 


    return possible_emails_list

class Find():

  #Creates list of urls with appended email possibilities
  def create_url_list(self, email_list):

    url = 'http://email-validation.herokuapp.com/?addr='
    url_list = []


    for i in range(len(email_list)):
      person_url_list = []

      for y in range(len(email_list[i])):
        person_url_list.append(url + email_list[i][y])
      url_list.append(person_url_list)

    return url_list

  #Requests server with urls for create_url_list and returns server message for each url
  def request_server(self, url_list):

    server_list = []

    for i in range(len(url_list)):
      email_server_list = []

      for y in range(len(url_list[i])):
        response = requests.get(url_list[i][y])
        data = response.text
        email_server_list.append(data)
        print data
        time.sleep(1)

      server_list.append(email_server_list)


    return server_list

  #Uses regular expression to extract messages from server. 
  def match(self, server_list):

    match_list = []

    for i in range(len(server_list)):
      match_person_list = []
      for y in range(len(server_list[i])):
        match=re.findall(r'\"(.+?)\"',server_list[i][y])
        match_person_list.append(match)
      match_list.append(match_person_list)
    return match_list

  #Takes list from match function, determines which emails are valid and returns list of emails.
  def validate_email(self, match_list):

    valid = 'Valid email address'
    invalid = 'Invalid email address'

    email_list = []

    for i in range(len(match_list)):
      valid_email_list = []
      ticker = 0
      for x in range(len(match_list[i])):
        if match_list[i][x][1] == valid:
          valid_email_list.append(match_list[i][x][3])
      email_list.append(valid_email_list)

    return email_list

class Write():

  #Outputs elements in "email_list" to seperate csv file
  def csv_write(self, email_list):
      csv_out = open("email_dump.csv", "wb")
      mywriter = csv.writer(csv_out)
      for item in email_list:
        mywriter.writerow(item)
      print "E-mail addresses outputed successfully. Check email_dump.csv."


#code execution
create_file = Aggregate()
people_list = create_file.start()
email_list = create_file.compile_list(people_list)
find_email = Find()
url_list = find_email.create_url_list(email_list)
server_list = find_email.request_server(url_list)
match_list = find_email.match(server_list)
email_list = find_email.validate_email(match_list)
write_email = Write()
write_email.csv_write(email_list)



