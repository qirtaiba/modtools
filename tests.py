from dotenv import load_dotenv
load_dotenv()
import database_handler as db_handler

db_handler.test(4)