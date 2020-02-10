import redis

class Redis:

    def __init__(self, host='localhost', port=6379, db=0,):
        self.host = host  
        self.port = port
        self.db = db
        self.connection = self.connect()

    def connect(self):
        '''
        :return: Returns connection, which is set to self.connect
        '''
        connection = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        if connection:
            print('Connection established : ', connection)
        return connection

    def delete(self, *names):
        self.connection.delete(*names)

    def exists(self, key):
        return self.connection.exists(key)

    def get(self, key):
        return self.connection.get(key)

    def mget(self, *key):
        return self.connection.mget(*key)

    def set(self, key, value, exp_s=None, exp_ms=None):
        '''
        :param key: Name for Cache 'key'
        :param value: Name of what is being stored in Cache 'key'
        :param exp_s: Expiry of cache in seconds, None would mean cache is stored indefinitely
        :param exp_ms: Expiry of cache in milliseconds
        :return : returns string with confirmation
        '''
        self.connection.set(key, value, exp_s, exp_ms)
        return 'key:value is set in-memory cache'
