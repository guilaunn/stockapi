from sqlalchemy import create_engine
from app.models import Base
from app.database import DATABASE_URL

# Create the engine using the DATABASE_URL
engine = create_engine(DATABASE_URL)

def setup_database():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
