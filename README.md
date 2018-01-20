# GHCN-data-cleanup
Scripts for manipulating the [NOAA GHCN data set](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn) to be in desirable format with fields including station name, county, state, date, temperature, geom so that it can be easily queried in a Postgres database. This is used as part of my Master's research to decide on a state to observe for extreme heat. By formatting the data this way, I can see which state has the highest frequency of extreme heat days temporally and spatially.

## Files needed:
* GHCN list of station IDs and locations. <ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt>
* GHCN station daily readings - one file per year. <ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/>

## Software needed:
* Postgres installation (with PostGIS extension) and pgAdminIII client
* Python and Python IDE (such as PyCharm community edition)

## Steps to take:
1. Open the file with the GHCN list of station IDs and locations. Delete all non-US stations (IDs that do not begin with "US") and all but the first 3 columns (ID, lat, long).
2. Create Postgres table named `us_station_locations` with columns `station_id`, `latitute` and `longitude`. Import your data into this table.
3. Import GHCN station daily readings into new Psotgres table called `station_temp_data_only`. Fields should be `station_id`, `date`, `obs_type`, `value`, `test1`, `test2`, `test3`, `test4`. Ultimately, we will only care about the first 4 columns.
    - Use the \COPY command in the psql command line for each file.
    - i.e. `\COPY state_selection.station_temp_data_only FROM 'C:\Users\User\Documents\Research\State Selection\2018.csv' CSV HEADER;`


