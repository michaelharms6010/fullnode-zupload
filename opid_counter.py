# Nothing to see here

import subprocess
import time
import json

opids = json.loads(subprocess.check_output("zcash-cli z_listoperationids", shell=True).strip())

print len(opids)