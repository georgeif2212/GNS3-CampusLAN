from dotenv import load_dotenv
import os


def dotenv():
    load_dotenv()


configVariables = {
    "SERVER": os.getenv("SERVER"),
    "DATABASE": os.getenv("DATABASE"),
    "USERNAME": os.getenv("USERNAME"),
    "PASSWORD": os.getenv("PASSWORD"),
    "DRIVER": os.getenv("DRIVER"),
}
