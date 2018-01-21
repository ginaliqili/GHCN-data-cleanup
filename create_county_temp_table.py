import sys
import psycopg2

# This script will identify the county and state of each station ID based on lat/long and output to a PostGIS table

# Read in station location table and us counties table
station_location_table = sys.argv[1]
us_counties_table = sys.argv[2]
print("station location table: " + station_location_table)
print("us counties table: " + us_counties_table)

# Connect to an existing database
try:
    conn = psycopg2.connect("dbname='research' user='postgres' host='localhost' password='postgres'")
except:
    print("I am unable to connect to the database")
# Open a cursor to perform database operations
cur = conn.cursor()
# Get all the county geometries
cur.execute("SELECT geoid FROM " + us_counties_table)
county_geoids = cur.fetchall()
for county_geoid in county_geoids:
    # Get all the station geometries
    cur.execute("SELECT geom FROM " + station_location_table)
    station_geoms = cur.fetchall()
    for station_geom in station_geoms:
        # Find all stations contained in given county
        cur.execute("SELECT a.station_id from " + station_location_table + " as a right join " + us_counties_table + " as b on st_contains(b.geom, a.geom) where b.geoid='" + county_geoid + "'")
        stations_contained = cur.fetchall()
        for station_contained in stations_contained:
            # Find all Tmax and Tmin readings from that station and add (statefp, county, data, Tmax, Tmin) to new table


