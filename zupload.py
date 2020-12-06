# Nothing to see here

import subprocess
import time
import json
import base64
import time
from datetime import datetime

def current_time():
    return int(time.mktime(datetime.today().timetuple()))



def get_new_zaddr_pair():
    new_zaddr = subprocess.check_output("zcash-cli z_getnewaddress", shell=True).strip()
    bash_command = 'zcash-cli z_exportviewingkey "' + new_zaddr + '"'
    view_key = subprocess.check_output(bash_command, shell=True)
    return [new_zaddr, view_key]

def get_current_opids():
    current_opids = json.loads(subprocess.check_output("zcash-cli z_listoperationids", shell=True).strip())
    return current_opids

def get_operation_status(opid):
    opid_command = "zcash-cli z_getoperationstatus '[\"" + opid + "\"]'"

    status = json.loads(subprocess.check_output(opid_command, shell=True).strip())

    if len(status) > 0:
        return status[0]
    else:
        return {}

def operation_succeeded(opid):
    status = get_operation_status(opid).get("status")
    return status == "success"

def operation_failed(opid):
    status = get_operation_status(opid).get("status")
    return status == "failed"

def operation_complete(opid):
    return operation_succeeded(opid) or operation_failed(opid)

def check_if_opids_done():
    current_opids = get_current_opids()
    for opid in current_opids:
        time.sleep(.05)
        if not operation_complete(opid):
            print opid + " in progress"
            return False

    return True

def clear_operations_from_memory():
    current_opids = get_current_opids()
    subprocess.check_output("zcash-cli z_getoperationresult '" + json.dumps(current_opids) + "'", shell=True).strip()

filename = str(input("Enter filename >>> "))

text = open(filename,"r") 

input_file = text.read()

input_file = base64.encodestring(input_file).strip() + ">]EOF]>\n"

chunks, chunk_size = len(input_file), 500
memos = [ input_file[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

memos.insert(0,filename + " - <blockheight> " + "- Lorem Ipsum Description" + ">]FILE]>")


zaddrs = json.loads(subprocess.check_output("zcash-cli z_listaddresses", shell=True).strip())

index = 0
zaddr_pair = get_new_zaddr_pair()
new_zaddr = zaddr_pair[0]
view_key = zaddr_pair[1]

count = 0
opid = None
start_time = current_time()
print("BEGINNING UPLOAD ***** --> ", filename)
print("View Key:", view_key)

while count < len(memos):
    zaddr = zaddrs[index]
    balance = float(subprocess.check_output("zcash-cli z_getbalance \"" + zaddr + "\"", shell=True).strip())
    current_opids = json.loads(subprocess.check_output("zcash-cli z_listoperationids", shell=True).strip())
    if balance >= 0.00001 and (len(current_opids) == 0 or check_if_opids_done()):
        if opid and operation_succeeded(opid):
            count += 1
            clear_operations_from_memory()
        # if fail, resend chunk, otherwise next chunk
        if count < len(memos):
            print(len(memos[count]))
            memo = (str(count) + "--:--" + memos[count]).encode("hex")
            print(memo)
            new_tx_command = 'zcash-cli z_sendmany "' + zaddr + '" ' + '\'[{"address": "'+ new_zaddr +'" ,"amount": 0.00000001, "memo": "' + memo + '" }]\' 1 0.00001'
            opid = subprocess.check_output(new_tx_command, shell=True).strip()
            print(opid + ", " + str(count+1) + " of " + str(len(memos)+1))
            print("Time elapsed: " + str(current_time() - start_time) + "s")
    time.sleep(5)
    index  = (index + 1) % len(zaddrs)


print(filename)
print("Upload is complete and waiting on final confirmation.")
print("upload time: " + str(current_time() - start_time) + "s" )

print("View Key:", view_key)
