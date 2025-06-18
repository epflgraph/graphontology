import subprocess
from graphontology.utils.config import config


def import_mysql_from_dump(dump_filename):
    """
    Imports a MySQL dump file into a database using the mysql command-line tool.

    Parameters:
        dump_filename (str): Path to the MySQL dump file (.sql).
    """
    # Set your database credentials and target database name here
    db_user = config['database']['user']
    db_password = config['database']['password']
    db_host = config['database']['host']
    db_port = config['database']['port']
    db_name = 'graph_ontology'
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
