# cozytouchpy

Inspired and forked from the [biker91620](https://github.com/biker91620/cozypy) repository

Cozytouch python implementation

This API allows you to control Atlantic, Thermor and Sauter equipment via the Cozytouch bridge

Used to obtain information from the following sensors:

- Gateway
- Radiators
- Water heaters and other counters
- APC Heat Pump (Beta)

## Example

     from cozytouchpy import CozytouchClient
     
     username="my-username"
     password="my-password"
     
     client = CozytouchClient(username, password, 'atlantic_cozytouch')
     client.connect()
     setup = await client.async_get_setup() 
     for place in setup.places:  
         print(place.id)
