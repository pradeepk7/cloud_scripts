#!/usr/bin/python
# 0 3 * * * cd /apps/scripts; python ldap_sync.py > /dev/null 2>&1

import subprocess
import datetime

sync = subprocess.call(('boto-rsync', 's3://itops-ldap/', '/apps/scripts/ldapsync/'))

def datestamp():
    '''
    returns current date as a string
    '''
    full = datetime.datetime.now().strftime("-%Y-%m-%d")
    return full

# Initial load:
username_uid = "/apps/scripts/ldapsync/ldapuser"
userterm = "/apps/scripts/ldapsync/ldapterm"
groups_gid_username = "/apps/scripts/ldapsync/ldapgroup"
# Use this after initial load:
#username_uid = "/apps/scripts/ldapsync/ldapdiff"
#userterm = "/apps/scripts/ldapsync/ldaptermdiff"
#groups_gid_username = "/apps/scripts/ldapsync/ldapgroupdiff"

ldapusers = []
ldapterms = []
ldapgroups = []

with open(username_uid + datestamp()) as users:
    for line in users:
        ldapusers.append([str(n) for n in line.strip().split(',')])
for pair in ldapusers:
    try:
        username,uid = pair[0],pair[1]
        # user mods
        print username,uid
        add = subprocess.call(('useradd', '-s', '/bin/bash', '-g 104', '-u', uid, username))
        #mod = subprocess.call(('usermod', '-u', uid, username))
    except IndexError:
        print "A line in the file doesn't have enough entries."
users.close()

with open(userterm + datestamp()) as terms:
    for line in terms:
        ldapterms.append([str(n) for n in line.strip().split(',')])
for pair in ldapterms:
    try:
        usertrm,uidtrm = pair[0],pair[1]
        # user terms
        print usertrm,uidtrm
        term = subprocess.call(('userdel', '-f', usertrm))
        remhome = subprocess.call(('rm', '-Rf' , '/home/' + str(usertrm)))
    except IndexError:
        print "A line in the file doesn't have enough entries."
terms.close

with open(groups_gid_username + datestamp()) as usrgrps:
    for line in usrgrps:
        ldapgroups.append([str(n) for n in line.strip().split(',')])
for pair in ldapgroups:
    try:
        group,gid = pair[0],pair[1]
        # group mods
        add = subprocess.call(('groupadd', '-fg', gid, group))
        for user in range(2,len(pair)):
         usergrp = pair[user]
         print group,gid,usergrp
         usrgrp = subprocess.call(('usermod', '-a', '-G', group, usergrp))
    except IndexError:
        print "A line in the file doesn't have enough entries."
usrgrps.close()