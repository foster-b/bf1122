import requests, json
print()
print()
print()
print()
print("+++++++++++++++++++++++++++++STARTING NEW++++++++++++++++++++++++++++++++++++++")
print()

headers = {"Content-Type": "application/json"}

url = "http://0.0.0.0:5000/api/v1.0/inventory"
print("Returning Entire Inventory: GET "+url)

r = requests.get(url, headers=headers)

print(r)
print(json.dumps(r.json(), indent=4))
print()

url = "http://0.0.0.0:5000/api/v1.0/inventory/CHNS"
print('Testing returning information for specific tool code: GET'+url)

r = requests.get(url, headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

url = "http://0.0.0.0:5000/api/v1.0/inventory/LADX"

payload = {"tool_type": "ladder", "brand": "Little Giant"}

print('adding a new tool code', url, payload)

r = requests.post(url, params=payload, headers=headers)

print(r)
print(json.dumps(r.json(), indent=4))
print()

url = "http://0.0.0.0:5000/api/v1.0/rental_cost/ladder"
payload = {"daily": '2.99', "weekday": 'Yes', "weekend": 'Yes', "holiday": 'No'}

print('return rental costs associated with ladder', url, payload)

r = requests.get(url, params=payload, headers=headers)

print(r)
print(json.dumps(r.json(), indent=4))
print()

url="http://0.0.0.0:5000/api/v1.0/inventory/HMMR"
payload = { "tool_type": "hammer", "brand": "Black & Decker"}

print()
print('Adding HMMR to inventory', url, payload)
r = requests.post(url, params=payload, headers=headers)

print(r)
print(json.dumps(r.json(), indent=4))
print()
print()

url="http://0.0.0.0:5000/api/v1.0/rental_cost/hammer"

payload = {"daily": 17.99, "weekday": False, "weekend": True, "holiday": True}

print('adding hammer to rental costs', url, payload)

r = requests.post(url, params=payload, headers=headers)

print(r)
print(json.dumps(r.json(), indent=4))
print()

url="http://0.0.0.0:5000/api/v1.0/rental_cost/shovel"

payload = {"daily": 2.99, "weekday": 'Yes', "weekend": 'Yes', "holiday": 'No'}

print("check correct error returned for tool type doesn't exist in rental_cost", url, payload)

r = requests.put(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

# updating cost of tool type

url="http://0.0.0.0:5000/api/v1.0/rental_cost/ladder"

payload = {"daily": 2.99, "weekday": 'Yes', "weekend": 'Yes', "holiday": 'No'}

print('updating cost for a ladder', url, payload)
r = requests.put(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

url="http://0.0.0.0:5000/api/v1.0/rental_agreement"
payload={"tool_code": 'CHNS',"rental_days": 300, "checkout_date": '09/01/22', "discount_percent": 101}
print('Generating rental agreement w/ discount percent greater than 100', payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

url="http://0.0.0.0:5000/api/v1.0/rental_agreement"
payload={"tool_code": 'CHNS',"rental_days": 0, "checkout_date": '09/01/22', "discount_percent": 0}
print('Generating rental agreement w/ 0 rental days', payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

# generate rental agreement

url="http://0.0.0.0:5000/api/v1.0/rental_agreement"
payload={"tool_code": 'LADX',"rental_days": 300, "checkout_date": '12/01/22', "discount_percent": 5}
print('generating rental agreement', payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

# update to include holidays for ladder
url="http://0.0.0.0:5000/api/v1.0/rental_cost/ladder"

payload = {"holiday": 'Yes'}
print('update to include holidays for ladder', payload)
r = requests.put(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

# check labor day
print('Checking to make sure Labor Day is accounted for')
print()
url="http://0.0.0.0:5000/api/v1.0/rental_cost/ladder"
r = requests.get(url, headers=headers)
print('holiday is yes for ladder')
print(json.dumps(r.json(), indent=4))
print()

url="http://0.0.0.0:5000/api/v1.0/rental_agreement"
payload={"tool_code": 'LADX',"rental_days": 90, "checkout_date": '08/01/22', "discount_percent": 5}
print(url, payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

print('TESTING EXAMPLES:')
payload={"tool_code": 'JAKR',"rental_days": 5, "checkout_date": '09/03/15', "discount_percent": 101}
print(payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

payload={"tool_code": 'LADW',"rental_days": 3, "checkout_date": '07/02/20', "discount_percent": 10}
print(payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

payload={"tool_code": 'CHNS',"rental_days": 5, "checkout_date": '07/02/15', "discount_percent": 25}
print(payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

payload={"tool_code": 'JAKD',"rental_days": 6, "checkout_date": '09/03/15', "discount_percent": 0}
print(payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

payload={"tool_code": 'JAKR',"rental_days": 9, "checkout_date": '07/02/15', "discount_percent": 0}
print(payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()

payload={"tool_code": 'LADL',"rental_days": 4, "checkout_date": '07/02/20', "discount_percent": 50}
print(payload)
r=requests.get(url, params=payload, headers=headers)
print(r)
print(json.dumps(r.json(), indent=4))
print()




