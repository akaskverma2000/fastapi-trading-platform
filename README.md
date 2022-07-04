# SteelEye-API-Developer-Assessment

Descrption - I created this REST API for SteelEye's technical test to retrieve all trades, trades by id, and some complex search filters from the trade database. Additionally, I included the pagination and sorting features.

## Installation
```console
$ pipenv shell --python 3.8
$ pipenv install fastapi==0.68.1
$ pipenv install uvicorn==0.15.0
$ pipenv install fastapi-pagination
```

## Run it
Run the server with:

```console
$ python app.py

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
I'm using FASTAPI Swagger documentation to demonstrate the rest API I have created for this assessment.

![image](https://user-images.githubusercontent.com/63094947/177128207-d55a33f6-cacb-4e83-9252-ed311d6866bf.png)


## Fetch All Trades
I have added the endpoint URL `/trades/` to get all the trades stored in the database. I have return the array of dictonary where I have stored the details of a trade.

![image](https://user-images.githubusercontent.com/63094947/177128093-ceaebb97-e50e-43bd-b78e-03c7d360d8d2.png)

## Fetch A Single Trade by Trade Id
I have added the endpoint URL `/trades/{trade_id}` to get a trade which is equal to the Trade ID stored in the Trade Database. From this, I have run a for-loop to get the trade which has the same trade id which given in the query parameter and return that particular trade in the form of dictionary.

![image](https://user-images.githubusercontent.com/63094947/177128911-7ab3e5a9-07fa-4d86-89d5-3e26f026d67f.png)

## Fetch All Trades where it's matches with the search parameter 
I have added the endpoint URL `/trade` to get all those trades where the search query paramter gets is equal to the counterparty, instrumentId, instrumentName and trader stored in the Trade database. From this, I have run a for-loop to get all those trades where atleast one of the values in the trade details get matches with the search paramter given in the query parameter and return all those trades in the form of list of dictionary.

![image](https://user-images.githubusercontent.com/63094947/177130368-76de6212-388b-47d4-b2a9-5af7e1d75d3f.png)

## Fetch All Trades by Advanced Filtering 
I have added the endpoint URL `/trades` to get all those trades where it matches with the exact value sent in the query paramter from the Trade database. I have loop through all the trade in the trades dictonary. Everytime loop run, I have wriiten a condition when it's come under the constraints which is given in the query parameter then only it is going to add that trade into the result and return all those trades in the form of list of dictionary.

![image](https://user-images.githubusercontent.com/63094947/177132104-3854395a-a202-4617-a148-65aebdb94eb4.png)

![image](https://user-images.githubusercontent.com/63094947/177131438-0b2e827f-8e21-49b6-ae97-2da966595534.png)

## Pagination Functionality 
For this, I have used inbuilt library given in the fastapi. They have created a function call `/add_pagiantion/` which will allow the pagination functionality. After that, whenever I have to return the list of dictionary. I have added `/paginate/` function to it.

## Sorting Functionality 
I have created a enum class. So that user can easily select the order in which they want to sort the data. I have used `/sorted/` library given in the python to sort the list of dictionary according to the parameter given from the user. 

![image](https://user-images.githubusercontent.com/63094947/177134888-7815aa42-a46a-49a1-ab26-9a569388abca.png)
![image](https://user-images.githubusercontent.com/63094947/177134799-48ae8b00-8f30-4fa1-88f7-f309e3dc55a2.png)

## Dependencies
<code>uvicorn</code> - for the server that loads and serves your application.
<code>fastapi_pagination</code> - to add pagination functionality.


