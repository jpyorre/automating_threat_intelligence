##################################
# Download samples from VirusTotal hunting results
##################################
import datetime, json, os, requests
import json, os
from urllib2 import Request, urlopen
from pprint import pprint as pp
####################################
# MAKE CHANGES HERE
####################################
virustotal_key = "VIRUSTOTALKEYGOESHERE"

# Go to https://www.virustotal.com/intelligence/hunting/, click on 'JSON', copy that whole URL and put it inside the quotes in the virustotal_notification_url variable. 
virustotal_notification_url = "FEEDURLGOESHERE"
hash_log = 'downloaded_hash_log.txt'
vt_hunter_downloader_log = 'vt_hunter_downloader_log.txt'

def write_log(filename, line):
    f = open(filename,'a')
    f.write(line)
    f.close


write_log(hash_log,"\n----------\n{0}\n----------\n".format(datetime.datetime.now()))
write_log(vt_hunter_downloader_log,"\n----------\n{0}\n----------\n".format(datetime.datetime.now()))

# Get the hunting url json contents:
request = Request(virustotal_notification_url)
request_response = urlopen(request).read()
data = json.loads(request_response)

sha_list = []	# Store the Sha's for download
i = 0
for d in data['notifications']:
    # if d['subject'] == 'hancitor':
    try:
        for item in data['notifications'][i]:
        	date = data['notifications'][i]['date']
        	sha256 = data['notifications'][i]['sha256']
        	size = data['notifications'][i]['size']
        	ruleset_name = data['notifications'][i]['ruleset_name']
        	first_seen = data['notifications'][i]['first_seen']
        	AV_positives = data['notifications'][i]['positives']
        	line = "Date: {0},AV Positives: {1}, YARA Ruleset: {2}, Filesize: {3}, SHA256: {4}".format(date,AV_positives,ruleset_name,size,sha256)
        	write_log(vt_hunter_downloader_log, line) # Write to a log file
        	#print line
        	if sha256 not in sha_list:
        		sha_list.append(sha256)
        	i +=1

        for hash in sha_list:
        	with open(hash_log, 'r') as already_downloaded:
        		if hash not in already_downloaded.read():
        			name = hash + '.exe'
        			dest_dir = os.path.dirname('samples/')
        			path = os.path.join(dest_dir,name)
        			params = {'apikey': virustotal_key, 'hash': hash}
        			response = requests.get('https://www.virustotal.com/vtapi/v2/file/download', params=params)
        			downloadedfile = response.content
        			fo = open(path,"wb")
        			fo.write(downloadedfile + '.exe')
        			fo.close()
        			write_log(hash_log, hash + '\n')
    except:
        pass
print ("Files are in the 'Samples' directory\nLog written to auto_downloader_log.txt")
