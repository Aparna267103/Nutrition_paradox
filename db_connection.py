from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://postgres:Aswin789vishnu@localhost:5432/postgres"
)

print("Connected!")