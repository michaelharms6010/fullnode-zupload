import subprocess
import time
import json
import base64 
import time
from datetime import datetime

def current_time():
    return int(time.mktime(datetime.today().timetuple()))
start_time = current_time()

vk = "zxviews1qdm7rk7t9gqqpqyzlksx9s8lwlmrdqhqpkpcy0xclzsy4rvzw0lz28szhv4d377uvc9rmtgdwxjsq5txmme65y0eltkmy6kjd9pp2r94lkfevyc7k6ap2w9gsdvsje57dapzumt7wf6zguh9mkwnj9y3l0megcyhez4ezer8h47aup2ad57w7fty2umr26s6hp32wu5paka0ms5rwjma7wk7wwkwk8svwpfwm58czhd535tdt776ce5mfns4t5gweem6h252a3cfmls07ha4p"


def get_transactions_for_address(zaddr):
    zaddr = zaddr.replace(" ", "")
    get_transactions_command = 'zcash-cli z_listreceivedbyaddress "' + zaddr + '"'
    transactions = json.loads(subprocess.check_output(get_transactions_command, shell=True).strip())
    print(transactions)
    transactions = sorted(transactions, key = lambda tx: int(tx["memo"].decode("hex").split("--:--")[0]))
    # should these transactions be explicitly storted by created_time?
    return transactions

def fetch_file(view_key, rescan_height=1066000):
    # should this eventually look for multiple files??
    # import key
    # when complete
        # get transactions
        # isolate base64 string
        # save ile
    # import_view_key(view_key, rescan_height)
    
    transactions = get_transactions_for_address("zs14stmn89xqa ht86hlkc5e76e en3lxqtptmefg qehygrga6447x mfreku5z0vkxz cfh23syyamvrs")
    metadata = transactions.pop(0)['memo'].decode("hex").split("--:--")[1]
    print(metadata)
    filename = metadata.split(" ")[0]
    file_as_base64 = ""
    eof = False
    for tx in transactions:
        if not eof:
            memo = tx['memo'].decode("hex").split("--:--")[1].replace(" ", "").replace("\n", "")
            file_as_base64 += memo
        if ">]EOF]>" in memo:
            eof = True
        print(memo)

    print file_as_base64
    
    file_as_base64 = file_as_base64.replace(">]EOF]>", "")

    with open(filename, "wb") as f:
        f.write(file_as_base64.decode("base64"))



fetch_file(vk)
    



def import_view_key(view_key, rescan_height=1066000):
    if not view_key:
        return
    import_command = 'zcash-cli z_importviewingkey "' + view_key + '" whenkeyisnew ' + str(rescan_height)
    import_result = json.loads(subprocess.check_output(import_command, shell=True).strip())
    print(import_result)
    return import_result

