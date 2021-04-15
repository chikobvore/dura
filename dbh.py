
#this script handles the database connections
import pymongo

# client = pymongo.MongoClient('localhost', 27017)
# db = client['dura']

client = pymongo.MongoClient("mongodb+srv://dura:ei3TOR5FpldWCVZV@cluster0.ye35n.mongodb.net/dura?retryWrites=true&w=majority")
db = client.tau