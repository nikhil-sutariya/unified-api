from google.cloud import firestore
db = firestore.Client.from_service_account_json('service_account.json')

# Register models/collections here
Projects = db.collection("projects")
Users = db.collection("users")
