import subprocess
import random
import string
import base64
import sys
import os

#check if input is a file
if os.path.exists(sys.argv[1]) != True:
	print "you typed something wrong, could not find that file"
else:
	file_to_upload = sys.argv[1]

#generate random data for credentials
user_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
email = ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + "@" + ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
passphrase = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
key_server = "eu.pool.sks-keyservers.net" #any key server is good as it will propogate world wide

#unattended key generation
p=subprocess.Popen('gpg2 --pinentry loopback --batch --passphrase ' + passphrase + ' --quick-gen-key "' + user_name + ' ' + email + '" rsa1024',shell=True,stdout=subprocess.PIPE)
out, err = p.communicate()

#get pub key
p=subprocess.Popen('gpg2 --list-key ' + email,shell=True,stdout=subprocess.PIPE)
out, err = p.communicate()

#do not upload again to the same key as this will mess up retreival of the file later
print email
key = out.split()[6] # parse out the key so we can use to send keys to the key servers

#open file in binary and break it up into 1305byte chunks
chunk_list = []
with open(file_to_upload, 'rb') as infile:
	while True:
		chunk = infile.read(1305)
		if not chunk: break
		chunk_list.append(chunk)

#encode binary chunks into base64 strings
i=0
for x in chunk_list:
	print len(base64.b64encode(x) + "\n")

	new_uid = str(i) + "@" + base64.b64encode(x)
	#below you need to use --batch  so you only have to type the password in once, could not get --passphrase to work for some reason
	p=subprocess.Popen("gpg2 --pinentry loopback --batch --passphrase " + passphrase + " --quick-add-uid "  + email + " " + new_uid,shell=True,stdout=subprocess.PIPE)
	out, err = p.communicate()
	i += 1

#finally send keys to a server
p=subprocess.Popen("gpg2 --keyserver " + key_server + " --send-keys " + key,shell=True,stdout=subprocess.PIPE)
out, err = p.communicate()
