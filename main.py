import requests  # install this package
import json
import time
from flask import Flask, jsonify, request


app = Flask(__name__)


AUTH_THRESH = 60
state = {
    'john': 3000,
    'mary': 200,
    'joe': 0
}

auth = time.time() - 70

@app.route('/authenticate/', methods=['GET', 'POST'])
def authenticate():
    data = request.get_json()
    source = data['source']
    target = data['target']
    value = data['value']

    if state[source] < value:
        print('no funds!')
        return jsonify({'auth': 0})
    
    if not phone_auth():
        print('no two factor')
        return jsonify({'auth': 0})
    
    state[source] -= value
    state[target] += value

    print(state)
    
    return jsonify({'auth': 1})

def phone_auth():
    delta = time.time() - auth
    print(delta)
    if delta <= AUTH_THRESH:
        return True
    
    return False

@app.route('/ping/', methods=['GET', 'POST', 'OPTIONS'])
def ping():
    global auth
    auth = time.time()
    print(time.time() - auth)
    print('Pinged!')
    return 'pinged'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
#     result = 0
#     url = 'http://api.reimaginebanking.com/customers?key={}'.format(api_id)
#     f_name, l_name = t_name.split(' ')

#     output = requests.get(url)
#     account_list = output.json()
#     for n in range(account_list.len()):
#         if (account_list[n]['first_name'] == f_name) and (account_list[n]['first_name'] == l_name):
#             result = account_list['_id']

#     return result

# def proceed_request(cus_id, api_id, payload_type, payload_accname, amount, points, transfer_id):

#     url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(cus_id, api_id)

#     # Create a Savings Account
#     if payload_type == 'Savings':
#         payload = {
#             "type": payload_type,  # types: transfer!, creation of new account,
#             "nickname": payload_accname,  # the name of the account being used
#             "rewards": points,  # reward points
#             "balance": amount,
#         }
#         response = requests.post(
#             url,
#             data=json.dumps(payload),
#             headers={'content-type': 'application/json'},
#          )
#         if response.status_code == 201:
#             print('Account created')
#         else:
#             print('Transfer Failed')

#     # Make a Transfer
#     elif payload_type == 'Transfer':
#         payload = {
#             "type": payload_type,  # types: transfer!, creation of new account,
#             "nickname": payload_accname,  # the name of the account being used
#             "balance": amount,
#             "transfer": transfer_id,  # id of the receiving account
#         }
#         response = requests.post(
#             url,
#             data=json.dumps(payload),
#             headers={'content-type': 'application/json'},
#          )
#         if response.status_code == 202:
#             print('Transfer Executed')
#         else:
#             print('Transfer Failed')
#     else:
#         return 0

#     return 0


# if __name__ == "__main__":  # only runs when this script is called directly as opposed to from another script

#     t_id = transform_id(key, t_name)
#     proceed_request(id, key, 'Savings', 'test', 10, 0, t_id)


