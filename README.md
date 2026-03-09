# installed postgresQL(psql Ubuntu 18.2-1.pgdg24.04+1) on myPC OS Ubuntu 24.04.4 LTS
# entered in to postgresql by Command sudo -i -u postgres followed with password and then entering psql
# \l to view the databases and \q to quit
# use the command "create database assignmentdb;" to create assignmentdb database
#use the command "\c assignmentdb" to switch to assignmentdb database
#use command "drop database name_database" to delete the name_database
#created two tables named student with field name, rollnumber, dob and teacher with field name department and id
#various operations on table (refer attachment - table-operation 1 & 2)
#created virtual environment
#installed psycopg2 tool to connect database with python
#started postgresql server by command "sudo systemctl start postgresql"
#checked server status by command "sudo systemctl status postgresql"
#checked connection info by command "\conninfo" after entering to postgres
#exited postgres and entered the default user
#set password for database for default admin by command "sudo -u postgres psql"
#created a pythonfile named connecdb.py
#tested the connection successfully - the screenshot is attached as psycopg2_connection_test
# a function named inser_data programmed to view all the tables in the connected database
# user has been given a choice to select table name to which data has to be inserted
# After entering the data confirmation is displayed as the data is inserted successfully.
# After confirmation, user has been given a choice to continue the entry or exit by typing y/n
# The screen shots are enclosed herewith as Data_entry
# rest all the table and content operations have been executed successfully.
#submitted, please.
