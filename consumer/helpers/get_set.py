class storeData:
    def __init__(self):
        self.list = []

    def set_data(self, data):
        print("this is setter method for storeData")
        if data:
            self.list.append(data)

    def get_data(self):
        print("this is setter method for storeData")
        return self.list