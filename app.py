import os

from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

from backend.predict import predict

""" Flask application factory """

# Setup Flask app and app.config
app = Flask(__name__)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config[
	'SQLALCHEMY_DATABASE_URI'] = "postgres://umuyufhpqkxbfd:ab1220192cf8f53502d2f5eab4205ebb441dfa1c1500d66ef3e06633022ff105@ec2-54-163-246-165.compute-1.amazonaws.com:5432/dddq6l1q9nlmo6"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), index=True)
	password_hash = db.Column(db.String(128))

	first_name = db.Column(db.String(32))
	last_name = db.Column(db.String(32))
	face_username = db.Column(db.String(32))
	capital_one_id = db.Column(db.String(32))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=600):
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None  # valid token, but expired
		except BadSignature:
			return None  # invalid token
		user = User.query.get(data['id'])
		return user


@auth.verify_password
def verify_password(username_or_token, password):
	# first try to authenticate by token
	user = User.verify_auth_token(username_or_token)
	if not user:
		# try to authenticate with username/password
		user = User.query.filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True


@app.route('/api/users', methods=['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')

	first_name = request.json.get('first_name')
	last_name = request.json.get('last_name')

	if username is None or password is None:
		abort(400)  # missing arguments
	if User.query.filter_by(username=username).first() is not None:
		abort(400)  # existing user
	user = User(username=username)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return (jsonify({'username': user.username}), 201,
	        {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
	user = User.query.get(id)
	if not user:
		abort(400)
	return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token(600)
	return jsonify({'token': token.decode('ascii'), 'duration': 30000})


@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s!' % g.user.username})


from backend.capital_one import *


# TODO: Add more information from capital one id
# TODO: Add bank psuedo-information
@app.route('/api/profile')
@auth.login_required
def get_profile():
	return jsonify(
		username=g.user.username,
		first_name=g.user.first_name,
		last_name=g.user.last_name,
		account_id=g.user.capital_one_id,
		account_info=get_customer_info(g.user.capital_one_id),
		checking_account=get_account_data(
			get_checking_account(g.user.capital_one_id))

	)


@app.route('/api/deposit', methods=['POST'])
@auth.login_required
def deposit():
	amount = request.args.get('amount')
	account_id = request.args.get('account_id')

	if transfer_money(g.user.capital_one_id, account_id, amount):
		return jsonify(success=True)

	return jsonify(success=False)


@app.route('/api/compare', methods=['POST'])
@auth.login_required
def compare():
	print(request.data)
	base64 = request.data

	# print(base64)

	# ACCESS_KEY = "AKIAJT3KBLD2HWLCQ4DA"
	# SECRET_KEY = "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"
	# BUCKET_NAME = "sphere-flask"
	#
	# data_file = request.files['user-image']
	# file_name = data_file.filename
	#
	# conn = S3Connection(ACCESS_KEY, SECRET_KEY)
	# bucket = conn.get_bucket(BUCKET_NAME)
	#
	# k = Key(bucket)
	# k.key = file_name
	# #
	# data = "".join(data_file.readlines())
	# print(data)
	# k.set_contents_from_string(data)
	#
	# url = str(k.generate_url(expires_in=300))

	username = predict(base64)

	user = User.query.filter_by(username=username).first()

	data = {}

	print(user.capital_one_id)

	if user.capital_one_id != None:
		data = get_customer_info(user.capital_one_id)

	return jsonify(
		username=username,
		data=data

	)


@app.route("/api/account")
def account():
	pass


# return json.dumps({
# 	'data': presigned_post,
# 	'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
# })


@app.route("/capital_one/recent_deposits")
def recent_deposits():
	return jsonify(results=get_recent_deposits())


@app.route("/capital_one/customer/<customer_id>")
def customer(customer_id):
	return jsonify(results=get_customer_information(customer_id))


if __name__ == "__main__":

	if not os.path.exists('db.sqlite'):
		db.create_all()
	app.run(debug=True)
