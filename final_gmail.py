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
import sys
import csv
from email.mime.text import MIMEText



class gmail_api:
	def __init__(self):
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
	    self.service = build('gmail', 'v1', credentials=creds)
	    #return service
	def list_message(self,l_userId="me", l_maxResults=50, l_labelIds=['INBOX'], l_includeSpamTrash=None, l_pageToken=None, l_q=None, l_x__xgafv=None):
		results = self.service.users().messages().list(userId=l_userId, maxResults=l_maxResults, labelIds=l_labelIds,q=l_q).execute()
		return results
	def read_message(self,list_res):
		
		pass
	def send_mail(self):
		pass
	def make_message(self):
		pass
	def base64_ut8(self):
		pass

def check_avail():
	pass
def ret_avail():
	pass
a = gmail_api()
msg_ids = a.list_message(l_q = "No Reply <no-reply@ifttt.com> is:unread")
