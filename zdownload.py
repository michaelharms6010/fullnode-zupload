import subprocess
import time
import json
import base64 
import time
from datetime import datetime

def current_time():
    return int(time.mktime(datetime.today().timetuple()))
start_time = current_time()

vk = "zxviews1qdm7rk7tzcqqpqqk36hypakt0lgn9p2gmxt2q4jhga4ktw20rg2yw6mx3kuk6mry8fv7jzlr2mvu32eu3zyqh9gnhlkmkvz2vpysrhfma3ex845uh85c6cgdtnrsal6v0uqvuwgx94zq0dv5hytp0f7wwc3x9a3kyvhe083vgvcgqhghgwvgxdpm497zk3m94jqv3l0sdeyu25qtrqldydvq6a9htlyrtsl5my9v7s5q0pdedh7nlky9yp5lyj3grgzkpg8sjaz5qls2pqss7"


def get_transactions_for_address(zaddr):
    zaddr = zaddr.replace(" ", "")
    get_transactions_command = 'zcash-cli z_listreceivedbyaddress "' + zaddr + '"'
    transactions = json.loads(subprocess.check_output(get_transactions_command, shell=True).strip())
    print(transactions)
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
    
    transactions = get_transactions_for_address("zs179k8pwql9q e2k2r8fy0ur56 j3e02dqnzndq6 47wc9xh3kvn5c 5nc688jqz92ua vj073zzvef2yc")
    metadata = transactions.pop(0)['memo'].decode("hex")
    print(metadata)
    filename = metadata.split(" ")[0]
    file_as_base64 = ""
    eof = False
    for tx in transactions:
        if not eof:
            memo = tx['memo'].decode("hex")
            file_as_base64 += memo
        if ">]EOF]>" in memo:
            eof = True
        print(memo)
    
    memo = memo.replace(">]EOF]>", "")

    with open(filename, "wb") as f:
        f.write(memo.decode("base64"))



fetch_file(vk)
    



def import_view_key(view_key, rescan_height=1066000):
    if not view_key:
        return
    import_command = 'zcash-cli z_importviewingkey "' + view_key + '" whenkeyisnew ' + str(rescan_height)
    import_result = json.loads(subprocess.check_output(import_command, shell=True).strip())
    print(import_result)
    return import_result

