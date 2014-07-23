#!/bin/bash -x

# username,uid
ldapuser () 
{
 ldapsearch -LL -x -H "ldaps://localhost" -D cn=admin,dc=myorg,dc=net -w secret -b ou=people,dc=myorg,dc=net "(&(objectClass=person)(objectClass=posixAccount))" uidNumber | awk '{print $2}' | awk -F, '{print $1}' | tr '\n[0-9]' ',[0-9]*' | sed 's/',,'/\
/g' | grep -v archived | grep -v vendor | cut -c 5- | grep -v '^[0-9]' | sed '/^$/d' | sort -u
}

# group,gid,members(username)
ldapgroup ()
{
 ldapsearch -LL -x -H "ldaps://localhost" -D cn=admin,dc=myorg,dc=net -w secret -b ou=group,dc=myorg,dc=net "(objectClass=posixGroup)" gidNumber memberUid | awk '{print $2}' | awk -F, '{print $1}' | tr '\n[0-9]' ',[0-9]*' | sed 's/',,'/\
/g' | grep -v archived | grep -v vendor | cut -c 4- | grep -v '^[0-9]' | sed '/^$/d' | sort -u
}

# username,uid
ldapterm ()
{
ldapsearch -LL -x -H "ldaps://localhost" -D cn=admin,dc=myorg,dc=net -w secret -b ou=archivedPeople,dc=myorg,dc=net "(&(objectClass=person)(objectClass=posixAccount))" uidNumber | awk '{print $2}' | awk -F, '{print $1}' | tr '\n[0-9]' ',[0-9]*' | sed 's/',,'/\
/g' | grep -v archived | grep -v vendor | cut -c 5- | grep -v '^[0-9]' | sed '/^$/d' | sort -u
}

ldapdiff ()
{
comm -3 /apps/sysadmin/ldap_csv/ldapuser-$(date '+%F') /apps/sysadmin/ldap_csv/ldapuser-$(date -d "1 day ago" '+%F') | sed -e 's/^[ \t]*//'
}

ldaptermdiff ()
{
comm -3 /apps/sysadmin/ldap_csv/ldapterm-$(date '+%F') /apps/sysadmin/ldap_csv/ldapterm-$(date -d "1 day ago" '+%F') | sed -e 's/^[ \t]*//'
}

ldapgroupdiff ()
{
comm -3 /apps/sysadmin/ldap_csv/ldapgroup-$(date '+%F') /apps/sysadmin/ldap_csv/ldapgroup-$(date -d "1 day ago" '+%F') | sed -e 's/^[ \t]*//'
}

ldapuser > /apps/sysadmin/ldap_csv/ldapuser-$(date '+%F')
ldapgroup > /apps/sysadmin/ldap_csv/ldapgroup-$(date '+%F')
ldapterm > /apps/sysadmin/ldap_csv/ldapterm-$(date '+%F')
ldapdiff > /apps/sysadmin/ldap_csv/ldapdiff-$(date '+%F')
ldaptermdiff > /apps/sysadmin/ldap_csv/ldaptermdiff-$(date '+%F')
ldapgroupdiff > /apps/sysadmin/ldap_csv/ldapgroupdiff-$(date '+%F')

s3cmd put /apps/sysadmin/ldap_csv/ldapuser-$(date '+%F') s3://itops-ldap/
s3cmd put /apps/sysadmin/ldap_csv/ldapgroup-$(date '+%F') s3://itops-ldap/
s3cmd put /apps/sysadmin/ldap_csv/ldapterm-$(date '+%F') s3://itops-ldap/
s3cmd put /apps/sysadmin/ldap_csv/ldapdiff-$(date '+%F') s3://itops-ldap/
s3cmd put /apps/sysadmin/ldap_csv/ldaptermdiff-$(date '+%F') s3://itops-ldap/
s3cmd put /apps/sysadmin/ldap_csv/ldapgroupdiff-$(date '+%F') s3://itops-ldap/

s3cmd del s3://itops-ldap/ldapuser-$(date -d "1 day ago" '+%F')
s3cmd del s3://itops-ldap/ldapgroup-$(date -d "1 day ago" '+%F')
s3cmd del s3://itops-ldap/ldapterm-$(date -d "1 day ago" '+%F')
s3cmd del s3://itops-ldap/ldapdiff-$(date -d "1 day ago" '+%F')
s3cmd del s3://itops-ldap/ldaptermdiff-$(date -d "1 day ago" '+%F')
s3cmd del s3://itops-ldap/ldapgroupdiff-$(date -d "1 day ago" '+%F')

rm -f /apps/sysadmin/ldap_csv/ldapdiff-$(date -d "1 day ago" '+%F')
rm -f /apps/sysadmin/ldap_csv/ldapuser-$(date -d "1 day ago" '+%F')
rm -f /apps/sysadmin/ldap_csv/ldapgroup-$(date -d "1 day ago" '+%F')
rm -f /apps/sysadmin/ldap_csv/ldapterm-$(date -d "1 day ago" '+%F')
rm -f /apps/sysadmin/ldap_csv/ldaptermdiff-$(date -d "1 day ago" '+%F')
rm -f /apps/sysadmin/ldap_csv/ldapgroupdiff-$(date -d "1 day ago" '+%F')

exit 0