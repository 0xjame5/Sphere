import os

from flask import Flask, jsonify, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter

from backend.capital_one import get_recent_deposits, get_customer_information

app = Flask(__name__)


# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
	# Flask settings
	SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')

	SQLALCHEMY_DATABASE_URI = os.getenv(
		'DATABASE_URL',
		'sqlite:///basic_app.sqlite'
	)
	CSRF_ENABLED = True

	USER_ENABLE_CONFIRM_EMAIL = False
	USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
	# Requires USER_ENABLE_EMAIL=True

	USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = True
	# Allow users to login without a
	# confirmed email address
	# Protect views using @confirm_email_required

	USER_ENABLE_EMAIL = False  # Register with Email
	# Requires USER_ENABLE_REGISTRATION=True


	# Flask-Mail settings
	MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'email@example.com')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'password')
	MAIL_DEFAULT_SENDER = os.getenv(
		'MAIL_DEFAULT_SENDER', '"MyApp" <noreply@example.com>'
	)
	MAIL_SERVER = os.getenv(
		'MAIL_SERVER', 'smtp.gmail.com'
	)
	MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
	MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))

	# Flask-User settings
	USER_APP_NAME = "AppName"  # Used by email templates


def create_app():
	""" Flask application factory """

	# Setup Flask app and app.config
	app = Flask(__name__)
	app.config.from_object(__name__ + '.ConfigClass')

	# Initialize Flask extensions
	db = SQLAlchemy(app)  # Initialize Flask-SQLAlchemy
	mail = Mail(app)  # Initialize Flask-Mail

	# Define the User data model. Make sure to add flask_user UserMixin !!!
	class User(db.Model, UserMixin):
		id = db.Column(db.Integer, primary_key=True)

		# User authentication information
		username = db.Column(db.String(50), nullable=False, unique=True)
		password = db.Column(db.String(255), nullable=False, server_default='')

		# User email information
		# email = db.Column(db.String(255), nullable=False, unique=True)
		confirmed_at = db.Column(db.DateTime())

		# User information
		active = db.Column(
			'is_active', db.Boolean(),
			nullable=False, server_default='0'
		)
		first_name = db.Column(
			db.String(100), nullable=False,
			server_default=''
		)
		last_name = db.Column(
			db.String(100), nullable=False, server_default=''
		)

	# Create all database tables
	db.create_all()

	# Setup Flask-User
	db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
	user_manager = UserManager(db_adapter, app)  # Initialize Flask-User

	@app.route("/capital_one/recent_deposits")
	def recent_deposits():
		return jsonify(results=get_recent_deposits())

	@app.route("/capital_one/customer/<customer_id>")
	def customer(customer_id):
		return jsonify(results=get_customer_information(customer_id))

	@app.route("/register", methods=["POST"])
	def register():
		username = request.args.get("username")
		email = request.args.get("email")
		password = request.args.get("password")

		print(username, email, password)

		"""
		Username
		Email
		Password

		:return:
		"""
		return jsonify(success=True)

	@app.route("/api/login/")
	def login():
		pass

	@app.route("/api/logout")
	def logout():
		pass

	return app


if __name__ == "__main__":
	app = create_app()

	app.run(debug=True)
