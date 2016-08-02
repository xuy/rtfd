#!/usr/bin/python

from __future__ import print_function
import slumber
import json
import sys
import requests
import zipfile
import os

PROTOCOL = "http:"
usage = """ python rtfd.py slug_name"""

def download_file(url, local_filename):
    print("Downloding " + url + " and save as " + local_filename)
    try:
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    except:
        print ('Cannot download ' + url)
        return False

def unzip(local_filename, folder):
    print("Unzipping" + local_filename + " to folder " + folder)
    zip_ref = zipfile.ZipFile(local_filename, 'r')
    zip_ref.extractall(folder)
    zip_ref.close()

def add_index_entry(slug, folder):
    with open('index.md', 'a') as f:
        f.write("## [%s](%s/index.html)\n" % (slug, doc_name))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(usage)
    api = slumber.API(base_url='http://readthedocs.org/api/v1/')

    slug = sys.argv[1].lower()
    val = api.project.get(slug=slug)

    if val['objects']:
        obj = val['objects'][0]
        url = (PROTOCOL + obj['downloads']['htmlzip'])
        if not url:
            print("Cannot locate the document to download")
            sys.exit(-1)
        version = url.split('/')[-2]
        doc_name = '-'.join((slug, version))
        zip_file = doc_name + '.zip'
        if download_file(url, zip_file):
            unzip(zip_file, ".")
            os.remove(zip_file)

            add_index_entry(slug, doc_name)
