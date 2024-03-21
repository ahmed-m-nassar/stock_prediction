import logging
import psycopg2
from psycopg2 import sql
import psycopg2.extras as extras 
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)

def connect_to_database(database_url):
    """
    Establishes a connection to the PostgreSQL database.

    Parameters:
    - database_url (str): The URL of the PostgreSQL database.

    Returns:
    - psycopg2 connection: The connection to the PostgreSQL database if successful, otherwise None.
    """
    try:
        conn = psycopg2.connect(database_url)
        logging.info("Connected to the database.")
        return conn
    except psycopg2.Error as e:
        logging.error("Error connecting to the database: %s", e)
        return None

def insert_df(conn, df, table):
    """
    Inserts data from a Pandas DataFrame into a PostgreSQL table using psycopg2's execute_values method.

    Parameters:
    - conn (psycopg2 connection): The connection to the PostgreSQL database.
    - df (DataFrame): The DataFrame containing the data to be inserted.
    - table (str): The name of the PostgreSQL table.

    Returns:
    - int: Returns 1 if an error occurs, otherwise returns None.
    """
    # Convert DataFrame to list of tuples
    tuples = [tuple(x) for x in df.to_numpy()]

    # Get column names as a comma-separated string
    cols = ','.join(list(df.columns))

    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)

    cursor = conn.cursor()
    try:
        # Execute the query using psycopg2's execute_values method
        extras.execute_values(cursor, query, tuples)
        conn.commit()
        logging.info("Data inserted into table %s.", table)
    except (Exception, psycopg2.DatabaseError) as error:
        # Rollback changes if an error occurs
        logging.error("Error inserting data into table %s: %s", table, error)
        conn.rollback()
        return 1
    finally:
        # Close the cursor
        cursor.close()
        logging.info("Cursor closed.")
        
def update_data(connection, table_name, set_clause, where_clause=None):
    """
    Updates existing records in a table.

    Parameters:
    - connection (psycopg2 connection): The connection to the PostgreSQL database.
    - table_name (str): The name of the table to be updated.
    - set_clause (str): The SET clause specifying the columns to be updated.
    - where_clause (str, optional): The WHERE clause specifying the condition for updating rows. Default is None.

    Returns:
    - None
    """
    try:
        cursor = connection.cursor()
        update_query = sql.SQL("UPDATE {} SET {}").format(
            sql.Identifier(table_name),
            set_clause
        )
        if where_clause:
            update_query += sql.SQL(" WHERE {}").format(where_clause)
        cursor.execute(update_query)
        connection.commit()
        logging.info("Data updated in table %s.", table_name)
    except psycopg2.Error as e:
        connection.rollback()
        logging.error("Error updating data in table %s: %s", table_name, e)
    finally:
        if cursor:
            cursor.close()
            logging.info("Cursor closed.")

def select_data(connection, table_name, columns="*", where_clause=None):
    cursor = None  # Define cursor variable and initialize it to None
    try:
        cursor = connection.cursor()
        # Initialize the query with SELECT statement
        select_query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(', ').join(map(sql.Identifier, columns)) if columns != "*" else sql.SQL('*'),
            sql.Identifier(table_name)
        )
        # If where_clause is provided, add WHERE clause to the query
        if where_clause:
            # Compose the WHERE clause as a SQL expression
            where_expr = sql.SQL(where_clause)
            select_query += sql.SQL(" WHERE {}").format(where_expr)
        cursor.execute(select_query)
        rows = cursor.fetchall()
        return rows
    except psycopg2.Error as e:
        return None
    finally:
        if cursor:
            cursor.close()

def close_connection(connection):
    """
    Closes the connection to the database.

    Parameters:
    - connection (psycopg2 connection): The connection to the PostgreSQL database.

    Returns:
    - None
    """
    try:
        connection.close()
        logging.info("Connection closed successfully.")
    except psycopg2.Error as e:
        logging.error("Error closing connection: %s", e)
        
def commit_changes(connection):
    """
    Commits the pending changes to the database.

    Parameters:
    - connection (psycopg2 connection): The connection to the PostgreSQL database.

    Returns:
    - None
    """
    try:
        connection.commit()
        logging.info("Changes committed successfully.")
    except psycopg2.Error as e:
        logging.error("Error committing changes: %s", e)
