
#this script handles the database connections
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['dura']
# client = pymongo.MongoClient("mongodb+srv://ladsroot:ladsroot@lads.f97uh.mongodb.net/tau?retryWrites=true&w=majority")
# db = client.tau