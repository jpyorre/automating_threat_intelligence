"""Unpack a MIME message into a directory of files and print a screenshot of the email"""
# I honestly can't remember if I wrote this, or modified someone else's code... but I've recently modified this a bit- jpyorre

import os
import sys
import email
import errno
import mimetypes
from optparse import OptionParser
from os import listdir
from os.path import isfile, join

def process_malware(malware_path):
    files = [f for f in listdir(malware_path) if isfile(join(malware_path, f))]
    for f in files:
        if '.exe' in f or '.doc' in f or 'xls' in f:
            print "Sending: {}".format(f)
            os.system("cuckoo submit {}/{}".format(malware_path,f))

parser = OptionParser(usage="""Unpack a MIME message into a directory of files.
# Usage: %prog msgfile""")
opts, args = parser.parse_args()

try:
    msgfile = args[0]
except IndexError:
    parser.print_help()
    sys.exit(1)
try:
    directory = str(msgfile.split('.')[0])
    os.mkdir(directory)
except OSError, e:
    # Ignore directory exists error
    if e.errno != errno.EEXIST:
        raise

fp = open(msgfile)
msg = email.message_from_file(fp)
fp.close()

counter = 1
for part in msg.walk():
    # multipart/* are just containers
    if part.get_content_maintype() == 'multipart':
        continue
    # Applications should really sanitize the given filename so that an
    # email message can't be used to overwrite important files
    filename = part.get_filename()
    if not filename:
        ext = mimetypes.guess_extension(part.get_content_type())
        if not ext:
            # Use a generic bag-of-bits extension
            ext = '.bin'
        filename = 'part-%03d%s' % (counter, ext)
    counter += 1
    fp = open(os.path.join(directory, filename), 'wb')
    fp.write(part.get_payload(decode=True))
    fp.close()
    if ".ksh" in filename or ".html" in filename:
        continue
    else:
        process_malware(directory)
