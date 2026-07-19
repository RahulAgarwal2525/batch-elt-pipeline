import os
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent directory
# This allows us to test the script locally on our laptop
load_dotenv()

# OpenWeatherMap API Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Database Configuration
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
# Note: Since we are running this script locally on our laptop right now, the host is 'localhost'.
# When we eventually run this inside a Docker container, the host will be 'postgres'.
DB_HOST = os.getenv('DB_HOST', 'localhost') 
DB_PORT = "5432"

# A list of major tech hubs we want to track
CITIES = ["London", "San Francisco", "New York", "Tokyo", "Bengaluru", "Berlin"]

def extract_weather_data():
    """
    Fetches weather data from OpenWeatherMap API and loads it into the PostgreSQL database.
    """
    if not API_KEY:
        print("ERROR: OPENWEATHER_API_KEY is missing. Please check your .env file.")
        return

    # Initialize database connection variable so we can safely close it in the 'finally' block
    conn = None

    try:
        print(f"Connecting to database {DB_NAME} at {DB_HOST}...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        # Create a cursor object to execute SQL commands
        cur = conn.cursor()

        for city in CITIES:
            print(f"Fetching data for {city}...")
            
            # Set up API parameters (units=metric gets us Celsius)
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            
            # Make the GET request to the API
            response = requests.get(BASE_URL, params=params)
            
            # Raise an exception if the API call failed (e.g., 401 Unauthorized, 404 Not Found)
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            # Extract only the specific fields we need for our raw table
            city_name = data['name']
            temperature_celsius = data['main']['temp']
            humidity_percentage = data['main']['humidity']
            weather_condition = data['weather'][0]['main']
            
            # Prepare the SQL INSERT statement
            insert_query = """
                INSERT INTO raw_weather_data (city_name, temperature_celsius, humidity_percentage, weather_condition)
                VALUES (%s, %s, %s, %s)
            """
            
            # Execute the query with the extracted data
            cur.execute(insert_query, (city_name, temperature_celsius, humidity_percentage, weather_condition))
            print(f"Successfully inserted raw data for {city_name}.")

        # Commit the transaction to save all our inserts
        conn.commit()
        print("Data extraction and loading completed successfully!")

    except requests.exceptions.HTTPError as http_error:
        # Check specifically for a 401 Unauthorized error
        if http_error.response.status_code == 401:
            print(f"API ERROR (401): OpenWeatherMap rejected your API key.")
            print("If you just created the key, it often takes 10-20 minutes to activate.")
            print("Please wait a few minutes and try again.")
        else:
            print(f"API HTTP ERROR: Failed to fetch data from OpenWeatherMap. Details: {http_error}")
    except requests.exceptions.RequestException as api_error:
        print(f"API NETWORK ERROR: Failed to reach OpenWeatherMap. Details: {api_error}")
    except psycopg2.Error as db_error:
        print(f"DATABASE ERROR: Failed to interact with PostgreSQL. Details: {db_error}")
    except Exception as e:
        print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
    
    finally:
        # This block ALWAYS runs, ensuring we don't leave zombie connections open
        if conn is not None:
            cur.close()
            conn.close()
            print("Database connection closed.")

# Make sure these two lines are at the very bottom of your file!
# Without them, the script will do absolutely nothing.
if __name__ == "__main__":
    extract_weather_data()