#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import requests
from xml.etree import ElementTree as et

if xldeployServer is None:
    print "No server provided."
    sys.exit(1)

print "Connected to your XL Deploy server: \n"

url = '%s/deployit/tasks/v2/current/all' % (xldeployServer['url'])
u = url.replace('@http://', "@") # fix bug where extra http:// is added to URL based on CI settings

print "Non archived tasks can be found at: ", u

r = requests.get(u, auth=(xldeployServer['username'], xldeployServer['password']))
#page = r.text
content = r.content
#print page
print "Retrieving tasks from XL Deploy: " + content + "\n"

tree = et.fromstring(content)
#print tree

#Get all tasks from repo

for elem in tree.findall('task'):
    #print "ELEMENT: ", elem
    d = elem.attrib #create python dictionary from tasks
    print "TASK INFO: ", elem.attrib

    for key, value in d.iteritems():
        #print key, value
        if key == 'state':
            if value == 'EXECUTED': #find the tasks in an Executed state

                archiveId = d['id']
                archiveState = d['state']
                archiveURL = '%s/deployit/tasks/v2/%s/archive' % (xldeployServer['url'], archiveId) #API URL to post to archive
                archiveU = archiveURL.replace('@http://', "@") # fix bug where extra http:// is added to URL based on CI setting
                r = requests.post(archiveU, auth=(xldeployServer['username'], xldeployServer['password'])) #Archive the tasks marked as EXECUTED

                #print archiveId

                print "Archiving a task with id %s because it's in the state %s!!\n" % (archiveId, archiveState)
            else:
                print "Nothing to Archive!!!\n"


