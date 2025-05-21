from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

connection_string = "mssql+pyodbc://@MYDCL-47\\SQLEXPRESS/HMS_Project?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(connection_string, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#For Testing
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful.")
    except Exception as e:
        print("❌ Database connection failed:", e)
