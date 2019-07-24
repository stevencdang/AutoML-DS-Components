#!/bin/bash

docker_hostname=`hostname`

### MySQL
chown -R mysql:datashop /var/lib/mysql  ### /var/run/mysqld
sed -i 's/\[mysqld\]/[mysqld]\nsql_mode = "NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"/' /etc/mysql/mysql.conf.d/mysqld.cnf
### sed -i 's#/var/lib/mysql#/data/mysql#g' /etc/mysql/mysql.conf.d/mysqld.cnf

service mysql start

# DataShop and Tigris Databases
mysql -u root < /datashop/sql/create_databases.sql
mysql -u root < /datashop/sql/create_empty_auth_db.sql
mysql -u root adb_source < /datashop/sql/create/create_adb_10_x.sql
mysql -u root analysis_db < /datashop/sql/create/create_adb_10_x.sql

# Update DataShop/Tigris Authentication tables in database
cat << EOF | \
   mysql -u root
ALTER TABLE `workflow_component_instance` CHANGE COLUMN `state` `state` ENUM('new','running','running_dirty','error','do_not_run','completed', 'completed_warn') NULL DEFAULT 'new' COLLATE 'utf8_bin' AFTER `dirty_selection`;
ALTER TABLE `workflow_component_instance_persistence` CHANGE COLUMN `state` `state` ENUM('new','running','running_dirty','error','do_not_run','completed', 'completed_warn') NULL DEFAULT 'new' COLLATE 'utf8_bin' AFTER `dirty_selection`;
ALTER TABLE `workflow_component_instance` ADD COLUMN `warnings` LONGTEXT NULL COLLATE 'utf8_bin' AFTER `errors`;
ALTER TABLE `workflow_component_instance_persistence` ADD COLUMN `warnings` LONGTEXT NULL COLLATE 'utf8_bin' AFTER `errors`;
EOF

# Generate D3M Components
# cd /datashop/d3m_components/mk_docker
# ./setup_d3m_components.sh

mysql -u root analysis_db < /datashop/sql/workflow_component_local.sql
mysql -u root analysis_db < /datashop/sql/workflow_error_translation.sql
mysql -u root analysis_versions < /datashop/sql/create/create_versions_10_x.sql

# Generate conf script using environment variables'
if [ -f $D3MCONFIG ]; then
	rm $D3MCONFIG
fi
echo "[Data]" >> $D3MCONFIG
echo "dataset_root = $D3MINPUTDIR" >> $D3MCONFIG
echo "out_dir_root = $D3MOUTPUTDIR" >> $D3MCONFIG
echo "[TA2]" >> $D3MCONFIG
echo "ta2_url = $TA2ADDR" >> $D3MCONFIG
echo "ta2_name = $TA2NAME" >> $D3MCONFIG
echo "mode = D3M" >> $D3MCONFIG
chown jboss:datashop $D3MCONFIG
chmod 775 $D3MCONFIG

# Write Docker env variables to config file
dockerconfig="/datashop/workflow_components/D3M/docker_config.cfg"
echo "[frontend]" >> $dockerconfig
echo "HOST_URL=$FRONTEND_HOST_URL" >> $dockerconfig
echo "EXTERNAL_URL=$FRONTEND_URL" >> $dockerconfig
echo "[backend]" >> $dockerconfig
echo "HOST_URL=$BACKEND_HOST_URL" >> $dockerconfig
echo "EXTERNAL_URL=$BACKEND_URL" >> $dockerconfig
echo "[db]" >> $dockerconfig
echo "HOST_URL=$DB_HOST_URL" >> $dockerconfig
echo "[viz]" >> $dockerconfig
echo "HOST_URL=$VIZ_HOST_URL" >> $dockerconfig
echo "EXTERNAL_URL=$VIZ_URL" >> $dockerconfig
chown jboss:datashop $dockerconfig
chmod 775 $dockerconfig

chgrp -R datashop $D3MOUTPUTDIR
chmod g+w -R $D3MOUTPUTDIR


# MoocDB "core" and "clean" databases
cd /datashop/sql/create/MOOCdb
mysql -u root analysis_versions < /datashop/sql/create/MOOCdb/create_restore_MOOCdb.sql

# Update DataShop/Tigris Authentication tables in database
cat << EOF | \
  mysql -u root
REPLACE INTO \`authentication\`.\`auth_domain\` (\`domain_name\`, \`authenticator\`, \`created\`, \`last_modified\`, \`enabled\`) VALUES ('external', 'com.beginmind.login.PasswordAuthenticator', '2006-06-12 12:38:16', '2006-06-12 12:38:16', 1);
REPLACE INTO \`authentication\`.\`auth_domain\` (\`domain_name\`, \`authenticator\`, \`created\`, \`last_modified\`, \`enabled\`) VALUES ('guest', 'com.beginmind.login.PasswordAuthenticator', '2006-06-14 10:16:19', '2006-06-14 10:16:19', 1);
REPLACE INTO \`authentication\`.\`auth_domain\` (\`domain_name\`, \`authenticator\`, \`created\`, \`last_modified\`, \`enabled\`) VALUES ('webiso', 'com.beginmind.login.TrustedAuthenticator', '2006-06-12 12:38:09', '2006-06-12 12:38:09', 1);
INSERT INTO \`analysis_db\`.\`user\` (user_id, first_name, last_name, email, institution, admin_flag, creation_time, login_type, login_id, user_alias) VALUES ('%', NULL ,NULL,NULL,NULL,0,'2015-08-13 11:38:04',NULL,NULL, 'public'),('ctipper','C','Tipper','ctipper@cs.cmu.edu','',1,'2015-08-19 11:03:13',NULL,NULL, 'Cindy'),('datashop','DataShop','Manager','datashop-vm@lists.andrew.cmu.edu','Carnegie Mellon University',1,'2015-08-18 13:59:53',NULL,NULL, 'DataShop Manager'),('mkomisin','Mike','Komisin','mkomisin@cmu.edu','Carnegie Mellon University',1,'2015-08-18 14:04:10',NULL,NULL, 'Mike'),('system',NULL,NULL,NULL,NULL,0,'2015-08-13 11:38:04',NULL,NULL, 'DataShop'),('webservice_request',NULL,NULL,'datashop-help@lists.andrew.cmu.edu',NULL,0,'2015-08-19 14:52:03',NULL,NULL, 'Remote DataShop');
INSERT INTO \`authentication\`.\`system_user\` VALUES ('41f7a7957f00000101b9d13350e59254','external','datashop','2015-08-18 13:59:53','2015-08-18 13:59:53',1),('41fb935c7f000001019c4e49394706b3','external','mkomisin','2015-08-18 14:04:10','2015-08-18 14:04:10',1),('467c456a7f00000100b6391c18dd914d','external','ctipper','2015-08-19 11:03:13','2015-08-19 11:03:13',1);
INSERT INTO \`authentication\`.\`password\` VALUES ('41f7a8bc7f000001001a022ef2d316b8','41f7a7957f00000101b9d13350e59254','4d89e16ad93361c185159fafb4141b8c','2015-08-18 13:59:53','2015-09-09 15:01:59'),('41fb936c7f00000100b1bad06a1784b9','41fb935c7f000001019c4e49394706b3','519a421cb66a49e5d8fdb17fd4ad00c7','2015-08-18 14:04:10','2015-08-18 14:04:10'),('467c45867f00000100f29318e8637f0a','467c456a7f00000100b6391c18dd914d','0300df433ca5fbf22de2c11c8e23927e','2015-08-19 11:03:13','2015-08-19 11:03:13');

flush tables ;

EOF


# Create DataShop/Jboss login/config and mysql password configuration (relies on variables.sh)
/datashop/tools/vm/generate_login-config.sh docker

cd /datashop/deploy
ant deploySps 2> 1

### Apache

cat >> /etc/security/limits.conf << EOF
*               soft    nofile          8192
*               hard    nofile          8192

EOF

# Start a python server to try to keep network interface alive
python -m SimpleHTTPServer 8000 &

# Remote ipv6 lines from /etc/hosts
sudo printf ",g/ip6/d\nw\nq\n" | sudo ed /etc/hosts

service apache2 start

service ssh start

sleep 5


### JBoss

chown -R jboss:datashop /opt/jboss-4.2.0.GA/
echo "127.0.0.1 `hostname`" >> /etc/hosts

service jboss start
### Keep docker container running

echo "Waiting for jboss to start." ;
while [ ! -f /opt/jboss/server/oli/log/server.log ]; do sleep 4; done
echo "JBoss started."

touch /datashop/docker.log
tail -f /datashop/docker.log /opt/jboss/server/oli/log/server.log

# Start  the testing server as a service
./datashop/d3m_components/appserver/backend/run_server.sh &
