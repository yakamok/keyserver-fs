# Using PGP keyservers for decentralised file storage
    
### This is a proof of concept for educational use only!

WARNING: this may break easily and is intended for use only on linux, & only for educational purposes.  

So this basically works because you can have a UID(email address) that is 2048 characters in your PGP key, and from what I understand an unlimited amount of UIDs, perfect for dumping data on to the key-servers, Adding UIDs is a slow process by hand so I automated it using python, so you could dump any kind of file on the key servers. With some simple modifications you can dump plain text on to the key-servers containing any content you choose and watch it propagate through all the key-servers around the world. Once that has completed, the data is essentially impossible to be removed as said by the sks key-server Maintainer himself [Kristian Fiskerstrand](https://blog.sumptuouscapital.com/2016/03/openpgp-certificates-can-not-be-deleted-from-keyservers/).

I wrote this because I think this characteristic of key-servers is actually dangerous, for example someone could upload leaked data and it would be spread around the world and accessible by anyone and unstoppable, how would this situation be dealt with?

### Which Parts of the GDPR this might be affected by:  

I would be happy for people to make pull requests to add information they think is relevant to this.  

You can also join in the discussion in the comments of an [article](https://medium.com/@mdrahony/are-pgp-key-servers-breaking-the-law-under-the-gdpr-a81ddd709d3e) I wrote to accompany this project.  

I have moved this section to a separate document [GDPR and its effects](https://github.com/yakamok/keyserver-fs/blob/master/GDPR.md)  

### Usage 

__Notice:__ This Program is very slow to add data to the gpg pubkey so don't plan on super large files.  

### upload-text-file.py

Usage: python upload-text-file.py plain-text-file.txt  
One thing to note, is the text will not appear ordered, so don't expect a long rant to appear as you want it to.  
Also character length of each line should not exceed 2000 or the key will break and be unusable.  

### upload-file.py

Usage: python upload-file.py <file>  
Data can take between 3-10mins before it appears on the server so don't be surprised if the link you're given does not work straight away.  
Requirements: gnupg2, pinentry  

### download-keyserv.py

Usage: python download-keyserv.py "http://eu.pool.sks-keyservers.net/pks/lookup?search=WCNGKCCWBE@UMKVS.jpg&op=index"  
Requirements: python-bs4  

The first of the uid(email) is numeric to stand for the order of the base64 string so we can be put it together again in the correct order, then the second part is simply a set chunk of binary data converted to base64.  

First of all had to test how many chars could be put in the uid, turns out after some testing just a little over 2040. Once you enter more than this the key becomes invalid and you have to reset your pubkey. Through some trial and error decided to stick with a safe number 1741 chars long. Once you split the binary data into 1305Byte chunks and convert it to base64 it comes to 1741 chars in length. 

Key deletion was added after upload is completed as the keys are no longer needed.  

### Test file

For those who would like to test already uploaded data, i have placed a test file here:  
http://eu.pool.sks-keyservers.net/pks/lookup?search=WCNGKCCWBE@UMKVS.jpg&op=index  

### unpublished 

I wrote a version of this using OpenMPI to see what kind of scale this could be used on, it's very simple to implement and would allow a user to upload incredible amounts of data to all the key-servers.  

In theory it would be possible with the use of proxies and possibly tor to continually upload all kinds of illegal or sensitive data 24hrs a day accross all key-servers making it impossible to control or remove this data.

This is just a proof of concept and a discussion on the potential problems of key-servers in their current form!

DO NOT USE THIS TO DO ANYTHING ILLEGAL

### Notes

Why did i not use GPGME?  
Simply because it has some kind of memory leak which is only noticable when submitting 100s of UIDs into a PGP key, then it crashes after all memory has been eaten up. I do not know if this has been fixed in recent issues if it has then its possible to write the data to the PGP key much faster than the above python code is currently able to.
