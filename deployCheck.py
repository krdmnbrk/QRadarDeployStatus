# -*-  coding: utf-8 -*-
# Author: Burak Karaduman <burak.karaduman@kocsistem.com.tr>
# Usage: python deployCheck.py


# Import libraries
import os
import re
import requests
import urllib3
urllib3.disable_warnings()

# Define color codes
green = "\x1b[1;32;40m"
red = "\x1b[1;31;40m"
yellow = "\x1b[1;33;40m"
bold='\x1b[01m'
resetColor = "\x1b[0m"

# Define your authorized token
# to create admin token https://www.ibm.com/support/knowledgecenter/en/SSKMKU/com.ibm.security_operations_app.doc/t_Qapps_Operations_authToken.html
TOKEN = "9b9bf8e9-12b3-484d-b108-a8b6fad063d8"

# If you run this script out of console CLI, you need to connection on port 443 to console. 
# Define your IP if it is not localhost
consoleIP = "localhost"

# Define API URLs
deploy_api_url = "https://{}/api/staged_config/deploy_status".format(consoleIP)


# Define get request function
def getFromAPI(URL):
    response = requests.get(URL, verify=False, headers={"SEC":TOKEN})
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)

def getDeployStatus():
    deploy = getFromAPI(deploy_api_url)
    hosts = deploy["hosts"]

    os.system("clear")
    print(bold + "DEPLOY STATUS\n" + resetColor)

    if len(hosts) > 0:
        for host in hosts:
            ip = host["ip"]
            status = host["status"]
            if status == "SUCCESS":
                color = green
            elif status == "IN_PROGRESS" or status == "INITIATING":
                color = yellow
            elif status == "TIMED_OUT" or status == "ERROR":
                color = red
            deployment_hosts_url = "https://{}/api/staged_config/deployment/hosts?filter=private_ip%3D%27{}%27".format(consoleIP,ip)
            hostname = getFromAPI(deployment_hosts_url)[0]["hostname"]
            print(color + "Hostname   = " + hostname + resetColor)
            print(color + "IP Address = " + ip + resetColor)
            print(color + "Status     = " + status + resetColor)
            print("-"*48)
    percent_complete = deploy["percent_complete"]
    initiated_from = deploy["initiated_from"]
    deploy_type = deploy["type"]
    initiated_by = deploy["initiated_by"]
    deployStatus = deploy["status"]



    print("""\033[1;37;40m
################################################
#                                              #
#       Percent Complete = %{}#
#       Type             = {}#
#       Initiated By     = {}#
#       Status           = {}#
#       Time             = {}#
#                                              #
################################################
\033[0m""".format(str(percent_complete).ljust(19," "),deploy_type.ljust(20," "),initiated_by.ljust(20," "),deployStatus.ljust(20," "),open("/opt/qradar/conf/lastDeployTime.conf","r").read().ljust(20," ")))

getDeployStatus()