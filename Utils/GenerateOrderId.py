
class GenerateOrderId:
    def __init__(self , user_id , epochTime):
        self.user_id = user_id
        self.epochTime = epochTime


    def getOrderId(self):
        return self.user_id + self.epochTime
