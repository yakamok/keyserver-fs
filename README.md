# keyserver-fs

### proof of concept on using pgp keyservers for file storage

Using Python to open a file in binary then break it up and convert to base64 then insert that into a pgp pubring as new uid's. Once uploaded to a keyserver its there forever and propogated to all other key servers, making this a simple decentralised file storage system.  

I wrote this because i believe that pgp keyservers are very dangerous because of their poor design, anyone can upload any kind of data to them without the option for removal or peer review. Key Base although i am not a fan, require you to sign up and create an account instead of a simple dumping ground for keys that have the potential to contain sensitive data.
