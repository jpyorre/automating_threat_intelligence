# Go to the bottom to see how this works

import requests, os
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from feedparser import parse
import zipfile

d = parse('http://malware-traffic-analysis.net/blog-entries.rss')

downloaded_files = 'downloaded.txt'
open(downloaded_files, 'a').close() # Create downloaded_files.txt (used to unzip files before sending to sandbox)

def write_append(filename, line):
    writefile = open(filename,'a')
    writefile.write(line)
    writefile.close()

def download_files(item):
    updates = []
    paths = []
    content = requests.get(item['link']).content
    soup = BeautifulSoup(content, "html.parser")
    links = [l for l in soup.find_all('a') if l.has_attr('href')]
    download_url = "/".join(item['link'].split('/')[:-1]) + "/"
    link_texts = list(set([link.string for link in links]))
    page_text = soup.text
    title_dir = item['title']
    for filename in link_texts:
        try:
            if ".zip" in filename:  # Only find zip files
                if "pcap" in filename: # We don't need pcaps. Those will be recreated in the sandbox
                    continue
                else:
                    download_link = download_url + filename # Create the download link for each zip
                    print "Downloading: {}".format(download_link)   # Display what's happening
                    res = requests.get(download_link)   # Create the download object

                    # Download the files into the 'malware' directory
                    zipfile = open(os.path.join('malware', os.path.basename(filename)),'wb')

                    for chunk in res.iter_content(100000):
                        zipfile.write(chunk)
                    zipfile.close()
                    write_append(downloaded_files,'malware/' + filename +'\n')
        except:
            pass
        # except Exception,e: print str(e)

# 0: First Download (Do this once if you want to download everything in the blog_entries.rss)
def first_download():
    for item in d['items']:
        download_files(item)

# 1: Download New Files:
def most_recent_files_download():
    try:
        with open('most_recent.txt', 'r') as r:
            most_recent = r.readline().strip()
    except:
        most_recent = False
    new_most_recent = d['items'][0]['link']

    # Update most_recent.txt with the latest download so we aren't repeating things in the future
    with open('most_recent.txt', 'w') as w:
        w.write(new_most_recent)

    # Go through each link and download the files:
    for item in d['items']:
        if item['link'] == most_recent:
            break
        download_files(item)
# ############################
# # 2: Unzip the files:
def unzip_files():
    with open('downloaded.txt','r') as f:
        for i in f:
            split = i.strip().split('/')
            path = "/".join(split[:-1])
            file = split[-1]
            try:
                zipfile.ZipFile(path + '/' + file).extractall(path=path,pwd='infected')
            except Exception,e: print str(e)

def delete_zips():
    with open('downloaded.txt','r') as f:
        for i in f:
            try:
                os.remove(i.strip())
            except:
                pass
    os.remove('downloaded.txt')

def process_malware():
    malware_path = 'malware/'
    files = [f for f in listdir(malware_path) if isfile(join(malware_path, f))]
    for f in files:
        if '.exe' in f or '.doc' in f or 'xls' in f:
            print "Sending: {}".format(f)
            os.system("cuckoo submit malware/{}".format(f))

def delete_files_after_submitting():
    malware_path = 'malware/'
    for f in listdir(malware_path):
        try:
            os.remove("{}{}".format(malware_path,f.strip()))
        except:
            os.rmdir("{}{}".format(malware_path,f.strip()))
############################

# first_download()  # uncomment if you want to download everything in the blog_entries.rss. Might take a while...
most_recent_files_download() # download everything since the date in 'most_recent.txt'. It will be updated with todays date after the download.
unzip_files() # Unzip everything. CAUTION: THIS WILL UNZIP LIVE MALWARE!
delete_zips()   # Delete the zip files
process_malware()   # Send to cuckoo
delete_files_after_submitting()
