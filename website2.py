#!/usr/bin/python
from twisted.web.template import Element
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web import static, resource
from twisted.web.template import XMLFile
from twisted.python.filepath import FilePath
import os
import MySQLdb as mdb
import json
import random

def connectDB():
	con = mdb.connect('localhost', 'root', 'cdc', 'Website')
	cur = con.cursor()
	return con, cur

def closeDB(con):
	con.commit()

def checkUsername(username):
	self.con = mdb.connect('localhost', 'root', 'cdc', 'Website')
	self.cur = self.con.cursor()
	query = ("SELECT * FROM USER WHERE username=?")
	self.cur.execute(query, username)			
	check = self.cur.fetchall()
	closeDB(con)
	return check

def Get_last_Purchase():
	con, cur = connectDB()
	number = get_number_of_purchases()	
	print number
	query = ("SELECT * FROM Purchases where Tracker=? ")
	cur.execute(query, int(number) - 1)
	Last_purchase = cur.fetchall()
	closeDB(con)
	print Last_purchase
	return Last_purchase

def get_number_of_purchases():
	con, cur = connectDB()
	query = ("SELECT Max(Tracker) FROM Purchases")
	cur.execute(query)
	number = cur.fetchall()
	closeDB(con)
	print number[0][0]
	print '&&&&&&'
	return number[0][0]
	
def getPurchaseID(data):
	con, cur = connectDB()
	query = ("SELECT * FROM Products where txid=? ")
	cur.execute(query, data)
	info = 	cur.fetchall()	
	closeDB(con)
	print info[0][4]
	print '***********'
	return info[0][4]
	
def GetPurchaseproof(data):
	con, cur = connectDB()
	query = ("SELECT * FROM Products where txid=?")
	cur.execute("""SELECT Proof_of_purchase FROM Products where txid=?""", (str(data[0])))
	proof = cur.fetchall()
	closeDB(con)
	print "-------IN GETPURCHASEPROOF---------"
	print proof
	# print infoJson	
	return proof
       
def getDinoInfo():
	con, cur = connectDB()
	query = ("SELECT * FROM Info")
	cur.execute(query)
	infoJson = 	cur.fetchall()	
	closeDB(con)
	# print infoJson	
	return json.dumps(infoJson)

def addInfo(data):
	# print data
	data = data.split("&")
	Headers = data[0].replace("Headers=", '')
	Text = data[1].replace("Text=", '')
	con, cur = connectDB()
	cur.execute("""INSERT INTO Info VALUES (?,?)""", (Headers, Text))
	closeDB(con)

def ProcessPurchase(data):
	print 'processing data';
	print data
	print type(data)      
	data = data.split("&")
	print data
	
	data[0] = data[0].replace('txid=', '')
	data[1] = data[1].replace('amount=', '')
	data[2] = data[2].replace('paid=', '')
	
	print data
	con, cur = connectDB()
	purchaseID = getPurchaseID(data[0]);
	print purchaseID
	print purchaseID
	print '((((('
	cur.execute("""INSERT INTO Purchases VALUES(?,?,?,?,?)""", (data[0], data[1], data[2], str(purchaseID), get_number_of_purchases() + 1))
	closeDB(con)
	updateTXID(data[0])
	
def StoreMenu():
	con, cur = connectDB()
	query = ("SELECT * FROM Products")
	cur.execute(query)
	infoJson = 	cur.fetchall()	
	closeDB(con)
	# print infoJson	
	return json.dumps(infoJson)
       
def updateTXID(txid):
	print txid
        try:   
	    con, cur = connectDB()
	    query = ("SELECT * FROM Products WHERE txid=?")
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
		print 'product info stayed the same'
		
class StartPageData(Element):
	loader = XMLFile(FilePath(os.path.join('html', 'login.html')))
	isLeaf = False
	allowedMethods = ('GET', 'POST', 'HEAD')
	
	def __init__(self, resource):
		self.resource = resource
				
class loginPage(resource.Resource):
	isLeaf = False
	allowedMethods = ('GET', 'POST', 'HEAD',)
	
	def __init__(self):
		print 'loginPage init'
		resource.Resource.__init__(self)
	
class FormPage(resource.Resource):
	isLeaf = False
	allowedMethods = ('GET', 'POST', 'HEAD')

	def __init__(self):
		resource.Resource.__init__(self)
        
	def render_GET(self, request):
		print request
		print request.getHeader('request')
		if request.getHeader('request') == 'info':
			return getDinoInfo()
		if request.getHeader('request') == 'Storeinfo':
			return StoreMenu()
		if request.getHeader('request') == 'receipt':
			print 'I am returning purchases'
			print request.args
			last_purchase = Get_last_Purchase();
			proof = GetPurchaseproof(last_purchase)
			print last_purchase	
			# last_purchase.append(proof)
			print last_purchase
	       	return json.dumps(last_purchase)
	
		if request.uri == '/':
			data = open(os.path.join('html', 'login.html'))
			return data.read()
	
	def renderDone(self, result, request):

# 	print "Done"
		request.write('<!DOCTYPE html>\n')
		request.write(result)
		request.finish()

	def getChild(self, name, request):
           	
		allowedMethods = ('GET', 'POST', 'HEAD')
		if request.method == 'POST':
			print 'Post is woriking'
		if request.method == 'POST' and name == 'receipt':
			print 'Inisde if state,etn '
			string = request.content.read();
			ProcessPurchase(string)
			request.method = 'GET'
			print name
	
		if 'png' in name or 'jpeg' in name:
			print 'returning file'
			return static.File(os.path.join('photos', name))
		if name == 'logout' :
			print 'Returning login page'
			return static.File(os.path.join('html', 'login.html'))
		elif name == "login.css":
			return static.File(os.path.join('css', 'login.css'))
		elif name == "buy.css":
			return static.File(os.path.join('css', 'buy.css'))
		elif name == "dino.css":
			return static.File(os.path.join('css', 'dino.css'))
		elif name == 'jquery.js':
			return static.File(os.path.join('js', 'jquery.js'))
		elif name == "buy.js":
			return static.File(os.path.join('js', 'buy.js'))
		elif name == "info.js":
			return static.File(os.path.join('js', 'info.js'))
		elif name == "receipt.js":
			return static.File(os.path.join('js', 'receipt.js'))		
		elif name == 'buy' or name == 'home':
			return static.File(os.path.join('html', 'buy.html'))
		elif name == 'info':
			return static.File(os.path.join('html', 'info.html'))
		elif name == 'receipt' or name == 'receipt.html':
			return static.File(os.path.join('html', 'receipt.html'))
		else:	
			return FormPage()

	def render_POST(self, request): 
		allowedMethods = ('GET', 'POST', 'HEAD')
		print 'This is where i am'  	
		if request.getHeader('request') == 'Newinfo':
			addInfo(request.content.read());
			print "Adding new info"
		if request.uri == '/login':
			if self.login(request):
				data = open(os.path.join('html', 'buy.html'), 'r')
				return data.read()
			else:
			    data = open(os.path.join('html', 'login.html'), 'r')
			    return data.read()

	def login(self, request):
		try:	
		    username = request.args['username'][0]
		    password = request.args['password'][0]
		    check = checkUsername(username)
		    if check is not None:
				if check[0] is not None:
					if check[1] is not None:
						if username == check[0] and password == check[1]:
							print '*******************************'
							print 'THE USER LOGINING IN:' + check[0][0]
							print '********************************'
							return True
				
				return False
		    else:
		        return False
   		except:
	   		return True


factory = Site(FormPage())
reactor.listenTCP(80, factory)

reactor.run()

