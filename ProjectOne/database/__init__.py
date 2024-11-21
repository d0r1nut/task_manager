from pymongo import MongoClient
from .db import Database
import app_config as config

database = Database(config.CONST_DATABASE, config.CONST_MONGO_URL)
database.connect()