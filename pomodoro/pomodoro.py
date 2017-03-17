import os
import httplib, urllib

beeminder_user = 'icole'
beeminder_goal = 'pomodoros'
beeminder_token = os.environ['BEEMINDER_AUTH_TOKEN']

def update_beeminder(amount):
    conn = httplib.HTTPSConnection("www.beeminder.com", 443)
    path = "/api/v1/users/{0}/goals/{1}/datapoints.json".format(beeminder_user, beeminder_goal)
    params = urllib.urlencode({'value': amount, 'auth_token': os.environ['BEEMINDER_AUTH_TOKEN']})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn.request("POST", path, params, headers)
    r = conn.getresponse()
    print(r.read())

update_beeminder(1)
