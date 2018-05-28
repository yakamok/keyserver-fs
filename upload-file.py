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
	if "." in sys.argv[1]:
		domain = sys.argv[1][sys.argv[1].index("."):]
	else:
		domain = ".com"

#generate random data for credentials
user_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
email = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) + "@" + ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + domain
passphrase = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
key_server = "eu.pool.sks-keyservers.net" #any key server is good as it will propogate world wide

#unattended key generation
p=subprocess.Popen('gpg2 --pinentry loopback --batch --passphrase ' + passphrase + ' --quick-gen-key "' + user_name + ' ' + email + '" rsa1024',shell=True,stdout=subprocess.PIPE)
out, err = p.communicate()

#get pub key
p=subprocess.Popen('gpg2 --list-key ' + email,shell=True,stdout=subprocess.PIPE)
out, err = p.communicate()

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

#remove keys when done as they are not needed anymore
p=subprocess.Popen("gpg --batch --yes --delete-secret-keys " + key + "&& gpg --batch --yes --delete-keys " + key,shell=True,stdout=subprocess.PIPE)
out, err = p.communicate()

if err == None:
	print "removing temp keys\n"
	print "It can take 3-10mins before your key appears on your chosen server\n"
	print "http://" + key_server + "/pks/lookup?search=" + email + "&op=index"
else:
	print "something went wrong try again"
