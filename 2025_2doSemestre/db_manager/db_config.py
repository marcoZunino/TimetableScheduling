import psycopg2


db_params = {
    'dbname': 'horarios',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5434'
}

def get_database_connection():
    """
    Establishes a database connection using the DATABASE_CONFIG dictionary.
    Returns a connection object if successful, otherwise raises an exception.
    """
    connection = None

    try:
        print("Connecting to the database...")
        connection = psycopg2.connect(**db_params)
        connection.set_client_encoding('UTF8')
        print("Database connection successful.")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
    