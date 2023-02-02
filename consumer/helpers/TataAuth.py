import time
class Auth:
    def __init__(self):
        self._triggerTime = 60*60
        self.log = []
        self._token = None
        
    # getter method
    def get_token(self , callCurrTimeStamp):
        if time.time() - callCurrTimeStamp > self._triggerTime:
            return None
        else:
            return self._token

    # setter method
    def set_token(self, x):
        if x:
            self._token = x




