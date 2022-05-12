import  threading
__lock__ = threading.Lock()
__consumer_topic_wacther__dic__ = {}
class Consumer:
    def __init__(self,bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers

    def __getattr__(self, item):
        ret = Consumer.__consumer__(item,self)
        return ret

    class __consumer__:
        def __init__(self,key,owner):
            assert isinstance(owner,Consumer)
            self.__owner__=owner
            self.__key__ = key
            self.topic =Consumer.__consumer_topic__(self)

    class __consumer_topic__:
        def __init__(self,owner):
            assert isinstance(owner,Consumer.__consumer__)
            self.__owner__ = owner
        def __getattr__(self, item):
            # global __consumer_topic_wacther__dic__
            # global __lock__
            topic_id = self.__owner__.__key__+"."+item
            ret = __consumer_topic_wacther__dic__.get(topic_id,None)
            if not isinstance(ret,Consumer.__consumer_topic_wacther__):
                __lock__.acquire()
                __consumer_topic_wacther__dic__[topic_id] = Consumer.__consumer_topic_wacther__(
                    topic_id=topic_id,
                    owner= self
                )
                ret = __consumer_topic_wacther__dic__[topic_id]
                __lock__.release()
            return ret



    class __consumer_topic_wacther__:
        def __init__(self,topic_id,owner):
            assert isinstance(owner,Consumer.__consumer_topic__)
            self.__owner__ = owner
            self.topic_id=topic_id

ConsumerTopicWacther = Consumer.__consumer_topic_wacther__