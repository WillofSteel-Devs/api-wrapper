.. Will of Steel API Wrapper documentation master file, created by
   sphinx-quickstart on Fri Feb 16 20:57:09 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Will of Steel API
============================

Will of Steel API Wrapper is a modern, easy to use, Pythonic wrapper for the Will of Steel API.

**Features:**

- Mordern Pythonic API
- Easy to use with an object oriented design
- Optimised for both speed and memory


Installing
~~~~~~~~~~

**Python 3.8 or higher is required**

On windows, the library can be installed using the following command:

.. code:: py

   py -3 -m install willofsteel

On macOS/linux, use the following command:

::

   python3 pip install willofsteel

If desired, you can also clone the repository directly:

::

   git clone https://github.com/WillofSteel-Devs/api-wrapper

Using the library
~~~~~~~~~~~~~~~~~

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