import libs.firestore as firestore


class User(object):

    def __init__(self, telegramId):
        self.telegramId = telegramId

    async def createMessage(self, message):
        res = await firestore.addDoc(self.telegramId, message)
        return res

    async def readMessages(self, filterArg):
        res = await firestore.readCol(self.telegramId, filterArg)
        return res
