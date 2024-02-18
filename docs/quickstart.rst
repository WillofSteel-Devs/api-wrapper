Quick Start
~~~~~~~~~~~

**Creating a Client**

To create a client to interact with the API with, you can use the
followning code:

.. code:: py

   import willofsteel

   API_KEY = 'Place your api key here'

   client = willofsteel.Client(API_KEY)

**Example**

A quick example of using this library is to look up your profile every
hour and send the results to a text file, this can be accomplished with
the following:

.. code:: py

   import willofsteel
   import time

   API_KEY = 'Place your api key here'
   client = willofsteel.Client(API_KEY)


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