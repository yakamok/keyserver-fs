# Using PGP keyservers for decentralised file storage
    
### This is a proof of concept

WARNING: this may break easily and is intended for use only on linux, & only for educational purposes.  

Using Python to open a file in binary then break it up and convert to base64 then insert that into a pgp pubring as new uid's. Once uploaded to a keyserver its there forever and propogated to all other key servers, making this a simple decentralised file storage system.  

I wrote this because of the keyservers poor design, anyone can upload any kind of data to them without the option for removal or peer review, for example i uploaded the entire GDPR. Key Base although i am not a fan, at least require you to sign up and create an account instead of a simple dumping ground for keys that have the potential to contain sensitive data. There are endless ways to abuse this system, I have not even began to explore every option.

__Notice:__ This Program is very slow to add data to the gpg pubkey so dont plan on super large files, this is also not safe to use in any kind of production enviroment as its using subprocess and shell is set to true.  
### upload-file.py

Usage: python upload-file.py <file>  
Data can take between 3-10mins before it apears on the server so don't be supprised if the link your given does not work straight away.  
Requirements: gnupg2, pinentry  

### download-keyserv.py

Usage: python download-keyserv.py "http://eu.pool.sks-keyservers.net/pks/lookup?search=WCNGKCCWBE@UMKVS.jpg&op=index"  
Requirements: python-bs4  

### Format used

The first uid has the file extention at the end: random@random.jpg   

so we used uid's like so:  

    1@base64stringhere

The first of the uid(email) is numeric to stand for the order of the base64 string so we can be put it together again in the correct order, then the second part is simply a set chunk of binary data converted to base64.  

First of all had to test how many chars could be put in the uid, turns out after some testing just a little over 2040. Once you enter more than this the key becomes invalid and you have to reset your pubkey. Through some trial and error decided to stick with a safe number 1741 chars long. Once you split the binary data into 1305Byte chunks and convert it to base64 it comes to 1741 chars in length. 

Key deletion was added after upload is completed as the keys are no longer needed.  

### Test file

For those who would like to test already uploaded data, i have placed a test file here:  
http://eu.pool.sks-keyservers.net/pks/lookup?search=WCNGKCCWBE@UMKVS.jpg&op=index  
