import psycopg2
import json


db_params = {
    'dbname': 'horarios',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5434'
}

try:
    with open("db_manager\\db_params.json", "r") as file:
        db_params = json.load(file)
except FileNotFoundError:
    print("db_params.json file not found. Using default parameters.")


def get_database_connection() -> psycopg2.extensions.connection:
    """
    Establishes a database connection using the DATABASE_CONFIG dictionary.
    Returns a connection object if successful, otherwise raises an exception.
    """
    connection = None

    try:
        # print("Connecting to the database...")
        connection = psycopg2.connect(**db_params)
        connection.set_client_encoding('UTF8')
        # print("Database connection successful.")
        
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
    