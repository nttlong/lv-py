__static_dict__ = None

import confluent_kafka
import threading as __threading__

__lock__ = __threading__.Lock()

class KafkaProducerAuto():
    def __init__(self,topic_key, bootstrap_servers):
        import json
        import time
        self.__producer__ = None
        is_ok= False
        self.bootstrap_servers =bootstrap_servers
        while not  is_ok:
            try:
                self.__producer__ = confluent_kafka.Producer(
                    {
                        'bootstrap.servers':",".join(self.bootstrap_servers)
                        # 'socket.timeout.ms': 100,
                        # 'api.version.request': 'false',
                        # 'broker.version.fallback': '0.9.0',
                    }
                )

                is_ok = True
            except Exception as e:
                time.sleep(0.3)


        self.topic_key = topic_key
        self.topic = KafkaProducerAuto.__Topic__(self)


    class __Topic__:
        def __init__(self,owner):
            self.__owner__ = owner
        def __getattr__(self, item):
            return KafkaProducerAuto.__Topic__.__Sender__(
                self.__owner__.topic_key+"."+item,
                self
            )

        class __Sender__:
            def __init__(self,topic_key,owner):
                self.__owner__ = owner
                self.topic_key = topic_key

            def send(self, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
                import json
                assert isinstance(self.__owner__, KafkaProducerAuto.__Topic__)
                assert isinstance(self.__owner__.__owner__, KafkaProducerAuto)

                def delivery_report(err, msg):
                    if err:
                        print(err)
                    else:
                        print(msg)

                ret=self.__owner__.__owner__.__producer__.produce(
                    self.topic_key,
                    json.dumps(value,check_circular=False),
                    callback=delivery_report

                )


                return ret




Topic_sender = KafkaProducerAuto.__Topic__.__Sender__

def __producer__(
        producer_name,
        servers
):
    global __static_dict__
    global __lock__
    assert isinstance(producer_name, str), 'producer_name must be str'
    assert isinstance(servers, list), 'producer_name must be str[]'

    producer_name = producer_name.lower()
    from confluent_kafka import Producer

    import json
    if not __static_dict__:
        __lock__.acquire()
        __static_dict__ = {}
        __lock__.release()
    ret = __static_dict__.get(producer_name, None)

    if not isinstance(ret, Producer):
        __lock__.acquire()
        ret = Producer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        __lock__.release()
    return ret


class Bootstrap:

    def __init__(self, bootstrap_servers):
        """
        Create bootstrap servers
        """
        assert isinstance(bootstrap_servers, list), 'producer_name must be str[]'
        self.__bootstrap_servers__ = bootstrap_servers
        self.producers = Bootstrap.ReProducer(self)

    class ReProducer:
        def __init__(self, owner):
            self.__owner__ = owner
        # def __getitem__(self, item):
        #     print("get_" + item)
        # def __getattr__(self, item):
        #     print("get_"+item)
        def __getattr__(self, item):
            assert isinstance(self.__owner__, Bootstrap)
            return KafkaProducerAuto(item, self.__owner__.__bootstrap_servers__)





