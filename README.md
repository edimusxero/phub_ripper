I didn't spend a ton of time writing this script but it does work.  

This is tested with python3

Required feilds are the following:

**-s / --search (REQUIRED)**

This is the term you are searching for.  It is required and needs to be wrapped in quotes if spaces are involved.

**-p / --pages**

Number of pages to scrape.  Not required, defaults to 1

**-l / --list_name**

Optional custom list name.  Defaults to list.txt

**-x / --premium**

Allows you to pass login credentials to scrape premium pages.  <username:password> format
    
**-v / --verbose**

Just prints out the titles of what your scrapping to console output


You can set a list name at the list_name variable.  All scraped urls are dumped into this file which can then be used with youtube-dl

I use youtube-dl like so

    youtube-dl -a list.txt
    
That command will download the best quality video and pull in the links from the list file
