import json

import requests

BASE_URL = "http://api.reimaginebanking.com/"
API_KEY = "1224760f0bb2413925135dbdb6e28aff"


# Helper function for function below this one
def get_checking_accounts(results):
	new_results = []

	for result in results:
		if result['type'] == 'Checking':
			new_results.append(result)

	return new_results


def get_list_of_checking_accounts():
	path_to_url = "{0}/enterprise/accounts?key={1}".format(BASE_URL, API_KEY)

	payload = {
		'type': "Checking"
	}
	response = requests.get(
		path_to_url,
		data=json.dumps(payload),
		headers={
			'content-type': 'application/json'
		},
	)

	data = json.loads(response.content)

	if response.status_code == 200:
		results = get_checking_accounts(data["results"])
		# return jsonify(checking_accounts=results)
		return results
	else:
		print("ERROR: Could not obtain data from CapitalOneApi")
		return []


def delete_all_non_checking_accounts():
	# http://api.reimaginebanking.com/enterprise/customers?key=1224760f0bb2413925135dbdb6e28aff

	path_to_url = "{0}/enterprise/accounts?key={1}".format(BASE_URL, API_KEY)

	response = requests.get(
		path_to_url,
		headers={
			'content-type': 'application/json'
		},
	)

	data = json.loads(response.content)
	if response.status_code == 200:
		results = data["results"]
		print(len(results))
		print(results)

	# print(len(results))

	# capital_one customer id

	# print(results)
	else:
		print("ERROR")

	# curl -X DELETE --header "Accept: application/json" "http://api.reimaginebanking.com/accounts/588381221756fc834d8eb749?key=1224760f0bb2413925135dbdb6e28aff"


def delete_account(account_id):
	path_to_url = "{0}/accounts/{1}?key={2}".format(
		BASE_URL, account_id, API_KEY
	)

	response = requests.delete(
		path_to_url,
		headers={
			'content-type': 'application/json'
		},
	)

	print(response.status_code)
	print(response.content)


def get_recent_deposits():
	NUM_OF_RESULTS = 10

	path_to_url = "{0}/enterprise/deposits?key={1}".format(
		BASE_URL, API_KEY
	)

	response = requests.get(
		path_to_url,
		headers={
			'content-type': 'application/json'
		},
	)

	if response.status_code == 200:
		data = json.loads(response.content)
		results = data["results"]

		return results[:NUM_OF_RESULTS]
	else:
		print("error")
		return []


def get_customer_information(customer_id):
	"""
	:param customer_id: the id of the customer w/ Capital One API
	:return: a dictionary with customer information
	"""

	path_to_url = "{0}/enterprise/customers/{1}?key={2}".format(
		BASE_URL, customer_id, API_KEY
	)

	response = requests.get(
		path_to_url,
		headers={
			'content-type': 'application/json'
		},
	)

	if response.status_code == 200:
		data = json.loads(response.content)
		return data

	else:
		print("error")
		return {}


def get_customer_id(account_id):
	"""
	Call API to get account information, then retrieve customer ID from there
	:param account_id:
	:return: returns the customer_id, required for customer_information
	"""

	# enterprise/accounts/56c66be6a73e492741507b39?key=1224760f0bb2413925135dbdb6e28aff

	path_to_url = "{0}/enterprise/accounts/{1}?key={2}".format(
		BASE_URL, account_id, API_KEY
	)

	response = requests.get(
		path_to_url,
		headers={
			'content-type': 'application/json'
		},
	)

	if response.content == 200:
		data = json.loads(response.content)
		return data["customer_id"]
	else:
		print("ERROR!")
		return 0
