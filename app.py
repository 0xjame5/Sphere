"""
Name: app.py
Description: Holds endpoints for our application.
"""

"""
TODO: Create an endpoint to transfer money
We need to pull this data and place it into a SQL database
"""

from flask import Flask, jsonify

from backend.capital_one_api import get_recent_deposits

app = Flask(__name__)

"""
@app.route("/capital_one/transfer_money/USER_ID"):
def transfer_money():
	call capital one API with both ID
"""
BASE_URL = "http://api.reimaginebanking.com/"
CUSTOMER_ID = ""
API_KEY = "1224760f0bb2413925135dbdb6e28aff"

#
# def get_checking_accounts(results):
# 	new_results = []
#
# 	for result in results:
# 		if result['type'] == 'Checking':
# 			new_results.append(result)
#
# 	return new_results


# @app.route("/capital_one/checking_accounts/")
# def get_list_of_checking_accounts():
# 	path_to_url = "{0}/enterprise/accounts?key={1}".format(BASE_URL, API_KEY)
#
# 	payload = {
# 		'type': "Checking"
# 	}
# 	response = requests.get(
# 		path_to_url,
# 		data=json.dumps(payload),
# 		headers={
# 			'content-type': 'application/json'
# 		},
# 	)
#
# 	data = json.loads(response.content)
#
# 	if response.status_code == 200:
# 		results = get_checking_accounts(data["results"])
# 		return jsonify(checking_accounts=results)
# 	else:
# 		return jsonify(success=False)


"""
WHAT DO WE NEED THE API TO DO?
WE NEED IT TO...:

Verify if a face exists and return the ID of the user

If not, we want to make the user upload to api and train the clarifai data
"""


""" CAPITAL ONE """
@app.route("/capital_one/recent_deposits")
def recent_deposits():
	return jsonify(results=get_recent_deposits())

# @app.route("/capital_one/customer")
# def customer():







if __name__ == "__main__":
	app.run(debug=True)
