import sys
import psycopg2

# Read in station location file and station temperature file
#station_locations = open("", "")
station_locations_file = sys.argv[1]
station_temperature_directory = sys.argv[2]
print("station location file: " + station_locations_file)
print("station temperature directory: " + station_temperature_directory)

# Connect to an existing database
conn = psycopg2.connect("dbname=research user=postgres")
# Open a cursor to perform database operations
cur = conn.cursor()
# 
