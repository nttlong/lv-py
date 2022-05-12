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

        def group(self,id, auto_offset_reset= 'earliest'):
            return Consumer.__consumer_topic_wacther_runner__(self,id,auto_offset_reset)


    class __consumer_topic_wacther_runner__:
        def __init__(self,
                     owner,
                     group_id,
                     auto_offset_reset = 'earliest',
                     enable_auto_commit=False):
            self.group_id =group_id
            self.auto_offset_reset =auto_offset_reset
            self.enable_auto_commit =enable_auto_commit
            assert isinstance(owner, Consumer.__consumer_topic_wacther__)
            self.__owner__ = owner
            self.handler = None
        def __enter__(self):
            from confluent_kafka import Consumer
            from json import loads
            import time
            is_ok = False
            brokers = self.__owner__.__owner__.__owner__.__owner__.bootstrap_servers
            options = {
                'bootstrap.servers':",".join(brokers),
                'group.id': self.group_id,
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': self.enable_auto_commit,
            }
            config = {'metadata.broker.list': ','.join(brokers),
                      'group.id': self.group_id,
                      'default.topic.config': {'auto.offset.reset': 'latest'},
                      'enable.auto.commit': False,
                      'api.version.request': True,
                      'isolation.level': 'read_uncommitted'
                      }
            while not is_ok:
                try:
                    self.consumer = Consumer(
                        options
                    )
                    is_ok =True
                except:
                    time.sleep(1)
                    is_ok =False

            return  self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.consumer.close()
        def get_value(self):
            return self.__current_value__
        def get_record(self):
            return self.__current_record__
        def get_msg(self):
            return self.__current_mgs__
        def start_watch(self):
            import time
            import json
            from confluent_kafka import Consumer, KafkaException
            from confluent_kafka import TopicPartition
            if not self.handler or not callable(self.handler):
                raise Exception("handler was not set")
            origin = TopicPartition(self.__owner__.topic_id, 0, 0)
            self.consumer.subscribe(
                topics=[self.__owner__.topic_id]

            )
            c= self.consumer
            while True:
                try:
                    msg = c.poll(timeout=1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        raise KafkaException(msg.error())
                    else:
                        val = msg.value()
                        data = None
                        try:
                            data = json.loads(val)
                            self.handler(c, msg, data)
                        finally:
                            data = None
                            self.handler(c, msg, data)

                except:
                    time.sleep(1)

def consumer_in_thread(wacther):
    assert isinstance(wacther, Consumer.consumer_topic_wacther_runner)
    from multiprocessing import Process
    import time
    p = Process(target=wacther.start_watch, args=())
    p.start()
    p.join()











ConsumerTopicWacther = Consumer.__consumer_topic_wacther__