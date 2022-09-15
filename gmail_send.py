"""
This project aim to send a reply mail to my employer based on my availailabiliy
First one to reply will get available shift.
This project is designed to run on a raspberry pi server
"""
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from bs4 import BeautifulSoup
import re
import time
#import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
from email.mime.text import MIMEText
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
# list of days available and not available
days_true = ["Monday","Tuesday","Wednesday","Thursday"]
days_false = ["Friday","Saturday","Sunday"]
#
def check_send(msg_id):
	res = None
	done_ids =[]
	fl = open("send_id.txt",'r+b')
	#ids = fl.read()
	for lines in fl:
		done_ids.append(lines)
	#print(done_ids)
	if (msg_id+"\n") in done_ids:
		#print(msg_id)
		pass
	else:
		fl.write(msg_id+"\n")
		res = True
	fl.close()
	return res
def create_message(sender, to, subject, message_text,id,msg_id):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  #message['Thread-Index'] = id
  message["References"] = msg_id
  message["In-Reply-To"] = msg_id
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def check_avail(data):
	res =[]
	data = data.split("\n")
	for data_l in data:
		avail = ret_avail(data_l)
		if avail:
			res.append(avail)
	return res

def ret_avail(data):
	# This function check of date strings in the message and validate the available dates
	#print( data+"\n")
	for d_f in days_true:
		if d_f in data:
			print(data+"\n")
			return data
	for d_t in days_false:
		if d_t in data:
			return None
		
def send_message(service, user_id, message):
  """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
  message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
  print('Message Id: %s' % message['id'])
  return message
  #print('An error occurred: ')
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    #results = service.users().messages().list(userId='me',maxResults=100,labelIds = ['INBOX']).execute()
    while True:
	    results = service.users().messages().list(userId='me',maxResults=50,labelIds = ['INBOX']).execute()
	    print(results)
	    messages = results.get('messages', [])

	    if not messages:
	    	#print "No messages found."
		pass
	    else:
	    	print("Message snippets")
	    	for message in messages:
			msg1 = service.users().messages().get(userId='me', id=message['id']).execute()
			msg =  msg1["payload"];
			msg = (msg["headers"])
			for val in msg :
				if val["name"] == "From":
	    				if "CSRShifts" in (val["value"]):  # "CSRShifts"
						payld=msg1["payload"]
						mssg_parts = payld['parts'] # fetching the message parts
						part_one  = mssg_parts[0] # fetching first element of the part 
						part_body = part_one['body'] # fetching body of the message
						part_data = part_body['data'] # fetching data from the body
						#clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
						#clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
						#clean_two = base64.b64decode (bytes(clean_one.encode('UTF-8'))) # decoding from Base64 to UTF-8
						#soup = BeautifulSoup(clean_two , "lxml" )
						#mssg_body = soup.body()
						print(part_data)
						print("\n***********************\n")						
						clean_two =base64.b64decode(part_data)
						print(clean_two)

						message_to_send = check_avail(clean_two) # the message to send
						tosend = False # check if to send
						to_mail = None
						sub = None
						msg_id = None
						thread_index = None
						
						for i in msg:
							#print(i)
							if i["name"] == "Message-ID":
								msg_id = i
							elif i["name"] == "Subject":
								sub = i["value"]
							elif i["name"] == "From":
								#to_mail = i["value"]
								to_mail = "xyz@garda.com"
								#to_mail = "xyz@gmail.com"
							elif i["name"] == "Thread-Index":
								thread_index = i["value"]
						tosend = check_send(msg_id["value"])
						#print("body: ",message_to_send,"\nif to send: ",tosend,"\nsub: ",sub,"\nto mail",to_mail)
						if tosend and message_to_send:
							print("body: ",message_to_send,"\nif to send: ",tosend,"\nsub: ",sub,"\nto mail",to_mail)
							message_to_send = "i am available \n\r"+"from monday to thursday \n\r any station any time" #message_to_send[0]
							message_cr = create_message("xyz@gmail.com", to_mail, sub, message_to_send,thread_index,msg_id["value"])
							send_message(service,"me",message_cr)
						time.sleep(2)
			#print("\n**************************************************\n")
			#break
	    # Call the Gmail API
	    #get_mail = service.users().messages().list(userId='me', labelIds="174a488cb4a0d96b", q=None, pageToken=None, maxResults=10, includeSpamTrash=None).execute()
	    #print(get_mail)
if __name__ == '__main__':
    main()
