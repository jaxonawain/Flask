import mysql.connector, yaml


class Session:
    def __init__(self, request_headers):
        # Load config file into memory and set database parameters.
        with open('conf.yml', 'r') as conf_file:
            loaded_conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        self.request_headers = request_headers
        self.db_conn = mysql.connector.connect(host=loaded_conf.get('host'), user=loaded_conf.get('db_user'),
                                               passwd=loaded_conf.get('db_secret'), database='flask')
        self.db_cursor = self.db_conn.cursor()

    def start_session(self):
        # Insert session data into session table
        query = "INSERT INTO sessions(access_date, ip_address, id, user_agent) VALUES (%s, %s, %s, %s);"
        values = [self.request_headers['timestamp'], self.request_headers['ip'], self.request_headers['guid'],
                  self.request_headers['agent']]
        self.db_cursor.execute(query, values)
        self.db_conn.commit()
        return self.request_headers

    def create_user(self):
        query = "INSERT INTO user_db(user_id, secret, first_name, last_name) VALUES (%s, %s, %s, %s);"
        values = [self.request_headers['username'], self.request_headers['secret'], self.request_headers['first_name'],
                  self.request_headers['last_name']]
        self.db_cursor.execute(query, values)
        self.db_conn.commit()
        return True

    def validate_login(self):
        query = "SELECT user_id FROM user_db WHERE user_id=%s AND secret=%s"
        values = [self.request_headers['username'], self.request_headers['secret']]
        self.db_cursor.execute(query, values)
        result = str(self.db_cursor.fetchall())
        if self.request_headers["username"] in result:
            return True
        else:
            print(result)
            print(self.request_headers['username'])
            return False

    def validate_session(self):
        # Validate that there is a current session for user/machine
        query = """select ip_address from sessions where ip_address=%s;"""
        values = [self.request_headers['ip']]
        self.db_cursor.execute(query, values)
        results = self.db_cursor.fetchall()
        if results:
            return str(results)
        else:
            return False

    def __del__(self):
        self.db_cursor.close()
        self.db_conn.close()
