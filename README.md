# GHCN-data-cleanup
Scripts for manipulating the [NOAA GHCN data set](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn) to be in desirable format with fields including station name, county, state, date, temperature, geom so that it can be easily queried in a Postgres database. This is used as part of my Master's research to decide on a state to observe for extreme heat. By formatting the data this way, I can see which state has the highest frequency of extreme heat days temporally and spatially.

## Files needed:
* GHCN list of station IDs and locations. <ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt>
* GHCN station daily readings - one file per year. <ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/>
* [US Census county boundaries shapefile](https://www.census.gov/geo/maps-data/data/cbf/cbf_counties.html) with 500k resolution

## Software needed:
* Postgres installation (with PostGIS extension) and pgAdminIII client
* Python and Python IDE (such as PyCharm community edition)

## Steps to take:
1. Open the file with the GHCN list of station IDs and locations. Delete all non-US stations (station IDs that do not begin with "US") and all but the first 3 columns (station ID, lat, long).
2. Create Postgres table named `us_station_locations` with columns `station_id`, `latitute` and `longitude`. Import your data into this table. Create a new column called `geom` and generate the geom data from the lat/long columns
    - i.e. In pgAdmin execute `UPDATE state_selection.us_station_locations` SET geom = ST_MakePoint(longitude, latitude)`
3. Import US Census county boundaries shapefile into a new table named `us_counties`
    - Use the PostGIS Shapefile and DBF loader in pgAdminIII. Select the .shp file to import, change the name to `us_counties` and select the correct schema. For me, the schema is `state_selection`
    - Delete columns 'countyns', 'lsad', 'aland', and 'awater'
4. Import GHCN station daily readings into new Postgres table called `station_temp_data_only`. Fields should be `station_id`, `date`, `obs_type`, `value`, `test1`, `test2`, `test3`, `test4`. Ultimately, we will only care about the first 4 columns.
    - Use the \COPY command in the psql command line for each file.
        - i.e. `\COPY state_selection.station_temp_data_only FROM 'C:\Users\User\Documents\Research\State Selection\2018.csv' CSV HEADER;`
    - Delete the unnecessary columns named `test*` (these are metadata such as measurement, quality, and source flags, as well as observation times. For a breakdown of the columns see [this](./ghcn-daily-by_year-format.txt))
        - i.e. `ALTER TABLE state_selection.station_temp_data_only DROP COLUMN test1, test2, test3, test4`
    - Create new table without unnecessary rows (only interested in TMIN and TMAX)
        - Faster and more efficient to create a new table rather than deleting when it comes to specific rows
        - i.e. `CREATE table state_selection.station_temp_data_only2 AS (SELECT * FROM state_selection.station_temp_data_only where obs_type='TMIN' or obs_type='TMAX')`
5. Run `create_county_temp_table.py` and pass in `[schema_name].[us_station_locations table]`, `[schema_name].[us_counties table name]`, `[name of new output table]` as the arguments
    - This will look at each county boundary and see which stations are contained within it by assessing the lat/long data in the station location table. If it is contained, a new row is added to the new table. This is effectively identifying the state and county for each station, including the temperature and date information, and outputting it into a new PostGIS table.
    - i.e. Run `assign_county_and_state_to_station.py "state_selection.us_station_locations" "state_selection.us_counties" "us_stations_counties"`



