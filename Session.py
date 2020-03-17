import mysql.connector, yaml


class Session:
    def __init__(self, request_headers):
        with open('conf.yml', 'r') as conf_file:
            loaded_conf = yaml.load(conf_file, Loader=yaml.FullLoader)

        db_host = loaded_conf.get('host')
        user = loaded_conf.get('db_user')
        secret = loaded_conf.get('db_secret')
        db_name = 'flask_access_log'
        self.request_headers = request_headers
        self.db_conn = mysql.connector.connect(host=db_host, user=user, passwd=secret, database=db_name)
        self.db_cursor = self.db_conn.cursor()

    def start_session(self):
        query = "INSERT INTO sessions(access_date, ip_address, id, user_agent) VALUES (%s, %s, %s, %s);"
        values = [self.request_headers['timestamp'], self.request_headers['ip'], self.request_headers['guid'], self.request_headers['agent']]
        self.db_cursor.execute(query, values)
        self.db_conn.commit()
        return self.request_headers

    def validate_session(self):
        query = """select ip_address from sessions where ip_address=%s;"""
        values = [self.request_headers['ip']]
        self.db_cursor.execute(query, values)
        results = self.db_cursor.fetchall()
        if results:
            return str(results)
        else:
            return False

        #create a validate login page



    def __del__(self):
        self.db_cursor.close()
        self.db_conn.close()