import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

LOG_FILE = "etl_project_log.txt"

def log_progress(message):
    """Logs the mentioned message at a given stage of the code execution to a log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def extract(url, table_attribs):
    """Extracts the required information from the website and saves it to a dataframe."""
    log_progress("Starting data extraction")
    response = requests.get(url)
    if response.status_code != 200:
        log_progress("Failed to fetch the webpage")
        raise Exception("Failed to fetch the webpage")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", table_attribs)
    rows = table.find_all("tr")
    
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) > 1:
            country = cols[1].text.strip()
            gdp_text = cols[2].text.strip().replace(",", "").split("[")[0]
            try:
                gdp = float(gdp_text)
                data.append({"Country": country, "GDP_USD_Millions": gdp})
            except ValueError:
                continue

    log_progress("Data extraction completed successfully")
    return pd.DataFrame(data)

def transform(df):
    """Converts GDP information to float and transforms it from USD (Millions) to USD (Billions)."""
    log_progress("Starting data transformation")
    df["GDP_USD_Billions"] = round(df["GDP_USD_Millions"] / 1000, 2)
    df = df.drop(columns=["GDP_USD_Millions"])
    log_progress("Data transformation completed successfully")
    return df

def load_to_csv(df, csv_path):
    """Saves the final dataframe as a CSV file."""
    log_progress(f"Saving data to CSV file at {csv_path}")
    df.to_csv(csv_path, index=False)
    log_progress("Data successfully saved to CSV")

def load_to_db(df, sql_connection, table_name):
    """Saves the final dataframe as a database table."""
    log_progress(f"Saving data to database table '{table_name}'")
    conn = sqlite3.connect(sql_connection)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    log_progress(f"Data successfully saved to database table '{table_name}'")

def run_query(query_statement, sql_connection):
    """Runs the stated query on the database table and prints the output on the terminal."""
    log_progress("Running query on the database")
    conn = sqlite3.connect(sql_connection)
    result = pd.read_sql(query_statement, conn)
    conn.close()
    log_progress("Query executed successfully")
    print(result)

# Main Code Execution
if __name__ == "__main__":
    URL = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    TABLE_ATTRIBS = {"class": "wikitable"}
    CSV_PATH = "Countries_by_GDP.csv"
    DB_PATH = "World_Economies.db"
    TABLE_NAME = "Countries_by_GDP"

    try:
        log_progress("ETL process started")
        
        # Extract
        df = extract(URL, TABLE_ATTRIBS)
        
        # Transform
        df = transform(df)
        
        # Load to CSV
        load_to_csv(df, CSV_PATH)
        
        # Load to Database
        load_to_db(df, DB_PATH, TABLE_NAME)
        
        # Query
        query = f"SELECT * FROM {TABLE_NAME} WHERE GDP_USD_Billions > 100"
        run_query(query, DB_PATH)
        
        log_progress("ETL process completed successfully")
    except Exception as e:
        log_progress(f"ETL process failed: {e}")
