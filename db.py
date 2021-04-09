
import pyrebase
import logging
import random
import KEYS

config = {
  "apiKey": KEYS.apiKeyFirebase,
  "authDomain": KEYS.authDomain,
  "databaseURL": KEYS.databaseURL,
  "storageBucket": KEYS.storageBucket,
  "serviceAccount": KEYS.pathToServiceJson
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# servers
db.child("Server").push(714884228021616732) # let'splayAGame
db.child("Server").push(639818527058165770) # Limbo
db.child("Server").push(733901926390825021) # Secret

# channel
db.child("channels").child(714884228021616732).push(778167058537775112) # let'splayAGame
db.child("channels").child(639818527058165770).push(755990356654424124) # Limbo 
db.child("channels").child(733901926390825021).push(799485382944227329) # Secret

# admins
db.child("Admins").child(714884228021616732).push(506018589904470047) # let'splayAGame
db.child("Admins").child(639818527058165770).push(506018589904470047) # Limbo
db.child("Admins").child(733901926390825021).push(506018589904470047) # Secret

#retrive data
#servers = db.child("Servers")
#serverInfo = servers.get()
#print(serverInfo.val())

