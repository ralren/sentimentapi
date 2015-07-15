import tornado.ioloop
import tornado.web


class SentimentHandler(tornado.web.RequestHandler):
	@tornado.gen.coroutine
    def get(self, author, buzz_slug):
        buzz = get_buzz(author, buzz_slug)
        fbid = get_fbid(author, buzz_slug)

    @tornado.gen.coroutine
    def get_buzz(author, buzz_slug):
    	dashbird_url = settings.get('dashbird_api_url')
        url = '%s/api/buzz?author=%s&slug=%s' % (dashbird_url, author, buzz_slug)

        request = tornado.httpclient.HTTPRequest(url=url)

        with statsd.timer('whirldash.fetch'):
            response = yield self.http.fetch(request)
            logging.info(response.body)
            buzz = json.loads(response.body)

        raise tornado.gen.Return(buzz)

    @tornado.gen.coroutine
    def get_fbid(author, buzz_slug):

application = tornado.web.Application([
    (r"author/([\w-]+)/buzz/([\w-]+)$", SentimentHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()