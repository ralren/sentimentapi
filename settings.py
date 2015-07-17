default_settings = {
    'API_KEY': 'e9b4e1c528d800c67c8dec7ade55dbb1',
    'SECRET': 'g5uyHb7IpJ7KKJrmFP6rggdVUrXMaq5bUhC8wqSUhy0vGpcEBACUOYw=',
    'indico_api_key': '322268e58f68a70969842a9e885a891d',
    'ACCESS_TOKEN': 'CAACEdEose0cBAJdWN4ZB24GZArNXRb7tFqBT2tOnNrEk9GuACuFhTj74vvp6wS6M0kEqdnARXif5sz7t0COiXCZAxYHmkqWy8NwYZBSZB2fkRVKiXfWFUUBHO1LDu5ZCfyUwN56w0zql6ZAsomV6TLElIslpSbnuyjdnWT5szXgtYk2gb3bJ6pfZBieL3IMIeeGytEEcnwMBTyUiKibGdY7x'
}

def get(key):
    for k, v in default_settings.iteritems():
        if k == key:
            return v
