import subprocess
import random
import string
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
		domain = ""

keyservaddr = "add valid key server here"

def parse_n_upload(upload_file):
	#generate random data for credentials
	user_name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
	email = ''.join(random.choice(string.ascii_uppercase) for _ in range(10)) + "@" +\
			''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + domain

	passphrase = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
	key_server = keyservaddr #any key server is good as it will propogate world wide

	#unattended key generation
	p=subprocess.Popen('gpg2 --batch --pinentry-mode=loopback --passphrase ' + passphrase +\
						' --quick-gen-key "' + user_name + ' ' + email + '" rsa1024', shell=True,\
						stdout=subprocess.PIPE)

	out, err = p.communicate()

	#get pub key
	p=subprocess.Popen("gpg2 --list-key --with-colons " + email, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	# parse out the key id so we can use it to send keys to the key servers
	key = key = [x.replace(':', '').replace('fpr', '') for x in out.split() if "fpr" in x][0] 

	#read file and add it to the gpg key as plain text
	with open(upload_file, 'r') as infile:
		for x in infile.readlines():
			if x:
				print x
				p=subprocess.Popen("gpg2 --batch --pinentry-mode=loopback --passphrase " + passphrase +\
								" --quick-add-uid "  + email + " " + '"' + x + '"', shell=True, stdout=subprocess.PIPE)
				out, err = p.communicate()
				print "key added"
			else:
				print "empty string ignoring"


	#finally send keys to a server
	p=subprocess.Popen("torsocks gpg2 --keyserver " + key_server + " --send-keys " +\
						key, shell=True, stdout=subprocess.PIPE)
	out, err = p.communicate()
	if err:
		print "something went wrong with sending"

	#remove keys when done as they are not needed anymore
	p=subprocess.Popen("gpg --batch --yes --delete-secret-keys " + key +\
				"&& gpg --batch --yes --delete-keys " + key, shell=True, stdout=subprocess.PIPE)

	if err == None:
		print "removing temp keys\n"
		print "It can take 3-10mins before your key appears on your chosen server\n"
		print "http://" + key_server + "/pks/lookup?search=" + email + "&op=index"
	else:
		print "something went wrong try again"

parse_n_upload(file_to_upload)
