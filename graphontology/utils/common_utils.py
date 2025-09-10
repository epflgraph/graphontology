from sqlalchemy import create_engine, text
import subprocess
from graphontology.utils.config import config

# Initialize DB connection
db_cfg = config["database"]
engine = create_engine(
    f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['schema']}"
)

def import_mysql_from_dump(dump_filename, verbose=False):
    """
    Imports a MySQL dump file into a database using the mysql command-line tool.

    Parameters:
        dump_filename (str): Path to the MySQL dump file (.sql).
        db_name (str): Name of schema, 'graph_ontology' by default
    """
    # Set your database credentials and target database name here
    db_user = config['database']['user']
    db_password = config['database']['password']
    db_host = config['database']['host']
    db_port = config['database']['port']
    if db_host == 'localhost':
        db_host = '127.0.0.1'
    db_schema = config['database']['schema']

    try:
        # Construct the command to run
        command = [
            "mysql",
            f"--user={db_user}",
            f"--password={db_password}",
            f"--host={db_host}",
            f"--port={db_port}",
            f"--database={db_schema}"
        ]

        if verbose:
            print(f'Starting to load dump into MySQL schema `{db_schema}`')

        # Open the dump file and pass it to the mysql command
        with open(dump_filename, "rb") as dump_file:
            subprocess.run(command, stdin=dump_file, check=True)

        if verbose:
            print(f"Successfully imported dump file into database '{db_schema}'.")

    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"Error during MySQL import: {e}")
    except FileNotFoundError:
        if verbose:
            print(f"Dump file '{dump_filename}' not found.")
    except Exception as e:
        if verbose:
            print(f"Unexpected error: {e}")


def verify_table_existence(table_name):

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{db_cfg['schema']}') AND (TABLE_NAME = '{table_name}')"))
        count = result.fetchall()[0][0]

    if count > 0:
        return True
    return False
