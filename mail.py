"""mail.py is a script that reads a csv file categorized 
with first name, last name, and website domain. 
Provides different email possiblities based on that information 
and outputs the different possibilites as a seperate csv file. 
The purpose of this script is to find someone's email address. 
Just paste a row from the outputed csv into compose in gmail.
Hover over each of the possibilities and the profile of an 
individual will show up on the rapportive app on the left side of 
gmail."""


import sys, csv, os


#Class that is used to define each row in the csv file

class Persons: 
  def __init__(self, first_name, last_name, domain):
    self.first_name = first_name
    self.last_name = last_name
    self.domain = domain

#Reads people.csv file when called and then stores each row as a list 

def csvread():
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

#Outputs elements in "email_list" to seperate csv file

def csvwrite(email_list):
    csv_out = open("email_dump.csv", "wb")
    mywriter = csv.writer(csv_out)
    for item in email_list:
      mywriter.writerow(item)
    print "E-mail addresses outputed successfully. Check email_dump.csv."

 
'''Please note that possible_emails and complile_emails are functions
pulled from https://github.com/Nateliason/Find-Email-Python repository 
by Nate Liason'''


#Called within "complile_emails" and returns a string in email format

def possible_emails(possible_name_combos, at_domain):
  return [item + '@' + at_domain for item in possible_name_combos]


# All of the basic possible email combinations. 


def complile_emails(person):
  
  first_name = person.first_name
  last_name = person.last_name
  at_domain = person.domain


  possible_name_combos = []
  possible_emails      = []
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
    possible_emails = possible_emails(possible_name_combos, at_domain) 


  return possible_emails


# Defines person object and passes object to complile_emails function
def main(people):
    
  email_list = []

  for i in range(len(people)):
    person = Persons(people[i][0], people[i][1], people[i][2])
    email_list.append(complile_emails(person))
    
  return email_list 



csvwrite(main(csvread()))





