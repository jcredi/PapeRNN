#!/usr/bin/env python

"""
This is a simple script to harvest data from the arXiv (https://arxiv.org/).
To use default arguments, simply run in your terminal using

    python harvest.py

If you wish to use custom arguments, just run

    python harvest.py -h
    
to get a list of the arguments you can pass.

NOTE:
The following code was adapted from this blog post:
http://betatim.github.io/posts/analysing-the-arxiv/ 

"""

import time
import urllib2
import datetime
import os
import argparse
import xml.etree.ElementTree as ET

__author__ = "Jacopo Credi"
__license__ = "MIT"
__version__ = "1.4.3-rc"
__email__ = "jacopo.credi@gmail.com"

parser = argparse.ArgumentParser(description='Harvests paper titles from the arXiv (https://arxiv.org/).')
parser.add_argument('--arxiv', dest='arxiv', default='stat', help='Top-level archive to harvest from. Default: "stat"')
parser.add_argument('--category', dest='category', default='stat.ML', help='Archive category to consider. Default: "stat.ML"')
parser.add_argument('--dateFrom', dest='date_from', default='2007-05-01', help='Start date. Default: "2007-05-01"')
parser.add_argument('--dateTo', dest='date_to', default='2016-11-31', help='End date. Default: "2016-11-31"')
parser.add_argument('--dataDumpPath', dest='dump_file_path', default=os.getcwd()+'/data_dump/arxiv_dump.csv', 
    help='Path to file where harvested data will be saved for later use. Default: "<current_working_directory>/data_dump/arxiv_dump.csv"')

args = parser.parse_args()

OAI = "{http://www.openarchives.org/OAI/2.0/}"
ARXIV = "{http://arxiv.org/OAI/arXiv/}"
BASE_URL = "http://export.arxiv.org/oai2?verb=ListRecords&"


titles = []
url = (BASE_URL +
       "from=%s"%args.date_from +
       "&until=%s"%args.date_to +
       "&metadataPrefix=arXiv&set=%s"%args.arxiv)
    
while True:
    print "fetching", url
    try:
        response = urllib2.urlopen(url)
        
    except urllib2.HTTPError, e:
        if e.code == 503:
            to = int(e.hdrs.get("retry-after", 30))
            print "Got 503 (temporary overloading or maintenance). Let me retry in {0:d} seconds.".format(to)

            time.sleep(to)
            continue
            
        else:
            raise
        
    xml = response.read()
    root = ET.fromstring(xml)

    for record in root.find(OAI+'ListRecords').findall(OAI+"record"):
        meta = record.find(OAI+'metadata')
        info = meta.find(ARXIV+"arXiv")
        category_tags = info.find(ARXIV+"categories").text

        # if there is more than one DOI use the first one
        # often the second one (if it exists at all) refers
        # to an eratum or similar
        doi = info.find(ARXIV+"doi")
        if doi is not None:
            doi = doi.text.split()[0]
            
        # if the specified category is among the paper category 
        # tags, save the paper's title
        if args.category in category_tags.split():
            title = info.find(ARXIV+"title").text
            title = " ".join(title.split())
            titles.append(title)
    
    # The list of articles returned by the API comes in chunks of
    # 1000 articles. The presence of a resumptionToken tells us that
    # there is more to be fetched.
    token = root.find(OAI+'ListRecords').find(OAI+"resumptionToken")
    if token is None or token.text is None:
        break

    else:
        url = BASE_URL + "resumptionToken=%s"%(token.text)
 
# Save data for later use
if not os.path.exists(os.path.dirname(args.dump_file_path)):
    os.makedirs(os.path.dirname(args.dump_file_path))

with open(args.dump_file_path, 'w') as data_dump_file:
    for title in titles:
        data_dump_file.write("%s\n" % title)
print "Data saved in %s" % args.dump_file_path
