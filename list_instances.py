#!/usr/bin/python
# Author: Pradeep R. Kumar
# Source(totally copied and modified): http://stackoverflow.com/questions/15411070/how-do-i-get-boto-to-return-ec2-instances-s3-works-fine
# Boto version: 2.2.2
# Usage: oq-lin.py <region(s)> --> ./oq-lin.py us-east-1 us-west-1

import boto
import boto.ec2

import sys

class ansi_color:
  red   = '\033[31m'
  green = '\033[32m'
  reset = '\033[0m'
  grey  = '\033[1;30m'

def app(i):
  if 'app' in i.tags:
    n = i.tags['app'] 
  elif 'Box' in i.tags:
    n = i.tags['Box']
  elif 'Name' in i.tags:
    n = i.tags['Name']
  else:
    n = 'nil'
  n = n.rjust(35)[:35]
  if i.state == 'running':
    n = ansi_color.green + n + ansi_color.reset
  else:
    n = ansi_color.red + n + ansi_color.reset
  return n

def owner(i):
  if 'owner' in i.tags:
    o = i.tags['owner']
  elif 'UserEmail' in i.tags:
    o = i.tags['UserEmail']
  else:
    o = 'nil'
  o = o.rjust(22)[:22]
  if i.state == 'running':
    o = o
  else:
    o = o
  return o

def inst_id( i ):
  return i.id.rjust(15)

def private_ip( i ):
  return i.private_ip_address.rjust(20)

def public_ip( i ):
  return i.ip_address.rjust(15)

print "%s%s%s%s" % (str('app name').rjust(37),str('instance id').rjust(17),str('address').rjust(20),str('owner').rjust(23))
print "%s%s%s%s" % (str('--------').rjust(37),str('-----------').rjust(17),str('-------').rjust(20),str('-----').rjust(23))

def print_instance( i ):
   print '  ' + app(i) + ' ' + inst_id(i) + ' ' + private_ip(i) + ' ' + owner(i)

regions = sys.argv[1:]
if len(regions)==0:
  regions=['us-west-1']

if len(regions)==1 and regions[0]=="all":
  rr = boto.ec2.regions()
else:
  rr = [ boto.ec2.get_region(x) for x in regions ]

for reg in rr:
  conn = reg.connect()
  reservations = conn.get_all_instances()

  for r in reservations:
  #  print ansi_color.grey + str(r) + ansi_color.reset
    for i in r.instances:
      print_instance(i)

print '[' + reg.name + ']'
