#CuckooScraperScript
#by Sk3tchymoos3

import os
import json
import jinja2
import argparse
from pprint import pprint as pp

parser = argparse.ArgumentParser(description='Reiterates through your Cuckoo Analyses and returns the Yara hits, VT hits, and links to the HTML report')
parser.add_argument('-p', '--path', help="Path you your cuckoo analyses folder", required=True)
# parser.add_argument('-t', '--template', help="Path to your template", required=True)
# parser.add_argument('-o', '--output', help="Path you want to save the output to", required=True)

args= vars(parser.parse_args())

pathToFolder=args['path']
# template=args['template']
# outputFile=args['output']


#jinja stuff
# templateLoader= jinja2.FileSystemLoader( searchpath="/")
# templateEnv = jinja2.Environment( loader=templateLoader)
# TEMPLATE_FILE=template
# template= templateEnv.get_template(TEMPLATE_FILE)

#get all the folder name in the directory
dirName= []
for stuff in os.listdir(pathToFolder):
	dirName.append(stuff)

# htmlFile=open(outputFile, "w")
# htmlFile.write("<HTML>")

network = []
for number in dirName:
	if number == ".DS_Store":
		pass
	else:
		rootDir=pathToFolder
		path=os.path.join(rootDir,number,"reports/report.json")
		urlPath=os.path.join(rootDir,number,"reports/report.html")
		if os.path.isfile(path):
			with open(path) as data_file:
				# try:
				data=json.load(data_file)
				behavior = data['behavior']
				signatures = data['signatures']
				try:
					dropped = data['dropped']
				except:
					pass
				network = data['network']
				target = data['target']

				# pp(data)
				# for i in behavior['generic']:
				# 	print "process_path: {}".format(i['process_path'])	# What exe was run on the system after opening the malware
				# 	print "first_seen: {}".format(i['first_seen'])	# First seen date
				# 	print "process_name: {}".format(i['process_name'])	# What exe was run on the system after opening the malware
				# 	print '=' * 100
				#
				# ## SUMMARY:
				# 	summary = i['summary']
				# 	for s in summary:
				# 		for x in summary[s]:
				# 			print "{}:\n\t{}".format(s,x)
				# 		print '*' * 100


				# ### DROPPED FILES
				# try:
				# 	for i in dropped:
				# 		for x in i:
				# 			print "{}: {}".format(x, i[x])
				# 	print '=' * 100
				# except:
				# 	pass

				iocs = []
				for s in signatures:
					marks = s['marks']
					try:
						for i in marks:
							ioc = i['ioc']
							iocs.append(ioc)
					except:
						pass
				for i in iocs:
					print i
				## NETWORK:
				tcps = []
				udps = []
				https = []
				domains_seen = []
				dns_results = []
				for i in network:
					if len(network[i]) <= 1: # Don't print something if there's no data
						pass
					else:
						dns = network['dns']
						for d in dns:
							line = []
							dns_line = {}
							dns_line['request'] = d['request']
							dns_line['type'] = d['type']
							answer = d['answers']
							for i in answer:
								dns_line['a_type'] = i['type']
								dns_line['a_record'] = i['data']
								line.append(dns_line)
							dns_results.append(line)

						domains = network['domains']
						for d in domains:
							domainline = "{},{}".format(d['domain'],d['ip'])
							domains_seen.append(domainline)

						tcp = network['tcp']
						udp = network['udp']
						http_ex = network['http_ex']

						for h in http_ex:
							httpline = "{},{},{},{},{},{},{},{}\n".format(h['dst'], h['dport'], h['host'], h['method'], h['request'], h['response'], h['status'], h['uri'])
							https.append(httpline)

						for t in tcp:
							tcpline = "{},{}".format(t['dst'], t['dport'])
							tcps.append(tcpline)

						for u in udp:
							udpline = "{},{}".format(u['dst'], u['dport'])
							udps.append(udpline)
						# for s in network[i]:
							# print "{}: {}".format(i,s)
							# pp(s)

							# print s['host']
					# else:
					# 	pp(s)
						# print "{}: {}".format(i,network[i])


				# for i in dns_results:
				# 	print i
				print '=' * 100
				print "TCP:"
				print '=' * 100
				for t in set(tcps):
					print t
				print '=' * 100
				print "UDP:"
				print '=' * 100
				for u in set(udps):
					print u
				print '=' * 100
				print "HTTP:"
				for h in set(https):
					print h
				print '=' * 100
				print "DOMAINS:"
				for d in set(domains_seen):
					print d


				### TARGET (FILE INFO):
				# for x in target['file']:
				# 	print "{}: {}".format(x,data['target']['file'][x])
				# print '=' * 100

				#
				# 	filename=data["target"]["file"]["name"]
				# 	yaraHits=data["target"]["file"]["yara"]
				# 	# print yaraHits
				# 	try:
				# 		virusTotalResponseCode=data["virustotal"]["response_code"]
				#
				# 		#if we have any VirusTotal hits...
				# 		if virusTotalResponseCode != 0:
				# 			numPositive=data["virustotal"]["positives"]
				# 			VTurl=data["virustotal"]["permalink"]
				# 	except:
				# 		pass
				# 	# #else keep the fields blank!
				# 	# else:
				# 	# 	numPositive=" "
				# 	# 	VTurl=" "
				# 	# virusTotalVerbose=data["virustotal"]["verbose_msg"]
				# 	# url=urlPath
				# 	# templateVars = {"name":filename,"yara":yaraHits, "VTResponse":virusTotalResponseCode, "VTVerbose":virusTotalVerbose,"urlAddress":url,"VTHits":numPositive, "VTUrl": VTurl}
				# 	# outputText = template.render(templateVars)
				# 	# htmlFile.write(outputText)
				# except:
		# 		# 	pass
		# else:
		# 	# print "File ", path, " does not exist!"
		# 	pass

# htmlFile.write("</HTML>")
# htmlFile.close()
