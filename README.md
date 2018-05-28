# keyserver-fs

Usage: python upload-file.py <file>  

### proof of concept on using pgp keyservers for Decentralized file storage

WARNING: this may break easily and is intended for use only on linux  

Using Python to open a file in binary then break it up and convert to base64 then insert that into a pgp pubring as new uid's. Once uploaded to a keyserver its there forever and propogated to all other key servers, making this a simple decentralised file storage system.  

I wrote this because i believe that pgp keyservers are very dangerous because of their poor design, anyone can upload any kind of data to them without the option for removal or peer review. Key Base although i am not a fan, require you to sign up and create an account instead of a simple dumping ground for keys that have the potential to contain sensitive data. There are endless ways to abuse this system, I have not even began to explore every option.

### format used

so we used uid's like so:  

    1@base64stringhere.com

The first of the uid(email) is numeric to stand for the order of the base64 string so we can be put it together again in the correct order, then the second part is simply a set chunk of binary data converted to base64.  

First of all had to test how many chars could be put in the uid, turns out after some testing just a little over 2040. Once you enter more than this the key becomes invalid and you have to reset your pubkey. Through some trial and error decided to stick with a safe number 1741 chars long. Once you split the binary data into 1305Byte chunks and convert it to base64 it comes to 1741 chars in length. 

### test file

For those who would like to test already uploaded data, i have placed a test file here:  
http://eu.pool.sks-keyservers.net/pks/lookup?search=STZFG%40ZDRRX&op=vindex

### ToDo

Which is best?  
Create program to parse the data from the site?  
Maybe also download the key locally with import and parse it this way?  
