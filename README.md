# automating threat intelligence scripts and documentation


# Installation Guides:

## cuckoo installation.txt
I started to write this as a shell script, but it requires interaction and I haven't yet dealt with that. Use it as a guide, making sure to change your networking and various passwords (for things like SQL) to match your environment and needs

## installMisp.txt
If you want to install MISP, this will get it done. It requires some interactivity and changing of passwords/networking stuff. I set it up in its own virtual machine because you have to install so much stuff.


# Scripts:

# MTAScraper:
## Scrapes http://malware-traffic-analysis.net/ blog entries and downloads the malware for personal analysis. Warning, it will unzip live malware (if you enable that function)

-----------------
# vt_hunter_downloader

## Download all samples that you're hunting for in Virustotal Intelligence
## Make these changes in vt_hunter_downloader.py:

virustotal_key = "putvirustotalkeyhere"

Go to https://www.virustotal.com/intelligence/hunting/, click on 'JSON', copy that whole URL and put it inside the quotes in the virustotal_notification_url variable. It will look something like this:
https://www.virustotal.com/intelligence/hunting/notifications-feed/?key=yourapikey

virustotal_notification_url = "FULL_URL_HERE"

---------------
## timeline_creation_script
Create timelines with data formatted like the sample.txt file

--------------
## Cuckoo Scraper Script

I took this script from: https://github.com/OpenSecurityResearch/CuckooScraperScript
and started modifiying it to give me something more useful for my needs.
Right now, it's still 'in progress' as I map all the fields created by a cuckoo analysis.

# Tools/Utilities:

## YARA Rules:
https://github.com/Yara-Rules/rules