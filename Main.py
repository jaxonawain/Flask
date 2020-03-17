import Session, uuid, datetime, yaml
from flask import Flask, request, render_template
app = Flask(__name__)

# Validate against IP, need to include functionality to pair with username once authentication in place
def validate():
    print(request.remote_addr)
    headers = {'ip': request.remote_addr,
               'agent': request.headers.get('User-Agent')}
    sessionObj = Session.Session(headers)
    if sessionObj.validate_session():
        return True
    else:
        return False

# Create session in session table. Need to call with authentication script. Need to automatically remove from table too.
def create_session():
    # Gather headers
    headers = {'ip': request.remote_addr,
               'agent': request.headers.get('User-Agent'),
               'timestamp': datetime.datetime.now(),
               'guid': str(uuid.uuid4())}

    sessionObj = Session.Session(headers)
    return sessionObj.validate_session()


@app.route('/')
def home():
    if validate():
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():
    return render_template('home.html')


#@app.route('.protein_tracker'):

if __name__ == '__main__':
    app.run(host='0.0.0.0')
