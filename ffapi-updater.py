#!/usr/bin/env python3

# ------------------------------------------------------------------------------
#
#    ffapi-updater - Update Freifunk API file
#    Copyright (C) 2016,2019 Benjamin Schmitt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Source code available at: https://github.com/Little-Ben/ffapi-updater
#
# ------------------------------------------------------------------------------
# This python script counts all active nodes (online = true)
# and updates the node count and lastchange date (UTC) in APIFILE.
# The source is a meshviewer's nodes.json in version 2.
# ------------------------------------------------------------------------------
# Configuration:
# - APIFILE is a local file containing your API-File,
#   file must be writeable for executing user
# - NODESFILE_REMOTE is a remote source
#  (https://example.com/meshviewer/nodes.json)
# - NODESFILE_LOCAL is a local source
#   and will only be used if NODESFILE_REMOTE is not given (empty string '')
# - SITE_CODE is the abbreviation of your community, i.e. 'ffwp'
#  (it has to be given, and could be used as a filter in multi-community setups)
#
# Configuration start
APIFILE = '../api/FreifunkWestpfalz-api.json'
NODESFILE_LOCAL = '../meshviewer/nodes.json'
NODESFILE_REMOTE = ''
SITE_CODE = 'ffwp'
# Configuration end
# ------------------------------------------------------------------------------

VERSION = 'V1.2.0'

import json,requests
from pprint import pprint
from datetime import datetime

def main():
    print("\nffapi-updater",VERSION,"Copyright (C) 2016,2019 Benjamin Schmitt")
    print("----------------------------------------------------------------------")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it,")
    print("see LICENSE for details.")
    print("Source code available at: https://github.com/Little-Ben/ffapi-updater")
    print("----------------------------------------------------------------------")

    with open(APIFILE) as data_file:
        data = json.load(data_file)

    if NODESFILE_REMOTE != "":
        headers = {
            'User-Agent': 'ffapi-updater by Little-Ben, ' + VERSION + ', used by: ' + SITE_CODE + ', see: https://github.com/Little-Ben/ffapi-updater'
        }

        r = requests.get(NODESFILE_REMOTE, headers=headers)
        dataNodes = r.json()
    else:
        with open(NODESFILE_LOCAL) as node_file:
            dataNodes = json.load(node_file)

    #count data
    iNodeCount=0
    iNodeCountSite=0
    iNodeCountFile=0
    for node in dataNodes["nodes"]:
        if dataNodes["nodes"][node]["nodeinfo"]["system"].get("site_code","n/a") == SITE_CODE:
            if dataNodes["nodes"][node]["flags"].get("online",False) == True:
                iNodeCount = iNodeCount + 1
            iNodeCountSite = iNodeCountSite + 1
        iNodeCountFile = iNodeCountFile + 1

    #data update
    print("UTC time:\t\t\t ", datetime.utcnow().strftime("%Y-%m-%dT%T.%f"))
    iNodeCountOld=data["state"]["nodes"]
    print("node count site/online old:\t ", str(iNodeCountOld))
    data["state"]["nodes"] = iNodeCount
    data["state"]["lastchange"] = datetime.utcnow().strftime("%Y-%m-%dT%T.%f")
    print("node count site/online new:\t ", str(data["state"]["nodes"]))
    print("node count site/all:\t\t ", str(iNodeCountSite))
    print("node count file/all:\t\t ", str(iNodeCountFile))

    if iNodeCountOld != iNodeCount:
        #write new api file, sorted and prettyprinted - only if node count changed
        with open(APIFILE, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        bApiChanged=True
    else:
        bApiChanged=False

    #write end message depending if changes happend
    print("----------------------------------------------------------------------")
    if bApiChanged == True:
        strEndMessage="API file updated successfully."
    else:
        strEndMessage="API file unchanged."
    print(strEndMessage, "DONE.\n")

    exit(0)

if __name__ ==  "__main__":
    main()
