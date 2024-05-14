import pyodbc
import os

from config.config import dotenv

dotenv()

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
DRIVER = os.getenv("DRIVER")

connectionString = (
    f"DRIVER={DRIVER};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
)


# Establecer una conexión a SQL Server
conn = pyodbc.connect(connectionString)

cursor = conn.cursor()
