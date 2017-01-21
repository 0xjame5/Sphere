from flask_script import Manager

from app import app
from backend.capital_one_api import get_list_of_checking_accounts

manager = Manager(app)


@manager.command
def generate_sql_db():
	accounts = get_list_of_checking_accounts()

	print(accounts)
	# GENERATE_DB HERE

if __name__ == '__main__':
	manager.run()
