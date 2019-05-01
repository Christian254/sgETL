#!/bin/bash
# vars
backups_path="/var/lib/postgresql/cron/backups"
database="bd_gerencial"
current_date_time="`date +%Y%m%d%H%M%S`";
# dump
pg_dump $database > $backups_path/$current_date_time.sql;
# get size of dump
size="`wc -c $backups_path/$current_date_time.sql`";
# get oldest backup
first_backup="`ls $backups_path | sort -n | head -1`"
echo 'first backup '$first_backup
# get size of oldest backup
size_first="`wc -c $backups_path/$first_backup`"
echo 'size_first '$size_first
# get backups count
backups_count="`find  $backups_path/*.sql -type f | wc -l`"
echo 'cantidad de backups '$backups_count

# condition for remove if there is more than 4 backups
if [ $backups_count -ge 2 ] ; then
 echo 'mayor que 2'
# removing backup
 rm $backups_path/$first_backup
 first_text="`ls $backups_path | sort -n | head -1`"
# removing text of backup
 rm $backups_path/$first_text
# printing body explaining removed backup
 printf "\nArchivo borrado: "$first_backup >>  $backups_path/$current_date_time.txt
 printf "\nPeso: "$size_first >>  $backups_path/$current_date_time.txt
fi