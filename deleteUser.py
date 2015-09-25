#!/usr/bin/python
import MySQLdb as mdb
import ConfigParser
import logging
import re


SQLINJECTION = re.compile(r'([^a-zA-Z0-9.])')
FORMAT = "%(asctime)-15s %(levelname)s - %(message)s"
logging.basicConfig(filename='deleteUser.log', level=logging.DEBUG, format=FORMAT)

def connectDB():
	configSection = 'MySQL'
	host = None
	username = None
	password = None
	database = None
	try:
		config = ConfigParser.ConfigParser()
		config.read('server.cfg')
		host = config.get(configSection, 'host')
		username = config.get(configSection, 'username')
		password = config.get(configSection, 'password')
		database = config.get(configSection, 'database')
	except:
		logging.warn("Error reading configuration file.")
		logging.debug('%s %s %s %s' % (host, username, password, database))
		return None, None

	try:
		con = mdb.connect(host, username, password, database)
		cur = con.cursor()
		logging.debug("Conected to database.")
		return con, cur
	except:
		logging.warn("Connection to database failed.")
		logging.debug('%s %s %s %s' % (host, username, password, database))
		return None, None

def closeDB(con):
	con.commit()

def deleteUser(username):
	if SQLINJECTION.search(username):
		logging.debug('SQL Injection found!')
		return False
	con, cur = connectDB()
	query = "DELETE FROM USER WHERE username='%s';" % (username)
	logging.debug(query)
	exe = cur.execute(query)
	if exe >= 1:
		print 'Success!'
	else:
		print 'Failed.'
	closeDB(con)

def main():
	print 'start'
	username = raw_input('Enter the username you wish to delete: ')
	deleteUser(username)

if  __name__ =='__main__':
	main()
