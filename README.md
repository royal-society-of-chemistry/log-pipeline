# README #

This README would normally document whatever steps are necessary to get your application up and running.

## What is this repository for? ##

### Quick summary ###

This repository contains the code for a data pipeline that takes as its input webserver log files. The pipeline does the following:

 1.  Converts the format to a W3C-based derivative
 2.  Remove internal web traffic
 3.  Identifies bot traffic
 4.  Identifies session IDs
 5.  Identifies the referrer address details
 6.  Does a GeoIP lookup
 7.  Does an IP-based customer lookup
 8.  Analyses the page accessed for product information
 9.  Deduplicates the user activity to remove multiple clicks
10.  Gives separate output files for bot and nonbot traffic. 

## How do I get set up? ##

### Summary of set up ###

 1.  Clone the repository to your local machine
 2.  Download some data files from other sites
 3.  Add some information to some configuration files
 4.  Run some set-up scripts
 5.  Ready to go!

### Dependencies ###

* Ubuntu Linux
* Python 3 (with packages: binascii, csv, datetime, fileinput, GeoIP, ipaddress, itertools, logging, marisa_trie, optparse, os, pickle, re, socket, struct, sys, time)

### Deployment instructions ###

 1.  Clone the bitbucket repository to a folder ("[yourfolder]") on your local machine
 2.  Go to: https://dev.maxmind.com/geoip/legacy/geolite/ and download the GeoLite City DAT file ("GeoLiteCity.dat"), and place it in the "[yourfolder]/_LIB/data" folder.
 3.  Go to: https://browscap.org/ then download the "browscap.csv" file, and place it in the "[yourfolder]/_LIB/csv" folder.
 4.  Run the script "[yourfolder]/_SYS/ProcessBrowscap.bsh". After a few minutes two files should appear in the "[yourfolder]/_LIB/pickle" folder: browscap_data_XXXX.pickle and browscap_trie_XXXX.pckle, where "XXXX" is the version number of the browscap release.
 5.  The process to generate the custom user agent list requires several steps:
  (a) Edit/create the file(s) that contain the details of user agent strings specific to your setup. Details of formatting can be found in "[yourfolder]/_SYS/ProcessUAList.cfg". An example file with a basic set of strings is here: "[yourfolder]/_LIB/csv/uas.csv".
  (b) Edit "[yourfolder]/_SYS/ProcessUAList.cfg" to list all the files created in step (a).
  (c) Run the script "[yourfolder]/_SYS/ProcessUAList.bsh". Two files should appear in the "[yourfolder]/_LIB/pickle" folder: ua_data.pickle and ua_str.pickle.
 6.  The process to generate the IP-based organisation lookup database requires several steps:
  (a) Edit/create the files that contain the details of the IP to name relationships. Details of formatting can be found in "[yourfolder]/_SYS/ProcessCustomIPs.cfg". An example file with the basic internal IP range is here: "[yourfolder]/_LIB/csv/ips.csv"
  (b) Edit "[yourfolder]/_SYS/ProcessCustomIPs.cfg" to list all the files created in step (a).
  (c) Run the script "[yourfolder]/_SYS/ProcessCustomIPs.bsh". A single file should appear in the "[yourfolder]/_LIB/data" folder: mmorg.dat
 7.  Edit the file [yourfolder]/_PIPES/Pipe1/CleanLogFiles.cfg to add:
  (a) appropriate find/replace regex patterns
  (b) set the number of processor cores
  (c) define the location(s) of the log file data to be processed
  (d) define the final locations of bot and nonbot log data after processing
  (e) set the browscap version variable from step (4) above.

Extra pipelines can be added as desired - copy/paste the original "pipe1" folder, renaming to e.g. "pipe2", then repeat step (7) for the new process.

### Execution ###

The script expects the original log files to be in the "NCSA Combined Log Format":

     host rfc931 username date:time request statuscode bytes referrer user_agent cookie

## Who do I talk to? ##

* Jeff White (whitejr@rsc.org)
* Data Science at RSC: http://www.rsc.org/data-science
