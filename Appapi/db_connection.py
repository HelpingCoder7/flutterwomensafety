from pymongo.mongo_client import MongoClient
import certifi



uri = "mongodb+srv://safetyapp:li7CIGUIiBZCJAvT@cluster0.nu2zdsi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  

ca = certifi.where()
client = MongoClient(uri )

db = client['logincollection']
print("connection done ")

