from flask_script import Manager

from app import app

manager = Manager(app)


@manager.command
def generate_sql_db():
	pass


if __name__ == '__main__':
	manager.run()
