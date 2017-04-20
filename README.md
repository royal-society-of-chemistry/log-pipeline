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

1. Clone the bitbucket repository to a folder (**[yourfolder]**) on your local machine
2. Go to **https://dev.maxmind.com/geoip/legacy/geolite/** and download the GeoLite City DAT file (**GeoLiteCity.dat**), and place it in the **[yourfolder]/_LIB/data** folder.
3. Go to **https://browscap.org/** then download the **browscap.csv** file, and place it in the **[yourfolder]/_LIB/csv** folder.
4. Run the script **[yourfolder]/_SYS/ProcessBrowscap.bsh**. After a few minutes two files should appear in the **[yourfolder]/_LIB/pickle** folder: **browscap_data_XXXX.pickle** and **browscap_trie_XXXX.pickle**, where "XXXX" is the version number of the browscap release.
5. Edit/create the file(s) that contain the details of user agent strings specific to your setup. Details of formatting can be found in **[yourfolder]/_SYS/ProcessUAList.cfg**. An example file with a basic set of strings is here: **[yourfolder]/_LIB/csv/uas.csv**.
6. Edit **[yourfolder]/_SYS/ProcessUAList.cfg** to list all the files created in the previous step.
7. Run the script **[yourfolder]/_SYS/ProcessUAList.bsh**. Two files should appear in the **[yourfolder]/_LIB/pickle** folder: **ua_data.pickle** and **ua_str.pickle**.
8. Edit/create the files that contain the details of the IP to name relationships. Details of formatting can be found in **[yourfolder]/_SYS/ProcessCustomIPs.cfg**. An example file with the basic internal IP range is here: **[yourfolder]/_LIB/csv/ips.csv**
9. Edit **[yourfolder]/_SYS/ProcessCustomIPs.cfg** to list all the files created in the previous step.
10. Run the script **[yourfolder]/_SYS/ProcessCustomIPs.bsh**. A single file should appear in the **[yourfolder]/_LIB/data** folder: **mmorg.dat**
11. Edit the file **[yourfolder]/_PIPES/Pipe1/CleanLogFiles.cfg** to: add appropriate find/replace regex patterns; set the number of processor cores; define the location(s) of the log file data to be processed; define the final locations of bot and nonbot log data after processing; and set the browscap version variable from above.

Extra pipelines can be added as desired - copy/paste the original **pipe1** folder, renaming to e.g. **pipe2**, then repeat step (11) for the new process.

### Execution ###

Execute the script: **[yourfolder]/_PIPES/Pipe1/CleanLogFiles.bsh**

The script expects the original log files to be in the "NCSA Combined Log Format":

    host rfc931 username date:time request statuscode bytes referrer user_agent cookie

They should be compressed as RAR archives; the log files within the RAR file can be optionally compressed as GZIP archives.

## Who do I talk to? ##

* Jeff White (whitejr@rsc.org)
* Data Science at RSC: http://www.rsc.org/data-science