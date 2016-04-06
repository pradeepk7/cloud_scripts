#!/usr/bin/python
# sudo apt-get install -y python-pip
# sudo chmod 755 /path/to/scripts/r53_salt_dereg.py
# sudo ln -s /path/to/scripts/r53_salt_dereg.py /usr/local/bin/r53_salt_dereg
# sudo pip install fabric
# %users    ALL=NOPASSWD: /usr/local/bin/r53_salt_dereg
# usage: sudo r53_salt_dereg <my_short_hostname>

import os
import sys
from fabric.api import *

env.host_string = 'saltstack-syndic.someorg.com'
env.key_filename = 'mykey.pem'
env.user = 'ubuntu'

if len(sys.argv) == 2:
   host=str(sys.argv[1])

   print ('Removing %s from Route53 DNS...' % (host))
   remhost = os.system("/usr/bin/salt-call -l quiet event.fire_master {'id':'%s'} 'route53-destroy'" % (host))
   print ('Removed.')

   def saltDereg():
     with settings (hide('stdout','running','warnings'), warn_only=True):
         #out = run('sudo salt-key -L | grep %s' % (host))
         out = run('sudo salt-key -d %s.someorg.com -y' % (host))
         return out

   print ('Deregistering %s from the Salt system...' % (host))
   print ("%s"%saltDereg())

else:
   print "USAGE: r53_salt_dereg <myhostname>.  Hostname does not support globbing(currently)."
   sys.exit()
