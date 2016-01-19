import time # so we can use "sleep" to wait between actions
import RPi.GPIO as io # import the GPIO library we just installed but call it "io"
import httplib, urllib
import os

## set GPIO mode to BCM
## this takes GPIO number instead of pin number
io.setmode(io.BCM)
 
## enter the number of whatever GPIO pin you're using
desk_pin = 22 
 
## use the built-in pull-up resistor
io.setup(desk_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp
 
## initialize desk 
desk=0
standing_sec=0
standing_min=0
beeminder_user = 'icole'
beeminder_goal = 'standing'
beeminder_token = os.environ['BEEMINDER_AUTH_TOKEN']

## this loop will execute the if statement that is true
while True:
    ## if the switch is open
    if io.input(desk_pin):
        standing_sec+=1
        if (standing_sec / 60) > standing_min:
            standing_min = (standing_sec / 60)
            print("Standing for " + str(standing_min) + " minutes")
            conn = httplib.HTTPSConnection("www.beeminder.com", 443)
            path = "/api/v1/users/{0}/goals/{1}/datapoints.json".format(beeminder_user, beeminder_goal)
            params = urllib.urlencode({'value': 1, 'auth_token': os.environ['BEEMINDER_AUTH_TOKEN']})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            conn.request("POST", path, params, headers)
            r = conn.getresponse()
            print(r.read())
    else:
        standing_sec=0
        standing_min=0
    time.sleep(1)

