import threading
import logging
import time
from kafka import KafkaConsumer


class Consumer(threading.Thread):
    daemon = True
    def run(self):

    
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                auto_offset_reset='earliest',   
                                )


        consumer.subscribe(['quickstart-events'])
        for message in consumer:
            print (message.value.decode("utf-8"))


def main():
    threads = [
        # Producer(),
        Consumer()
    ]
    for t in threads:
        t.start()
    time.sleep(10)
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
               '%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()