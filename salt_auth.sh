#!/bin/bash
USER1=$PAM_USER
USER2='root'
CHECKHOMEDIR=`ls /home | grep -o ^$USER1`
KEYEXISTS=`ls /home/$USER1/.ssh/ | grep -o id_rsa`
SALTSERVER='saltstack-syndic-east-1.itd.someorg.com'
SALTPORTS='4505-4506'

checkmaster ()
{
  nc -z $SALTSERVER $SALTPORTS 1>/dev/null 2>&1; RESULT=$?;

   if [ $RESULT -eq 0 ]; then
       login
   else
       exit 0
   fi
}


login ()
{
  if [ "$CHECKHOMEDIR" == "$USER1" ] && [ "$KEYEXISTS" == "id_rsa" ]; then
     echo "`date "+%b %d %T"` Welcome $USER1! With homedir $CHECKHOMEDIR and key $KEYEXISTS"

  elif [[ "$USER1" == "$USER2" ]]; then
	 echo "`date "+%b %d %T"` $USER2 user.  No key needed."

  elif [ "$KEYEXISTS" != "id_rsa" ] && [ "$USER1" != "$USER2" ]; then
     /usr/bin/salt-call event.fire_master '{"user_id":'$USER1'}' "generate_bastion_user" --skip-grains > /dev/null 2>&1
	 echo "`date "+%b %d %T"` Event fired for $USER1 by salt_auth.sh" 
	 exit 0
  else
	 echo "Nothing to do"
  fi

  exec 2>> /var/log/salt/salt-event-fire 2>&1
}

exec 1>> /var/log/salt/salt-event-fire
 checkmaster
exec 1>> /var/log/salt/salt-event-fire 2>&1

exit 0
