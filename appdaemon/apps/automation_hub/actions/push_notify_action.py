from util import hassutil

class PushNotifyAction():
    def __init__(self):
        self.target = None
        self.message = None
        self.title = None

    def set_message(self, message, title="Home Assistant"):
        self.message = message
        self.title = title
        return self

    def notify(self):
        hassutil.join_notify(self.target, self.message, title=self.title)