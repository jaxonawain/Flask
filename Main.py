import Session, uuid, datetime, yaml
from flask import Flask, request, render_template
app = Flask(__name__)


def validate_session():
    # Validate against IP, need to include functionality to pair with username once authentication in place
    headers = {'ip': request.remote_addr,
               'agent': request.headers.get('User-Agent')}
    sessionObj = Session.Session(headers)
    if sessionObj.validate_session():
        return True
    else:
        return False


@app.route('/')
def home():
    if validate_session():
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=["POST", "GET"])
def login_page():
    return render_template('login.html')


@app.route('/auth', methods=["POST"])
def auth():
    headers = {'username': request.form['username'],
               'secret': request.form['secret']}
    sessionObj = Session.Session(headers)
    if sessionObj.validate_login():
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/account_creation', methods=['POST'])
def create_account():
    headers = {'username': request.form['username'],
               'secret': request.form['secret'],
               'first_name': request.form['first_name'],
               'last_name': request.form['last_name']}
    sessionObj = Session.Session(headers)
    sessionObj.create_user()
    return render_template('login.html')


@app.route('/session_creation')
def create_session():
    # Create session in session table. Need to call with authentication script. Need to automatically remove from
    # table too.
    headers = {'ip': request.remote_addr,
               'agent': request.headers.get('User-Agent'),
               'timestamp': datetime.datetime.now(),
               'guid': str(uuid.uuid4())}
    sessionObj = Session.Session(headers)
    return sessionObj.start_session()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
