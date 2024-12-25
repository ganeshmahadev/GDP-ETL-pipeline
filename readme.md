# GDP Project: Extract, Transform, and Load (ETL) for Country GDP Data

## Overview
This project automates the process of extracting GDP data for countries from a Wikipedia page, transforming the data into billions of USD, and saving the results in both CSV and SQLite database formats. It also includes functionality to query the data for insights.

---

## Features
1. **Data Extraction**
   - Extracts GDP data for countries from a Wikipedia page.
   - Parses HTML tables using `BeautifulSoup` to retrieve the country name and GDP in USD (Millions).

2. **Data Transformation**
   - Converts GDP values from USD (Millions) to USD (Billions).

3. **Data Storage**
   - Saves the transformed data into a CSV file.
   - Loads the data into an SQLite database for easy querying.

4. **Query Execution**
   - Provides an example query to retrieve countries with GDP greater than 100 billion USD.

---

## Requirements

The project requires the following Python libraries:
- `requests`: For fetching the webpage data.
- `pandas`: For data manipulation and transformation.
- `sqlite3`: For database storage and query execution.
- `beautifulsoup4`: For parsing HTML tables.

### Installation
To install the required libraries, use:
```bash
pip install requests pandas beautifulsoup4
```

---

## Project Structure

```plaintext
etl_project.py         # Main ETL script
Countries_by_GDP.csv   # Transformed data in CSV format
World_Economies.db     # SQLite database file
etl_project_log.txt    # Log file for tracking execution
```

---

## How to Run the Project

1. Clone or download the project files.
2. Run the script using:
```bash
python etl_project.py
```
3. The script will:
   - Extract data from the Wikipedia page.
   - Transform GDP values from millions to billions.
   - Save the results to a CSV file and an SQLite database.
   - Execute an example SQL query to retrieve countries with GDP greater than 100 billion USD.

---

## Output
### Generated Files
- **CSV File:** The transformed data is saved as `Countries_by_GDP.csv`.
- **Database File:** The transformed data is stored in `World_Economies.db` under the `Countries_by_GDP` table.

### Example Query Result
The following query retrieves countries with GDP greater than 100 billion USD:
```sql
SELECT * FROM Countries_by_GDP WHERE GDP_USD_Billions > 100;
```
The output is printed on the terminal.

---

## Example Queries
To interact with the database, you can modify the SQL queries in the script or run your own queries using an SQLite client.

### Sample Queries:
1. **Print All Data:**
   ```sql
   SELECT * FROM Countries_by_GDP;
   ```
2. **Calculate Average GDP in Billions:**
   ```sql
   SELECT AVG(GDP_USD_Billions) FROM Countries_by_GDP;
   ```
3. **Retrieve Countries with GDP Less Than 50 Billion USD:**
   ```sql
   SELECT Country FROM Countries_by_GDP WHERE GDP_USD_Billions < 50;
   ```


