#!/usr/bin/python
import MySQLdb as mdb
import ConfigParser
import logging
import re
import hashlib, uuid

CONFIG_LOC = '/home/twisted/'
#CONFIG_LOC = './'
SQLINJECTION = re.compile(r'([^a-zA-Z0-9.])')
FORMAT = "%(asctime)-15s %(levelname)s - %(message)s"
logging.basicConfig(filename=CONFIG_LOC + 'insertUser.log', level=logging.DEBUG, format=FORMAT)

def connectDB():
	configSection = 'MySQL'
	host = None
	username = None
	password = None
	database = None
	try:
		config = ConfigParser.ConfigParser()
		config.read(CONFIG_LOC + '.eula.txt')
		host = config.get(configSection, 'host')
		username = config.get(configSection, 'username')
		password = config.get(configSection, 'password')
		database = config.get(configSection, 'database')
	except:
		logging.warn("Error reading configuration file.")
		return None, None

	try:
		con = mdb.connect(host, username, password, database)
		cur = con.cursor()
		logging.debug("Conected to database.")
		return con, cur
	except:
		logging.warn("Connection to database failed.")
		return None, None

def closeDB(con):
	con.commit()

def insertUser(username, password):
	if SQLINJECTION.search(username):
		logging.debug('SQL Injection found!')
		return False

	config = ConfigParser.ConfigParser()
	config.read(CONFIG_LOC + 'server.cfg')
	UUID_SALT = config.get('salt', 'uuid_salt')
	salt = UUID_SALT
	hashedPassword = hashlib.sha512((password.encode('UTF-8')) + salt).hexdigest()

	con, cur = connectDB()
	query = ("INSERT INTO USER VALUES('%s', '%s');", (username, hashedPassword))
	logging.debug(query)
	exe = cur.execute(query)
	if exe == 1:
		print 'Success!'
	else:
		print 'Failed.'
	closeDB(con)

def main():
	print 'start'
	username = raw_input('Enter the new username: ')
	print username
	password = raw_input('Enter the new password: ')
	insertUser(username, password)

if  __name__ =='__main__':
	main()
