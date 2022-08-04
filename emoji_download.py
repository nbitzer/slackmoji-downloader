# pylint: disable=line-too-long
#!/usr/bin/env python3

"""
FILL ME IN
"""
import os
from os import path
import logging
import requests
from bs4 import BeautifulSoup

# Setup basic logging config
logging.basicConfig(filename='emoji_downloader.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

SLACKMOJI_BASE_URL = 'https://slackmojis.com'
# All emojis will be saved in a new directory in which this script is executed
SLACKMOJI_LOCAL_DIR = os.getcwd() + "/slackmojis"

# Create directory to store all emojis
if not os.path.exists(SLACKMOJI_LOCAL_DIR):
    os.mkdir(SLACKMOJI_LOCAL_DIR)

# Create local directory to store emojis
# Use bs4 to parse the page for the emoji URLs
# Use requests to download all the emojis to the correct directory

# STRETCH: Use a slackapi to upload images


def download_file(url, filename):
    """ FILL ME IN """
    full_file_path = os.path.join(SLACKMOJI_LOCAL_DIR, filename)
    logging.info("Downloading emoji from: '%s'", url)
    with requests.get(url, allow_redirects=True) as req:
        with open(full_file_path, 'wb') as file:
            logging.info("writing emoji file '%s' to '%s'", filename, full_file_path)
            file.write(req.content)
            file.close()

def parse_filename(url):
    """ FILL ME IN """
    fragment_removed = url.split("#")[0]
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        return ""
    return path.basename(scheme_removed)

# Make call to get html containing links to emojis
try:
    r = requests.get(SLACKMOJI_BASE_URL + '/emojis/popular')
except requests.exceptions.HTTPError as err:
    raise SystemExit(err) from err

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

emoji_list = []

# Get all the <img> elements on the given page
images = soup.select('img')

for image in images:
    src = image.get('src')
    # Toss out any odd HTML we might have gotten by assuming all files are .png or .gif
    if '.png' or '.gif' in src:
        emoji_list.append({"src": src})
    else:
        print(f"WARN: Image source '{src}' not a valid file for download")

for image in emoji_list:
    file_name = parse_filename(image['src'])
    download_file(image['src'], file_name)
