# Nothing to see here

zaddrs = json.loads(subprocess.check_output("zcash-cli z_getaddresses", shell=True).strip())

index = 0

while True:
    zaddr = zaddrs[index]
    balance = float(subprocess.check_output("zcash-cli z_getbalance \"" + zaddr + "\")", shell=true).strip())
    if balance >= 0.00001:
        new_tx_command = 'zcash-cli z_sendmany "' + funded_zaddr + '" ' + '\'[{"address": "'+ new_zaddr +'" ,"amount": 0, "memo": "' + memo_as_hex + '"}]\' 1 0.00001'
        opid = subprocess.check_output(new_tx_command, shell=True).strip()
        time.sleep(5)
        # send
    else:
        print("zero balance at " + zaddr)
    index  = (index + 1) % len(zaddrs)
