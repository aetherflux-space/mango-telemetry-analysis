# How to do analysis on telemetry in Mongo

### First, get a local docker flat sat up and running.

In `config.toml` enable write_mongo


```
[fsw]
ip = "127.0.0.1"
tcp_port = 50239
udp_port = 2034

[logging]
write_logfile = true
logfile_path = "tlm.log"
write_stdout = false
write_mongo = true
write_state = false

[mongo]
ip = "127.0.0.1"
port = 27017
```


### Then, start a local mongo md server
I did this with:
```
brew services start mongodb-community
```

### Build with mango enabled 

`cargo build --features mongo`

### Connect to the server
Then you can connect 
```

from pymongo import MongoClient
from datetime import datetime
from pprint import pprint

try:
    client = MongoClient()
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

database = client['flatsat']
coll = database['tlm']
```

### And then grab the relevant telemetry 

```
r1 = coll.find_pandas_all({'mnemonic': 'OAR0_OSC_ACTMDL_RW'})
r2 = coll.find_pandas_all({'mnemonic': 'OAR1_OSC_ACTMDL_RW'})
r3 = coll.find_pandas_all({'mnemonic': 'OAR2_OSC_ACTMDL_RW'})
r4 = coll.find_pandas_all({'mnemonic': 'OAR3_OSC_ACTMDL_RW'})
```