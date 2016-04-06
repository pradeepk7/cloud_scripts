#!/usr/bin/python
from fabric.api import *
# For ip-### regexp matching
import re

env.hosts = ['10.0.0.10','10.0.0.11']
env.key_filename = 'mykey'
env.user = 'ubuntu'

def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

osflavor = (str(platform.dist()))

# 1. Get list of systems. See oq-lin script
def list_instances():

# 2. Use 'app-name' field in oq-lin as an alternative hostname for systems that do not have hostnames.
#    If app-name contains underscores and/or whitespace, convert those to dashes.
 def app_name():

# 3. Loop through IPs(address field) in oq-lin and execute remote SSH commands
  class host_processor():
        # a.  check OS
        def check_os():

        # a.  check whether hostname matches 'ip-###' pattern'
         def check_hostname():
          with settings (hide('stdout','running','warnings'), warn_only=True):
           host = run('hostname')
           if re.search('ip-', host, re.IGNORECASE):
            return host
         # b. if check_hostname is true, then replace with app_name
          def replace_hostname():
           if re.search('Ubuntu', osflavor, re.IGNORECASE):
                run('hostname',app_name)
                run('echo app_name > /etc/hostname')
           elif re.search('Centos', osflavor, re.IGNORECASE):
                run('hostname',app_name)
                run('sed -i "/'app_name'/d" /etc/sysconfig/network')
           else:
                print "Unknown or Windows OS"
                                        
