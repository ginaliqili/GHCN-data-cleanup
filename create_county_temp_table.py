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
cur.execute("SELECT geoid, statefp, name FROM " + us_counties_table)
county_data = cur.fetchall()
for county_data in county_data:
    # Find all stations contained in given county
    cur.execute("SELECT a.station_id from " + station_location_table + " as a right join " + us_counties_table + " as b on st_contains(b.geom, a.geom) where b.geoid='" + county_data[0] + "'")
    stations_contained = cur.fetchall()
    # If the county has stations inside of it:
    if len(stations_contained) != 0:
        for station_contained in stations_contained:
            # Find all Tmax and Tmin readings from that station and add (statefp, county, obs_type, value, date) to new table
            cur.execute("SELECT obs_type, value, date FROM " + sys.argv[3] + " WHERE station_id = '" + station_contained[0] + "'")
            result = cur.fetchall()
            if len(result) != 0:
                print("result: " + str(len(result)))
                print("output table: " + sys.argv[3])
                print("station_id: " + station_contained[0])
                print("statefp: " + county_data[1])
                print("county: " + county_data[2])
                for r in result:
                    print(str(r))
                    cur.execute("INSERT INTO " + sys.argv[4] + " (statefp, county, obs_type, value, date) VALUES (" + county_data[1] + ", '" + county_data[2] + "', '" + r[0] + "', " + str(r[1]) + ", '" + str(r[2]) + "')")
                    conn.commit()
cur.close()
conn.close()

