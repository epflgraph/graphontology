import subprocess

from db_cache_manager.db import DB

from graphontology.utils.config import config


def import_mysql_from_dump(dump_filename, db_name='graph_ontology'):
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

    try:
        # Construct the command to run
        command = [
            "mysql",
            f"--user={db_user}",
            f"--password={db_password}",
            f"--host={db_host}",
            f"--port={db_port}",
            db_name
        ]

        print(f'Starting to load dump into MySQL schema `{db_name}`')
        # Open the dump file and pass it to the mysql command
        with open(dump_filename, "rb") as dump_file:
            subprocess.run(command, stdin=dump_file, check=True)

        print(f"Successfully imported dump file into database '{db_name}'.")

    except subprocess.CalledProcessError as e:
        print(f"Error during MySQL import: {e}")
    except FileNotFoundError:
        print(f"Dump file '{dump_filename}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def verify_table_existence(table_name, db_name='graph_ontology'):
    db_manager = DB(config['database'])
    count = db_manager.execute_query(
        "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = %s) AND (TABLE_NAME = %s)",
        values=(db_name, table_name)
    )
    if count > 0:
        return True
    return False
