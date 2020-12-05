import subprocess
import time
import json
import base64 

funded_zaddr = "zs1lw6n36z0nsvahtae9kzv45j5esg062pchhuwcx3s4y22fltaxpxwkamwqsafxm2le786klunr9s"


def get_operation_status(opid)
    status = json.loads(subprocess.check_output("zcash-cli z_getoperationstatus '\"" + opid + "\"]'").strip())
    return status[0]

def operation_succeeded(opid)
    return get_operation_status(opid)["status"] == "success"


# file = input("enter the name of the file that you'd like to save and share via the zcash blockchain: ")
file = "targettext.txt"

text = open(file,"r") 

input_file = text.read()

input_file = base64.encodestring(input_file)

chunks, chunk_size = len(input_file), 500
memos = [ input_file[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
memos.append("-- END OF DATA --")

new_zaddr = subprocess.check_output("zcash-cli z_getnewaddress", shell=True).strip()
bash_command = 'zcash-cli z_exportviewingkey "' + new_zaddr + '"'
view_key = subprocess.check_output(bash_command, shell=True)
print(new_zaddr)
print(view_key)
print("After the sending completes, you can view your content using the viewing key: \n" + view_key)

count = 0
while count < len(memos):
    opid = False
    confirmed_balance = float(subprocess.check_output("zcash-cli z_getbalance \"" + funded_zaddr + "\"", shell=True).strip())
    print(confirmed_balance)

    while confirmed_balance < 0.00001:
        time.sleep(15)
        confirmed_balance = float(subprocess.check_output("zcash-cli z_getbalance \"" + funded_zaddr + "\"", shell=True).strip())
        print(confirmed_balance)

    memo_as_hex = memos[count].encode("hex")
     
    new_tx_command = 'zcash-cli z_sendmany "' + funded_zaddr + '" ' + '\'[{"address": "'+ new_zaddr +'" ,"amount": 0, "memo": "' + memo_as_hex + '"}]\' 1 0.00001'
    prev_opid = opid
    while prev_opid == opid:
        if not opid or operation_succeeded(opid):
            opid = subprocess.check_output(new_tx_command, shell=True)
        else:
            print("it looks like " + opid + " failed.")
            time.sleep(15)

    if "opid" in opid:
        print(opid)
        count += 1
        print("Sent tx " + str(count) + " of " + str(len(memos)))
        time.sleep(30)




x = subprocess.check_output("echo Hello World", shell=True)

print(x)