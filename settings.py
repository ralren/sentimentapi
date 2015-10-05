default_settings = {
    'API_KEY': 'e9b4e1c528d800c67c8dec7ade55dbb1',
    'SECRET': 'g5uyHb7IpJ7KKJrmFP6rggdVUrXMaq5bUhC8wqSUhy0vGpcEBACUOYw=',
    'indico_api_key': '322268e58f68a70969842a9e885a891d',
    'ACCESS_TOKEN': 'CAACEdEose0cBAAeLewL7UpJD5nzZBU5Dgp1Fl8ztYke0U78idZBfTT9ZAXlFV53Y0hadZBHkQj5DXckzxidEW7VikBIW73LTw7rAqR6YXttEs7HwyZCF4ZCHBXzhF31TJJsXz1kaS1xzcQDUDctfuIHxpd8Wg4IAL3ZAYgVxGQH9yqqW391Qv3tdxUBtWZBCV5Yq1X6CtIwQtKni7mxvYwjW'
}

def get(key):
    for k, v in default_settings.iteritems():
        if k == key:
            return v
