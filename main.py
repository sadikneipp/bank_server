import requests
import json
import time
from flask import Flask, jsonify, request
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser

app = Flask(__name__)

state = {
    'john': {'balance': 3000, 'credit': 999, 'rewards': 1337},
    'mary': {'balance': 200, 'credit': 700, 'rewards': 500},
    'leonard': {'balance': 0, 'credit': 100, 'rewards': 1}
}
AUTH_THRESH = 60
auth = time.time() - 60

ip_alexa = '82.132.222.99'

#splitwise shit
session = {}
consumer_key = "8K5e87K3y5haqW8hmG6x6mbP8GeOwyFqoed01b6q"
consumer_secret = "pW2YnEoK7vuiNCyES5c6Rvj2iBo0z5xOaFfujm4L"
session['access_token'] = {'oauth_token': 'y5dvUvYXr5MO038WUBBpfCVKoYSMxHq7jQjHqGJG', 'oauth_token_secret': 'CyoxnwNMTi9sZ5BMD1ASl1r6e7Z9SRahLZq58lY6'}
sObj = Splitwise(consumer_key,
                         consumer_secret)
sObj.setAccessToken(session['access_token'])

def add_bill(cost=100.0):
    users = []
    group = sObj.getGroup(10204809)
    people = group.getMembers()

    expense = Expense()
    expense.setCost(str(cost))
    expense.setDescription("Capital One Transfer")
    # per_person = str(round(cost / len(people), 2))
    per_person = cost

    paying_user =sObj.getCurrentUser()
    paying_id = paying_user.getId()
    paying_expense_user = ExpenseUser()
    paying_expense_user.setId(paying_id)
    paying_expense_user.setPaidShare(str(cost))
    paying_expense_user.setOwedShare(per_person)
    users.append(paying_expense_user)


    for friend in people:
        id = friend.getId()
        if id == paying_id:
            continue
        user = ExpenseUser()
        user.setId(id)
        user.setPaidShare('0.0')
        user.setOwedShare(per_person)
        users.append(user)
        expense.setUsers(users)
        expense = sObj.createExpense(expense)
        print(expense.getId())

@app.route('/splitwise/', methods=['GET', 'POST'])
def splitwise():
    data = request.get_json()
    value = data['value']
    add_bill(int(value))

@app.route('/authenticate/', methods=['GET', 'POST'])
def authenticate():
    data = request.get_json()

    target = data['target']
    value = data['value']
    source = data['source']
    operation = data['operation']
    # Make a transfer
    if operation == 'transfer':
        if state[source]['balance'] < value:
            return jsonify({'auth': 0})

        if not phone_auth():
            return jsonify({'auth': 0})

        state[source]['balance'] -= value
        state[target]['balance'] += value

        print(state)
        global auth
        auth = -1
        return jsonify({'auth': 1})
    # Check users' current balance
    elif operation == 'balance':
        return jsonify({'value':state[source]['balance']})
    # Check users' credit score
    elif operation == 'credit_score':
        return jsonify({'value':state[source]['credit']})
    # Check users' reward score
    elif operation == 'reward_points':
        return jsonify({'value':state[source]['rewards']})

def phone_auth():
    delta = time.time() - auth
    print(delta)
    if delta <= AUTH_THRESH:
        return True
    
    return False

@app.route('/ping/', methods=['GET', 'POST', 'OPTIONS'])
def ping():
    ip_phone = request.remote_addr
    
    print('phone: ' + ip_phone)
    print('alexa: ' + ip_alexa)
    if ip_phone[:5] == ip_alexa[:5]:
        global auth
        auth = time.time()
    print(time.time() - auth)
    print('Pinged!')
    
    data = request.get_json()
    return 'pinged'

if __name__ == "__main__":
    app.run(host='0.0.0.0')

# sample operations if the API documentation had worked     

# def transform_id(api_id, t_name):
#     result = 0
#     url = 'http://api.reimaginebanking.com/customers?key={}'.format(api_id)
#     f_name, l_name = t_name.split(' ')

#     account_list = requests.get(url).json()
#     for n in range(account_list.len()):
#         if (account_list[n]['first_name'] == f_name) and (account_list[n]['first_name'] == l_name):
#             result = account_list[n]['_id']

#     return result

# def proceed_request(cus_id, api_id, payload_operation, payload_accname, amount, points, transfer_id):

#     url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(cus_id, api_id)

#     # Create a Savings Account
#     if payload_operation == 'Savings':
#         payload = {
#             "operation": payload_operation,
#             "nickname": payload_accname,
#             "rewards": points,
#             "balance": amount,
#         }
#         response = requests.post(
#             url,
#             data=json.dumps(payload),
#             headers={'content-operation': 'application/json'},
#          )
#         if response.status_code == 201:
#             return 'Account created'
#         else:
#             return 'Account creation failed')

#     # Make a Transfer
#     elif payload_operation == 'Transfer':
#         payload = {
#             "operation": payload_operation,
#             "nickname": payload_accname,
#             "balance": amount,
#             "transfer": transfer_id,  # id of the receiving account
#         }
#         response = requests.post(
#             url,
#             data=json.dumps(payload),
#             headers={'content-operation': 'application/json'},
#          )
#         if response.status_code == 202:
#             return 'Transfer executed'
#         else:
#             return 'Transfer failed'
#     else:
#         return 'Transfer request failed'

#     # Check the balance of an account
#     elif payload_operation == 'Balance':
#         acc_details = requests.get(url).json()
#         for n in range(acc_details.len()):
#             if (acc_details[n]['nickname'] == payload_accname)):
#                 result = acc_details[n]['balance']
#                 return 'Current balance is '+result+' '+acc_details[n]['currency']
#         return 'Account balance is unavailable'
#     else:
#         return 'Request operation not supported'

#     return 'Request failed'


# if __name__ == "__main__":

#     t_id = transform_id(key, t_name)
#     proceed_request(id, key, 'Savings', 'test', 10, 0, t_id) # Parameters taken from Alexa App

