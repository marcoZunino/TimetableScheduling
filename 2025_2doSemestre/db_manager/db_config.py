import psycopg2
import json


def get_database_connection(db_params=None, default=False) -> psycopg2.extensions.connection:
    """
    Establishes a database connection using the DATABASE_CONFIG dictionary.
    Returns a connection object if successful, otherwise raises an exception.
    """

    default_params = {
                'dbname': 'horarios',
                'user': 'postgres',
                'password': 'postgres',
                'host': 'localhost',
                'port': '5434'
            }
    
    if default:
        return get_database_connection(default_params)

    if not db_params:
        try:
            with open("db_manager\\db_params.json", "r") as file:
                db_params = json.load(file)
            
        except FileNotFoundError:
            db_params = default
            print("db_params.json file not found. Using default parameters.")


    try:
        # print("Connecting to the database...")
        connection = psycopg2.connect(**db_params)
        connection.set_client_encoding('UTF8')
        print(f"Database connection successful: {db_params["dbname"]} -> {db_params['user']}@{db_params['host']}:{db_params['port']}")
        
        return connection
    
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return get_database_connection(default_params)
    