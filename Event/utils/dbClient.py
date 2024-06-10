from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
dbPassword = os.getenv('DB_PASSWORD')


def get_db_client():
    connection_string = f'''mongodb+srv://learningtechnigeria:{
        dbPassword}@airdropper.tjbu7cy.mongodb.net/?retryWrites=true&w=majority&appName=airdropper'''
    client = MongoClient(connection_string, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        print("Failed to connect to MongoDB. Please check your connection string and try again.")
    return client


client = get_db_client()
db = client['QREvent']
usersCollection = db["guests_info"]
verificationCollection = db["verification_state"]
