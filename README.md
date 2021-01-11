# fullnode-zupload
File sharing via Zcash view key. Splits binary into base64 chunks, stores files to ZEC blockchain in ~500 byte chunks. 

Everything is in `zupload.py` and `zdownload.py` - Configure them for the right address and you should be set to go.

Zupload.py circumvents waiting for change confirmation by rotating through all wallet addresses - it waits for operations to succeed before moving on to the next address, next operation.

There are some helpers related to the wallet fund distribution scheme that lets me bypass change confirmation. There are also some goober data flies I was using to test uploads.
