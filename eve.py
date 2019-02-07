import scrapy

class Sg101Spider(BaseSpider):
    name = "sg101"
    msg_id = 1              # current message to retrieve
    max_msg_id = 21399      # last message to retrieve

    def start_requests(self):
        return [FormRequest(LOGIN_URL,
            formdata={'login': LOGIN, 'passwd': PASSWORD},
            callback=self.logged_in)]

    def logged_in(self, response):
        if response.url == 'http://my.yahoo.com':
            self.log("Successfully logged in. Now requesting 1st message.")
            return Request(MSG_URL % self.msg_id, callback=self.parse_msg,
                    errback=self.error)
        else:
            self.log("Login failed.")

    def parse_msg(self, response):
        self.log("Got message!")
        print response.body

    def error(self, failure):
        self.log("I haz an error")
