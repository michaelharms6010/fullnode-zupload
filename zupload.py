# Nothing to see here

import subprocess
import time
import json
import base64

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
        if not operation_complete(opid):
            print opid + " in progress"
            return False
    return True

filename = input("Enter filename >>> ")

text = open(filename,"r") 

input_file = text.read()

input_file = base64.encodestring(input_file)

chunks, chunk_size = len(input_file), 500
memos = [ input_file[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

memos.insert(0,filename + " - <blockheight> " + "- Lorem Ipsum Description" + ">]FILE]>")
memos.append(">]EOF]>")

zaddrs = json.loads(subprocess.check_output("zcash-cli z_listaddresses", shell=True).strip())

index = 0
new_zaddr = "zs19zv8gmrc8uwa06xpc4dxehnu4vsfthndvu5xemqllwppgg36tvfmgje80990fpzc55jgs08ndmp"

count = 0
opid = None

while True:
    zaddr = zaddrs[index]
    balance = float(subprocess.check_output("zcash-cli z_getbalance \"" + zaddr + "\"", shell=True).strip())
    current_opids = json.loads(subprocess.check_output("zcash-cli z_listoperationids", shell=True).strip())
    if balance >= 0.00001 and (len(current_opids) == 0 or check_if_opids_done()):
        # if fail, resend chunk, otherwise next chunk
        if opid and operation_succeeded(opid):
            count += 1
        memo = memos[count].encode("hex")
        new_tx_command = 'zcash-cli z_sendmany "' + zaddr + '" ' + '\'[{"address": "'+ new_zaddr +'" ,"amount": 0, "memo": "' + memo + '" }]\' 1 0.00001'
        opid = subprocess.check_output(new_tx_command, shell=True).strip()
        print(opid + ", " + str(count))
    time.sleep(5)
    index  = (index + 1) % len(zaddrs)
