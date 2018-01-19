# GHCN-data-cleanup
Scripts for manipulating the NOAA GHCN data set to be in desirable format with fields including station name, county, state, date, temperature, geom

## Files needed:
* GHCN list of station IDs and locations. Data [here](ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt "GHCN station list")
* GHCN station daily temperature readings - one file per year. Data [here](ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/)

## Software needed:
* Postgres installation (with PostGIS extension) and pgAdminIII client
* Python and Python IDE (such as PyCharm community edition)

## Steps to take:
1. Open the file with the GHCN list of station IDs and locations. Delete all non-US stations (IDs that do not begin with "US") and all but the first 3 columns (ID, lat, long).
2. Create Postgres table named `us_station_locations` with columns `station_id`, `latitute` and `longitude`. Import your data into this table.
3. Run `clean-yearly-file.py` and specify the directory with all the GHCN station daily temperature readings. This will load the temperature data into a new Postgres table titled `station_temp_data_only`.
