import os
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

# DB CREDENTIALS (local settings)

#DATABASE_URI = f"postgresql://{DB_USERNAME}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
DATABASE_URI = os.environ.get("DATABASE_URL")
API_URL = os.environ.get("API_URL")

