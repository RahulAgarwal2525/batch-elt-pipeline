import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
# Default to localhost for local testing
DB_HOST = os.getenv('DB_HOST', 'localhost') 
DB_PORT = "5432"

def transform_data():
    """
    Transforms raw weather data into daily summaries entirely within PostgreSQL.
    This demonstrates the 'T' in an ELT pattern using Pushdown Compute.
    """
    conn = None
    try:
        print("Connecting to database to start transformation...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # The Transformation Query (ELT)
        # 1. We group by the city and the current date.
        # 2. We calculate the Average Temp and Max Humidity.
        # 3. ON CONFLICT: If a summary for this city/date already exists, we UPDATE it. 
        #    If it doesn't exist, we INSERT it. This guarantees Idempotency!
        transform_query = """
            INSERT INTO daily_weather_summary (report_date, city_name, avg_temperature, max_humidity, total_records)
            SELECT 
                CURRENT_DATE AS report_date,
                city_name,
                ROUND(AVG(temperature_celsius), 2) AS avg_temperature,
                MAX(humidity_percentage) AS max_humidity,
                COUNT(*) AS total_records
            FROM raw_weather_data
            WHERE DATE(ingested_at) = CURRENT_DATE
            GROUP BY city_name
            ON CONFLICT (report_date, city_name) 
            DO UPDATE SET 
                avg_temperature = EXCLUDED.avg_temperature,
                max_humidity = EXCLUDED.max_humidity,
                total_records = EXCLUDED.total_records,
                updated_at = CURRENT_TIMESTAMP;
        """
        
        print("Executing transformation query...")
        cur.execute(transform_query)
        
        # We can ask the cursor how many rows it just inserted/updated
        rows_affected = cur.rowcount
        
        conn.commit()
        print(f"Transformation successful! Upserted {rows_affected} daily summary rows.")

    except psycopg2.Error as db_error:
        print(f"DATABASE ERROR during transformation: {db_error}")
    except Exception as e:
        print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    transform_data()