Demo API             
=========

`RESTful API that allows users to insert, update and retreive data via HTTP methods POST, PUT, and GET.`             

## Table of Contents
1. [Installation](#installation)
2. [Assumptions](#assumptions)
3. [URL Examples](#url-examples)
4. [Python Requests Examples](#python-requests-examples)
5. [Testing](#testing)

## Installation
***
#### Python Virtual Environment Installation        
`(Note) if you already have virtualenv installed you can skip this first step`
```
$ pip install virtualenv
```
`create a project directory and then change working directory to it`
```
$ mkdir demo && cd demo  
```
`create a virtual environment by running`
```
$ python -m venv demo_env
```
`you then need to activate the virtual environment`  
```
$ source demo_env/bin/activate 
```
`you can then clone the API project from github`         
```
$ git clone https://github.com/foster-b/bf1122.git           
```
`change to directory bf1122`
```
$ cd bf1122
```
`install the dependencies`          
```
$ pip install -r requirements.txt
```
`to start running the API in the virtual environment use the following command`
```
$ python app.py
```

#### `Using Docker`
`clone the API project from github`
```
$ git clone https://github.com/foster-b/bf1122.git`
```
`change to directory bf1122`
```
$ cd bf1122
```
`build the docker image`
```
$ docker build -t demo_api .
```
`run the container`
```
$ docker run -d -p 5000:5000 -rm demo_api
```

### `Assumptions`

1. `dates will be entered in the format mm/dd/yy`      
2. `all dates will be in the 21st century`     
3. `since this is for internal testing and users would be verified when logging into company's system, there is no need to authentication or    authorization. Therefore headers will not require an API key.`         
4. `users will use the API responsibly. there won't be users spamming or excessively calling the API, no denial-of-service (DoS) attacks. without this assumption I would want to implement rate-limiting the API`
5. `there are two holidays July 4th and Labor Day`

### `URL Format`
***
`http://{host}:{port}/api/{version}/{resource}?{parameters}`

| `Name` | `Type` | `Value` |
|:----: | :---- | :---- |
| <sub>`host`</sub>| <sub>`domain name or ip address of the host that serves the API`</sub> | <sub>`in this demo it will be localhost` </sub> |
| <sub>`port`</sub> | <sub>`port number that can accept http connections`</sub> | <sub>`this demo uses 5000`</sub> |
| <sub>`version`</sub> | <sub>`breaking changes made to API (change in format of the response data for a call, change in response type, etc.) will be given a new version number,  non-breaking changes (adding new endpoints, etc.) will be given a new release number`</sub> | <sub>`new version: v1.0 -> v2.0, new release v2.2 -> v2.3`</sub> |
| <sub>`resource`</sub> | <sub>`entity whose data will be queried, updated, inserted. (in this demo data they are in-memory)` </sub> | <sub>`inventory, rental_cost, rental_agreement`</sub> |  
| <sub>`parameters`</sub> | <sub>`data to be sent in request` </sub> | <sub>`for `**`inventory`** `it is an optional tool_code,` **`rental_cost`** `it is required tool_type and for` **`rental_agreement`** `it is required tool_code, rental_days, checkout_date and discount_percent`</sub> |

### `URL Examples:`
##### `retreiving data about tool code CHNS`    
```
http://127.0.0.1:5000/api/v1.0/inventory
```
##### `getting a rental agreement for tool code CHNS, to be rented 30 days, starting 12/01/22 with a 5 percent discount`    
```
http:127.0.0.1:5000/api/v1.0/rental_agreement?tool_code=CHNS&rental_days=30&checkout_date=12/01/22&discount_percent=5
```

### `Python Requests Examples`     
#### `Inventory`

| `HTML Method` | `Endpoint` | `Description` |
|:----: | :---- | :---- |
| <sub>`GET`</sub> | <sub>`/api/v1.0/inventory`</sub> | <sub>`get information from all inventory` </sub> |
| <sub>`GET`</sub> | <sub>`/api/v1.0/inventory/<tool_code>`</sub> | <sub>`get information for specific tool`</sub> |
| <sub>`POST`</sub> | <sub>`/api/v1.0/inventory/<tool_code>`</sub> | <sub>`add tool information for new tool_code`</sub> |
| <sub>`PUT`</sub> | <sub>`/api/v1.0/inventory/<tool_code>`</sub> | <sub>`update information for existing tool`</sub> |  

#### `Examples:`
##### `retrieving data about tool code CHNS`
```python
import requests
url = "http://127.0.0.1:5000/api/v1.0/inventory/CHNS"
headers = {'Content-type': 'application/json'}
r = requests.get(url, headers=headers)
print(r.response)
print(r.json())
```
##### `adding tool code LADX to inventory`  
```python
import requests
url = "http://127.0.0.1:5000/api/v1.0/inventory/LADX"
headers = {'Content-type': 'application/json'}
payload = {"tool_type": "ladder", "brand": "Little Giant"}
r = requests.post(url, params=payload, headers=headers)
print(r.response)
print(r.json())
```
#### `Rental Costs`
| `HTML` | `Endpoint` | `Description` |
|:----: | :---- | :---- |
| <sub>`GET`</sub> | <sub>`/api/v1.0/rental_cost/<tool_type>`</sub> | <sub>`get charge info for a tool type`</sub> |
| <sub>`POST`</sub> | <sub>`/api/v1.0/rental_cost/<tool_type>`</sub> | <sub>`add new tool type charges`</sub> |
| <sub>`PUT`</sub> | <sub>`/api/v1.0/rental_cost/<tool_type>`</sub> | <sub>`update charge info for existing tool`</sub> |

#### `Examples:`      
##### `retrieving rental cost for tool type chainsaw`
```python
import requests 
url = "http://127.0.0.1:5000/api/v1.0/rental_cost/chainsaw"
headers = {'Content-type': 'application/json'}
r = requests.get(url, headers=headers)
print(r.response)
print(r.json())
```
##### `adding rental costs for ladder:`              
```python
import requests
url = "http://127.0.0.1:5000/api/v1.0/rental_cost/ladder"
headers = {'Content-type': 'application/json'}
payload = {"daily": 2.99, "weekday": "Yes", "weekend": "Yes", "Holiday": "No"}
r = requests.post(url, params=payload, headers=headers)
print(r.response)
print(r.json())
```

#### `Rental Agreement`
| `HTML` | `Endpoint` | `Description` |
|:----: | :---- | :---- |
| <sub>`GET`</sub> | <sub>`/api/v1.0/rental_agreement?<tool_code>&<rental_days>&<checkout_date>&<discount_percent>`</sub> | <sub>`return rental agreement information`</sub> |

#### `Example:`    
###### `getting a rental agreement for tool code CHNS, to be rented 30 days, starting 12/01/22 with a 5 percent discount`      
```python
import requests
headers = {'Content-type': 'application/json'}
url="http://0.0.0.0:5000/api/v1.0/rental_agreement"
payload={"tool_code": 'CHNS',"rental_days": 300, "checkout_date": '12/01/22', "discount_percent": 5}
print('generating rental agreement', payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(r.json())
print()
```        

###### `Example of Response from /api/v1.0/rental_agreement`
```json
<Response [200]>
{
    "Charge Days": 21,
    "Check Out Date": "12/01/22",
    "Daily Rental Charge": 1.49,
    "Discount Amount": "$1.56",
    "Discount Percent": "5%",
    "Due Date": "12/31/22",
    "Final Charge": "$29.73",
    "Pre-Discount Charge": "$31.29",
    "Rental Days": "30",
    "Tool Brand": "Stihl",
    "Tool Code": "CHNS",
    "Tool Type": "chainsaw"
}
```

#### `Errors`

`Conventional HTTP response codes are used to indicate if the API request was a success or a failure. 2xx range indicates success. 4xx indicates error (a required parameter is missing, etc.)`

| `HTTP` | `Status Codes` |
| :----: | :----: |
| `200` | `OK` |
| `201` | `Created` |
| `400` | `Bad Request (usually a required parameter is missing)` |
| `404` | `Requested resource doesn't exist` |

`Errors will also be thrown for rental days entered that isn't at least 1. And for discount percentages greater than 100.`

#### `Testing`

`after you have the API running you can use the *testing.py* script to test it.`
