# ATM 

1. start the server using : 
    fastapi dev main.py
2. the server run on port : 8000
3.  example of curl commands :

curl --location 'http://127.0.0.1:8000/atm/refill' \
--header 'Authorization: 12345' \
--header 'Content-Type: application/json' \
--data-raw '
{
"money":{
"200": 10
}
}'

curl --location 'http://127.0.0.1:8000/atm/withdrawal' \
--header 'Authorization: 12345' \
--header 'Content-Type: application/json' \
--data '{
"amount": 21.20
}'

4. following env properties can be change :
* MAX_WITHDRAW_AMOUNT=2000 # set the max withdraw value
* INIT_DB_FLAG=True # if set to false the DB will not be initiate when app is started default value is True.
* MAX_NUM_OF_COINS=50 # set the max coin allowed.

5. application is using embedded sqlite DB. atm.db will be created.