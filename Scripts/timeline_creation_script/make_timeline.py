inputfile = 'sample.txt'
outputfile = 'sample.html'

def write_append(filename, line):
    writefile = open(filename,'a')
    writefile.write(line)
    writefile.write('\n')
    writefile.close()

# hash first seen: be5bee2088a8d46f74d787ca59abbe9ade56f9bbad11b6e34f77ff219ea8fe8d, 2017-10-29 11:04:58
htmltop = """
<!DOCTYPE HTML>
<html>
<head>
  <title>Timeline basic demo</title>
  <script src="vis.min.js"></script>
  <link href="vis.min.css" rel="stylesheet" type="text/css" />

  <style type="text/css">
    body, html {
      font-family: sans-serif;
    }
  </style>
</head>
<body>
<div id="visualization"></div>

<script type="text/javascript">
  var container = document.getElementById('visualization');
  var data = ["""

htmlbottom = """];
  var options = {};
  var timeline = new vis.Timeline(container, data, options);
</script>
</body>
</html>"""


# data must look like this:
# {id: 1, content: 'item 1', start: '2013-04-20'},
# convert data with: cat 185.90.61.36_passivedns.txt | awk '{print $1 "," $3}' > passivednsdata.txt

data = []
idnumber = 0
with open(inputfile,'r') as f:
	for line in f.read().split('\n'):
		l = line.split(',')
		try:
			dt = l[0]
			domain = l[1]
		except:
			continue
		idnumber +=1
		dataline = {'id':idnumber, 'content':domain,'start':dt}
		dataline = str(dataline)


		# dataline = "{"+"'id': "+str(idnumber)+", content: '"+domain+"', start: '"+dt+"'},"
		cleaneddataline = dataline.replace("'content'","content").replace("'start'","start").replace("'id'","id")
		data.append(cleaneddataline)

writefile = open(outputfile,'w')
write_append(outputfile,htmltop)
for i in data:
	write_append(outputfile,i + ",")
# htmlfinal = "{}{}{}".format(htmltop,data,htmlbottom)
write_append(outputfile,htmlbottom)