#!/usr/bin/python
from twisted.web.template import Element
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web import static, resource
from twisted.web.template import XMLFile
from twisted.python.filepath import FilePath
import os, sys
import MySQLdb as mdb
import json
import random
import logging
import datetime
import hashlib, uuid
import re
import ConfigParser

SQLINJECTION = re.compile(r'([^a-zA-Z0-9_.])')
CONFIG_LOC = '/home/twisted/'
SOURCE_LOC = '/var/www/dinoWebApp/'
#CONFIG_LOC = './'
#SOURCE_LOC = './'

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

def Get_last_Purchase():
	try:
		con, cur = connectDB()
	except:
		raise
	number = get_number_of_purchases()
	logging.debug("Number of purchases: %s", str(number))
	query = ("SELECT * FROM Purchases where Tracker=%s ")
	cur.execute(query, int(number) - 1)
	Last_purchase = cur.fetchall()
	logging.debug("Last Purchase: %s", str(Last_purchase))
	closeDB(con)
	return Last_purchase

def get_number_of_purchases():
	con, cur = connectDB()
	query = ("SELECT Max(Tracker) FROM Purchases")
	cur.execute(query)
	number = cur.fetchall()
	logging.debug("Number of purchases: %s", str(number[0][0]))
	closeDB(con)
	return number[0][0]

def getPurchaseID(data):
	con, cur = connectDB()
	query = ("SELECT * FROM Products where txid=%s ")
	cur.execute(query, data)
	info = 	cur.fetchall()
	logging.debug("PurchaseID: %s", str(info[0][4]))
	closeDB(con)
	return info[0][4]

def GetPurchaseproof(data):
	logging.debug("GetPurchaseproof Data parameter: %s", str(data))
	con, cur = connectDB()
	# WHY is this query here when there is an execute line below??
	#query = ("SELECT * FROM Products where txid=%s")
	cur.execute("SELECT Proof_of_purchase FROM Products where txid=%s", (str(data[0])))
	proof =	cur.fetchall()
	logging.debug("Purchase Proof: %s", str(proof))
	closeDB(con)
	return proof

def getDinoInfo():
	con, cur = connectDB()
	query = ("SELECT * FROM Info")
	cur.execute(query)
	infoJson = 	cur.fetchall()
	logging.debug("DinoInfo: %s", str(infoJson))
	closeDB(con)
	return json.dumps(infoJson)

def addInfo(data):
	# print data
	logging.debug("addInfo Data parameter: %s", str(data))
	data = data.split("&")
	Headers = data[0].replace("Headers=", '')
	Text = data[1].replace("Text=", '')
	con, cur = connectDB()
	cur.execute("INSERT INTO Info VALUES (%s,%s)", (Headers, Text))
	closeDB(con)

def ProcessPurchase(data):
	logging.debug("ProcessPurchase processing..")
	logging.debug("Data: %s", str(data))
	logging.debug("Data Type: %s", type(data))
	data = data.split("&")
	logging.debug("Data after split: %s", str(data))

	data[0] = data[0].replace('txid=', '')
	data[1] = data[1].replace('amount=', '')
	data[2] = data[2].replace('paid=', '')

	logging.debug("Data after replacements: %s", str(data))
	con, cur = connectDB()
	purchaseID = getPurchaseID(data[0]);
	logging.debug("purchaseID: %s", str(purchaseID))
	numberOfPurchases = get_number_of_purchases()
	if numberOfPurchases is None:
		numberOfPurchases = 0
	cur.execute("INSERT INTO Purchases VALUES(%s,%s,%s,%s,%s);", (data[0], data[1], data[2], str(purchaseID), numberOfPurchases + 1))
	closeDB(con)
	updateTXID(data[0])
	logging.debug("ProcessPurchase processing complete.")

def StoreMenu():
	try:
		con, cur = connectDB()
		query = ("SELECT Text, Price, Img, Quantity, txid FROM Products")
		cur.execute(query)
		logging.debug('After query in StoreMenu')
		infoJson = 	cur.fetchall()
		#for item in infoJson:
		#	logging.debug('item: %s', arr(item)[5])
		#logging.debug("infoJson: %s", infoJson)
	except Exception as error:
		logging.warn('Error:' + str(error))
		logging.warn('Error parameters: ' + str(error.args))

	closeDB(con)
	return json.dumps(infoJson)

def updateTXID(txid):
	logging.debug("updateTXID parameter: %s", str(txid))
	try:
	 	con, cur = connectDB()
		query = ("SELECT * FROM Products WHERE txid=%s")
		cur.execute(query, int(txid))
		check1 = cur.fetchall()
		closeDB(con)
		# print check1
		# print check1[0][3]
		# quanity=int(check1[0][3])-1
		# newtxid=random.randrange(0,100000000)
		# cur.execute("""Insert into Products VALUES(%s,%s,%s,%s,%s)""",(check1[0][0],check1[0][1],check1[0][2],quanity,newtxid))
		# con.commit()
		# print check
	except:
		logging.info("Product info stayed the same")

def getOrderCompletion(orderID):
	logging.debug("Getting order completion details from DB.")
	logging.debug("orderID: %s", orderID)
	try:
		con, cur = connectDB()
		query = ("SELECT * FROM orders WHERE orderID='%s';", orderID)
		cur.execute(query)
		check = cur.fetchall()
		closeDB(con)
	except:
		logging.debug("getOrderCompletion failed.")
	if check:
		logging.debug("check: %s", check)
		return check

def updateViewed(orderID):
	logging.debug("Updating viewed column to 1.")
	logging.debug("OrderID: %s", orderID)
	try:
		con, cur = connectDB()
		query = ("UPDATE orders SET viewed=1 WHERE orderID='%s';", orderID)
		cur.execute(query)
		check = cur.fetchall()
		closeDB(con)
	except:
		logging.debug("updateViewed failed.")

class StartPageData(Element):
	loader = XMLFile(FilePath(os.path.join(SOURCE_LOC + 'html', 'login.html')))
	isLeaf = False
	allowedMethods = ('GET', 'POST', 'HEAD')
	def __init__(self, resource):
		self.resource = resource

class loginPage(resource.Resource):
	isLeaf = False
	allowedMethods = ('GET', 'POST', 'HEAD',)
	def __init__(self):
		logging.debug("loginPage init")
		resource.Resource.__init__(self)

class FormPage(resource.Resource):
	isLeaf = False
	allowedMethods = ('GET', 'POST', 'HEAD')
	def __init__(self):
		resource.Resource.__init__(self)
	def render_GET(self, request):
		logging.debug("FormPage Request Arguments: %s", str(request.args))
		logging.debug("FormPage request: %s", str(request))
		logging.debug("RequestHeader: %s", str(request.getHeader('request')))
		if request.getHeader('request') == 'info':
			return getDinoInfo()
		if request.getHeader('request') == 'Storeinfo':
			return StoreMenu()
		if request.getHeader('request') == 'receipt':
			logging.debug("I am returning purchases")
			logging.debug("RequestAllHeaders: %s", str(request.getAllHeaders()))

			last_purchase = Get_last_Purchase();
			proof = GetPurchaseproof(last_purchase)
			orderID = request.getHeader('orderID')
			logging.debug('OrderID: %s', orderID)
			completedOrder = getOrderCompletion(orderID)

			logging.debug("FormPage last_purchase (before): %s", str(last_purchase))
			logging.debug("FormPage completedOrder: %s", str(completedOrder))

			if completedOrder:
				if completedOrder[0][2] == 0:
					updateViewed(orderID)
					return json.dumps(last_purchase)
				else:
					logging.debug("viewed was not 0.")

			last_purchase = None
			logging.debug("FormPage last_purchase (after): %s", str(last_purchase))

			# last_purchase.append(proof)
			# print last_purchase

			return json.dumps(last_purchase)

		if request.uri == '/':
			 data = open(os.path.join(SOURCE_LOC + 'html', 'login.html'))
			 return data.read()

	def renderDone(self, result, request):

	# 	print "Done"
		request.write('<!DOCTYPE html>\n')
		request.write(result)
		request.finish()

	def getChild(self, name, request):

		allowedMethods = ('GET', 'POST', 'HEAD')
		if request.method == 'POST':
			logging.debug('Post is working')
		if request.method == 'POST' and name == 'receipt':
			logging.debug('Inisde if statement')
			string = request.content.read();
			ProcessPurchase(string)
			request.method = 'GET'
			logging.debug("getChild name: %s", str(name))

		if 'png' in name or 'jpeg' in name:
			logging.debug('returning file')
			return static.File(os.path.join(SOURCE_LOC + 'photos', name))
		if name == 'logout' :
			logging.debug('Returning login page')
			return static.File(os.path.join(SOURCE_LOC + 'html', 'login.html'))
		elif name == "login.css":
			return static.File(os.path.join(SOURCE_LOC + 'css', 'login.css'))
		elif name == "buy.css":
			return static.File(os.path.join(SOURCE_LOC + 'css', 'buy.css'))
		elif name == "dino.css":
			return static.File(os.path.join(SOURCE_LOC + 'css', 'dino.css'))
		elif name == 'jquery.js':
			return static.File(os.path.join(SOURCE_LOC + 'js', 'jquery.js'))
		elif name == "buy.js":
			return static.File(os.path.join(SOURCE_LOC + 'js', 'buy.js'))
		elif name == "info.js":
			return static.File(os.path.join(SOURCE_LOC + 'js', 'info.js'))
		elif name == "receipt.js":
			return static.File(os.path.join(SOURCE_LOC + 'js', 'receipt.js'))
		elif name == 'buy' or name == 'home':
			return static.File(os.path.join(SOURCE_LOC + 'html', 'buy.html'))
		elif name == 'info':
			return static.File(os.path.join(SOURCE_LOC + 'html', 'info.html'))
	   	elif name == 'receipt' or name == 'receipt.html':
			return static.File(os.path.join(SOURCE_LOC + 'html', 'receipt.html'))
		else:
			return FormPage()

	def render_POST(self, request):
		allowedMethods = ('GET', 'POST', 'HEAD')
		logging.debug("render_POST beginning.")
		if request.getHeader('request') == 'Newinfo':
 			addInfo(request.content.read());
			logging.debug("Adding new info")
		if request.uri == '/login':
				if self.login(request):
						data = open(os.path.join(SOURCE_LOC + 'html', 'buy.html'), 'r')
						logging.debug("render_POST end with login.")
						return data.read()
				else:

						data = open(os.path.join(SOURCE_LOC + 'html', 'login.html'), 'r')
						logging.debug("render_POST end with failed login.")
						return data.read()

	def login(self, request):
		logging.debug("login beginning.")
		try:
			username = request.args['username'][0]
			if SQLINJECTION.search(username):
				logging.debug('SQL Injection found!')
				return False
			password = request.args['password'][0]

			config = ConfigParser.ConfigParser()
			config.read(CONFIG_LOC + '.eula.txt')
			UUID_SALT = config.get('salt', 'uuid_salt')
			salt = UUID_SALT
			hashedPassword = hashlib.sha512((password.encode('UTF-8')) + salt).hexdigest()
			con, cur = connectDB()
			logging.debug("username: %s", username)
			query = ("SELECT * FROM Website.USER WHERE username=%s")
			logging.debug("query: %s", str(query))
			exe = cur.execute(query, str(username))
			logging.debug("execute return: %s", str(exe))
			if exe == 0:
				return False
			check = cur.fetchall()
			closeDB(con)

			if check is not None:
				if check[0][1] == hashedPassword:
					logging.debug('*******************************')
					logging.debug('THE USER LOGINING IN:' + check[0][0])
					logging.debug('*******************************')
					return True
				else:
					logging.debug('Password did not match.')
					return False
			else:
				return False
		except Exception as inst:
			logging.warn('Error:' + str(inst))
			logging.warn('Error parameters: ' + str(inst.args))
			logging.debug("login failed.")
			return False

FORMAT = "%(asctime)-15s %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, filename=(CONFIG_LOC + 'dinoWebApp.log'), format=FORMAT)
logging.info('Server starting...')
factory = Site(FormPage())
reactor.listenTCP(8080, factory)

reactor.run()
