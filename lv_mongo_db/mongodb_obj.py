class MongoDbItem:
    def __init__(self, data):
        assert isinstance(data, dict)
        for k, v in data.items():
            if k.__len__()>4 and k[0:2] != "__" and k[-2:] != "__":
                self.__dict__[k] = v
            else:
                self.__dict__[k] = v
    def __getattr__(self, item):
        ret = self.__dict__.get(item,None)
        return  ret

