# gpg test program
#
# This is just some nasty test code to add images automatically to a gpg pub key.
# Uses pexpect to interact with the shell.
# This does nothing alone its just an example, to use you need to write more code or
# add it to one of the existing programs in this repo.

import pexpect
import sys
import time

email = "fake@mail"
imagefile = '/usr/path/to/image/file.jpg'
child = pexpect.spawn('gpg --edit-key ' + email)
child.logfile = sys.stdout

child.expect('gpg>')
child.sendline('addphoto')
child.expect('Enter JPEG filename for photo ID: ')
child.sendline(imagefile)
child.expect('y+')
child.send('y\n')
child.expect('Is this photo correct (y/N/q)?')
child.send('y\n')
child.expect('gpg> ')
child.sendline('save')
child.expect (pexpect.EOF)
