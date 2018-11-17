import requests  # install this package
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

state = {
    'john': 3000,
    'mary': 200,
    'joe': 0
}

@app.route('/authenticate/', methods=['GET', 'POST'])
def authenticate():
    data = request.get_json()
    source = data['source']
    target = data['target']
    value = data['value']

    if state[source] < value:
        return jsonify({'auth': 0})
    
    if not phone_auth():
        return jsonify({'auth': 0})
    
    state[source] -= value
    state[target] += value

    print(state)
    
    return jsonify({'auth': 1})

def phone_auth():
    return True



# def transform_id(api_id, t_name):
#     result = 0
#     url = 'http://api.reimaginebanking.com/customers?key={}'.format(api_id)
#     f_name, l_name = t_name.split(' ')

#     account_list = requests.get(url).json()
#     for n in range(account_list.len()):
#         if (account_list[n]['first_name'] == f_name) and (account_list[n]['first_name'] == l_name):
#             result = account_list[n]['_id']

#     return result

# def proceed_request(cus_id, api_id, payload_type, payload_accname, amount, points, transfer_id):

#     url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(cus_id, api_id)

#     # Create a Savings Account
#     if payload_type == 'Savings':
#         payload = {
#             "type": payload_type, 
#             "nickname": payload_accname,  
#             "rewards": points, 
#             "balance": amount,
#         }
#         response = requests.post(
#             url,
#             data=json.dumps(payload),
#             headers={'content-type': 'application/json'},
#          )
#         if response.status_code == 201:
#             return 'Account created'
#         else:
#             return 'Account creation failed')

#     # Make a Transfer
#     elif payload_type == 'Transfer':
#         payload = {
#             "type": payload_type,  
#             "nickname": payload_accname,  
#             "balance": amount,
#             "transfer": transfer_id,  # id of the receiving account
#         }
#         response = requests.post(
#             url,
#             data=json.dumps(payload),
#             headers={'content-type': 'application/json'},
#          )
#         if response.status_code == 202:
#             return 'Transfer executed'
#         else:
#             return 'Transfer failed'
#     else:
#         return 'Transfer request failed'

#     # Check the balance of an account
#     elif payload_type == 'Balance':
#         acc_details = requests.get(url).json()
#         for n in range(acc_details.len()):
#             if (acc_details[n]['nickname'] == payload_accname)):
#                 result = acc_details[n]['balance']
#                 return 'Current balance is '+result+' '+acc_details[n]['currency']
#         return 'Account balance is unavailable'
#     else:
#         return 'Request type not supported'

#     return 'Request failed'


# if __name__ == "__main__":

#     t_id = transform_id(key, t_name)
#     proceed_request(id, key, 'Savings', 'test', 10, 0, t_id) # Parameters taken from Alexa App


