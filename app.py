from flask import Flask, jsonify

from backend.capital_one import get_recent_deposits, get_customer_information

app = Flask(__name__)





@app.route("/capital_one/recent_deposits")
def recent_deposits():
	return jsonify(results=get_recent_deposits())


@app.route("/capital_one/customer/<customer_id>")
def customer(customer_id):
	return jsonify(results=get_customer_information(customer_id))







if __name__ == "__main__":
	app.run(debug=True)
