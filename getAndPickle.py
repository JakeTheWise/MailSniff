from apiclient import discovery
from apiclient.http import BatchHttpRequest
from httplib2 import Http
from oauth2client import file, client, tools
from ticktock import tick, tock
import pickle

'''Authorizes and sends a query to the Gmail API 
for all messages with query parameter ut-lists.
Stores results as a list of the raw message responses in a pickle file 'messages.p'.
'''
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flags = tools.argparser.parse_args(args=[])
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
MSGS = GMAIL.users().messages()
tick()
msgList = []
response = MSGS.list(userId='me', q='ut-lists').execute()
if 'messages' in response:
    msgList.extend(response['messages'])

while 'nextPageToken' in response:
    token = response['nextPageToken']
    response = MSGS.list(userId='me', q='ut-lists', pageToken=token).execute()
    msgList.extend(response['messages'])

tock('getMessages')
# batch = BatchHttpRequest()
# for msg in messages:
#     batch.add(GMAIL.users().messages().get(userId = 'me', id = msg['id']), callback = callback)
# batch.execute()
# tock('execute batch')
count = 0
rawMessages = []
tick()
for msg in msgList:
    rawMessages.append(MSGS.get(userId='me', id=msg['id']).execute())
    count += 1
    if count % 2000 == 0:
        print(float(count)/len(msgList))
pickle.dump(rawMessages, open("messages.p", "wb"))
tock('DONE')