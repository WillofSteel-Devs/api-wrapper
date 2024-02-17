Will of Steel API Wrapper
=========================

A modern, easy to use, Pythonic API wrapper for the Will of Steel API in Python.


### Installing

**Python 3.8 or higher is required**

On windows, the library can be installed using the following command:

```py
py -3 -m install willofsteel
```

On macOS/linux, use the following command:
```
python3 pip install willofsteel
```

If desired, you can also clone the repository directly:
```
git clone https://github.com/WillofSteel-Devs/api-wrapper
```


### Using the library


**Creating a Client**

To create a client to interact with the API with, you can use the followning code:
```py
import willofsteel

API_KEY = 'Place your api key here'

client = willofsteel.Wrapper(API_KEY)
```

**Example**

A quick example of using this library is to look up your profile every hour and send the results to a text file, this can be accomplished with the following:
```py
import willofsteel
import time

API_KEY = 'Place your api key here'
client = willofsteel.Wrapper(API_KEY)


def scheduled_query():

    # Querying the api for the api key holder's profile
    player = client.get_player()
    
    # Creating a file name to log the results with
    timestamp = time.asctime().replace(':', '_')

    # Logging results
    with open(f'{timestamp}.txt', 'x', encoding='utf-8') as f:
        f.write(player)
    
    print(f"Query made at {timestamp}")

while True:
    scheduled_query()
    time.sleep(3600)
```
