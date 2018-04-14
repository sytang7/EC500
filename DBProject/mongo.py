from pymongo import MongoClient, ASCENDING
from requests import get
from os.path import isfile

def getfile(url):
	return get(url).json()

def upload(collection,data):
	return collection.insert_many(data)

def read(collection,item_index,query={}):
	result = serach(collection,query)[item_index]
	print(result)
	return result

def getCollection(client,db,collection):
	return client.db.collection

def update(collection,item_collection,item_index,update_items):
	for item in update_items:
		collection.update_one({'_id':item_collection[item_index]['_id']}, {"$set": update_items}, upsert=True)	

def serach(collection,query={}):
	return collection.find(query)

def importfromurl(DBaddress,db,collection,url):
	data = getfile(url)
	MongoClient(mongodb).db.collection.insert_many(data)

if __name__ == "__main__":
	url = "https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json"
	mongodb  = "mongodb://localhost:27017"

	print("Downloading Json Fie...")
	file = getfile(url)
	print("Connecting to Mongo...")
	cli = MongoClient(mongodb)
	db = "fun"
	collec = "airports"
	collection = getCollection(cli,db,collec)
	print("Uploading to MongoDB...")
	upload(collection,file)
	print("Find name: Logan International Airport...")
	items = serach(collection,{"name": "Logan International Airport"})
	print("read Logan Airport data: ")
	if items.count()>0:
		print(items[0])
	print("how many is in the item "+str(items.count()))
	print("Update Logan International Airport email...")
	updateitem = {"email": "sytang7@bu.edu"}
	if items.count()>0:
		update(collection,items,0,updateitem)
	print("Reread Logan International Airport data:")
	read(collection,0,{"name": "Logan International Airport"})



