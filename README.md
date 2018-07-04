# Using PGP keyservers for decentralised file storage
    
### This is a proof of concept for educational use only!

WARNING: this may break easily and is intended for use only on linux, & only for educational purposes.  

So this basicly works because you can have a UID(email address) that is 2048 characters in your PGP key, and from what i understand an unlimited amount of UID's, perfect for dumping data on to the key-servers, Adding UID's is a slow process by hand so i automated it using python, so you could dump any kind of file on the key servers. with some simple modifactions you can dump plain text on to the key-servers containing any content you choose and watch it propogate through all the key-servers around the world. Once that has completed, the data is essentially impossible to be removed as said by the sks key-server creator him self [Kristian Fiskerstrand](https://blog.sumptuouscapital.com/2016/03/openpgp-certificates-can-not-be-deleted-from-keyservers/).

For example there is a copy of the GDPR uploaded to the key-servers, points if someone can find it!

I wrote this because i think this charactaristic of key-servers is actually dangerous, for example someone could upload leaked data and it would be spread around the world and accessible by anyone and unstoppable.

### Which Parts of the GDPR this might be effected by:  

I am not a lawyer and i advise always seeking legal advice as i am purly expressing my opinion of what i think and this maybe wrong.

__Article 17__ (Right to eraseure('right to be forgotten'))  

sections 1(b)/2  - the data subject withdraws consent on which the processing is based according to point (a) of Article 6(1), or
point (a) of Article 9(2), and where there is no other legal ground for the processing;  

1(d) -the personal data have been unlawfully processed;  

__Article 7(3)__ (Conditions for consent)  
[The data subject shall have the right to withdraw his or her consent at any time.....It shall be as easy to withdraw as to give consent.]  

I think theres more in the GDPR that could apply to PGP key servers, but i don't have alot of time to look through it at the moment, i will add more when i can. Also suggestions and pull requests with more information is welcome.  

__Notice:__ This Program is very slow to add data to the gpg pubkey so dont plan on super large files.  

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

### unpublished 

i wrote a version of this using OpenMPI to see what kind of scale this could be used on, its very simple to implement and would allow a user to upload incredible amounts of data to all the key-servers.  

In theory it would be possible with the use of proxys and possibly tor to continually upload leaked data 24hrs a day accross all key-servers making it impossible to control or remove this data.

This is just a proof of concept and a discussion on the potential problems of key-servers in their current form!

DO NOT USE THIS TO DO ANYTHING ILLEGAL

### ToDo

remove the use for pinentry by using no passwords, this is possible in GPGME.

### Notes

why did i not use GPGME?  
Simply because it has some kind of memory leak which is only noticable when submitting 100's of UID's into a PGP key, then it crashes after all memory has been eaten up. I do not know if this has been fixed in recent issues if it has then its possible to write the data to the PGP key much faster than the above python code is currently able to.  
