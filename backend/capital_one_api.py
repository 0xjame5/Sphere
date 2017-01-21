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
