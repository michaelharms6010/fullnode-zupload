import subprocess
import time
import json

zaddrs = json.loads(subprocess.check_output("zcash-cli z_listaddresses", shell=True).strip())

recipients = []
for zaddr in zaddrs:
    recipients.append({
        "address": zaddr,
        "amount": 0.0003
    })

index = 0

for i in range(len(zaddrs)):
    zaddr = zaddrs[i]
    balance = float(subprocess.check_output("zcash-cli z_getbalance \"" + zaddr + "\"", shell=True).strip()) - 0.00001
    if balance >= 0.001:
        for tx in recipients:
            tx["amount"] = round(balance / float(len(zaddrs)),8) 
        new_tx_command = 'zcash-cli z_sendmany "' + zaddr + '" \'' + json.dumps(recipients) + '\' 1 0.00001'
        opid = subprocess.check_output(new_tx_command, shell=True).strip()
        print(opid)
        time.sleep(5)
        # send
    else:
        print("zero balance at " + zaddr)
    index  = (index + 1) % len(zaddrs)
