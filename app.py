from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'my secret key'

# MySQL configuration
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'database user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'database password'
app.config['MYSQL_DATABASE_DB'] = 'database name'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# route main, index
@app.route("/")
@app.route("/index")
def main():
	conn = mysql.connect()
	cursor = conn.cursor()
	query = "SELECT * FROM user"
	cursor.execute(query)
	data = cursor.fetchall()
	return render_template('index.html', data = data)

# route signup
@app.route('/signup')
def signup():
	return render_template('signup.html')

# route dosignup
@app.route('/doSignup', methods=['POST'])
def doSignup():
	_name = request.form['name']
	_email = request.form['email']
	_password = request.form['password']
	_hashed_password = generate_password_hash(_password)
	_bio = request.form['bio']

	if (_name and _email and _hashed_password and _bio):
		conn = mysql.connect()
		cursor = conn.cursor()
		query = "INSERT INTO user (name, username, password, bio) VALUES(%s,%s, %s, %s)"
		parameter = (_name, _email, _hashed_password, _bio)
		cursor.execute(query, parameter)
		data = cursor.fetchall()
		if len(data) is 0:
			conn.commit()
			return json.dumps({'message':'User created successfully!'})
		else:
			return json.dumps({'message':str(data[0])})
	else:
		return json.dumps({'message':'Field must be fill in!'})

# route signin
@app.route('/signin')
def signin():
	return render_template('signin.html')

# route dosignin
@app.route('/doLogin', methods = ['POST'])
def doLogin():
	try:
		_username = request.form['username']
		_password = request.form['password']

		conn = mysql.connect()
		cursor = conn.cursor()
		query = "SELECT * FROM user WHERE username = %s"
		parameter = (_username)
		cursor.execute(query, parameter)
		data = cursor.fetchall()
		if len(data) > 0:
			if check_password_hash(str(data[0][3]), _password):
				session['user'] = data[0][0]
				return redirect('/home')
			else :
				return render_template('error.html', error = 'Wrong email address or password.')
		else :
			return render_template('error.html', error = 'Wrong email address or password.')
	except Exception, e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()
		conn.close()

# route home
@app.route('/home')
def home():
	if session.get('user'):
		return render_template('home.html')
	else:
		return render_template('error.html', error = 'Unauthorized Access')

# route logout
@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect('/')


# run application
if __name__ == "__main__":
	app.run()