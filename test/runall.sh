cd ..
echo AHRF
python -m AHRF.main

echo USGS
python -m USGS.main

echo acra
python -m acra.main

echo agriculture
python -m agriculture.main

echo census
python -m census.main

echo crime
python -m crime.main

echo election
python -m election.main

echo groundwater
python -m groundwater.main
