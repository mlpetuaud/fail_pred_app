import os
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

# DB CREDENTIALS (local settings)
#DB_PASSWORD= os.environ.get("DB_PASSWORD")
DB_NAME=os.environ.get("DB_NAME")
DB_USERNAME=os.environ.get("DB_USERNAME")
DB_ADDRESS=os.environ.get("DB_ADDRESS")
DB_PORT=os.environ.get("DB_PORT")

# Scheme: "postgresql://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = f"postgresql://{DB_USERNAME}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
print(DATABASE_URI)
