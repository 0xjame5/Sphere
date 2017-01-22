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


def get_recent_deposits():
    # Requested content:
    # first/last name of person and customer id
    # date of transaction
    # amount transacted
    # is it a positive or negative

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

        results = filter_executed_deposits(results)
        print(results)

        for result in results:
            account_id = result["payee_id"]
            customer_id = get_customer_id(account_id)
            customer = get_customer_information(customer_id)
            result.update(customer)

        return results
    else:
        print("error")
        return []


def filter_executed_deposits(results):
    NUM_OF_RESULTS = 5
    new_results = []
    for result in results:
        if len(new_results) < NUM_OF_RESULTS:
            if result["status"] == "executed":
                new_results.append(result)
        else:
            break

    return new_results


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

    print(account_id)

    if response.status_code == 200:
        data = json.loads(response.content)
        return data["customer_id"]
    else:
        print("ERROR!")
        print(response.content)
        return 0
