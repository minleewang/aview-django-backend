from abc import ABC, abstractmethod


class RedisService(ABC):
    @abstractmethod
    def storeKeyValue(self, key, value):
        pass

    @abstractmethod
    def getValueByKey(self, key):
        pass

    @abstractmethod
    def deleteKey(self, key):
        pass