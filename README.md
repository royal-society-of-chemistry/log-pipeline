# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

#### Quick summary ####

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

### How do I get set up? ###

* Summary of set up

 1.  Clone the repository to your local machine
 2.  Download some data files from other sites
 3.  Add some information to some configuration files
 4.  Run some set-up scripts
 5.  Ready to go!

* Dependencies

Ubuntu Linux
Python 3

* Database configuration
* How to run tests
* Deployment instructions

### Who do I talk to? ###

* Jeff White (whitejr@rsc.org)
* Data Science at RSC: http://www.rsc.org/data-science