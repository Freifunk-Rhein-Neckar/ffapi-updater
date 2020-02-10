# ffapi-updater
ffapi-updater helps to manage your Freifunk API file.

## Prerequisites
The following files should be available on filesystem of server (if necessary 
download them before execution, e.g. using wget):
- nodes.json (v2) of Meshviewer's ffmap-backend (could also be remote url)
- Freifunk-API json file 

ffapi-updater modifies your API file, so best practice is to run it on that 
server that hosts your API file. If this is not possible, you need to 
upload your API file after each execution to its place. In our case API and
map files are hosted on the same server, so both needed json files could be 
referenced directly.

Since V1.2.0 it is possible to load a remote nodes.json (via url), simply 
configure the complete url and no loacal nodes.json will be used.

Furthermore SITE_CODE is checked, this helps to filter in multi site 
communities.


## Installation
To use it, simply clone this repository to a folder on your map server, create a copy 
of the `settings-example.conf` named `settings.conf` and set the settings according 
to your needs.

Updating your API file should happen on a regularly basis e.g. each 5 min, 
therefore create a cron job like this: 

<pre>
*/5 * * * * (cd /home/freifunk/ffapi-updater && /usr/bin/python3 /home/freifunk/ffapi-updater/ffapi-updater.py >/home/freifunk/ffapi-updater/ffapi-updater.log 2>&1)
</pre>

## Dependencies
- python3

