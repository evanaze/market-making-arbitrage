import time
from ccapi import EventHandler, SessionOptions, SessionConfigs, Session, Subscription, Event
from log import logger


class MyEventHandler(EventHandler):
    def __init__(self):
        super().__init__()
    def processEvent(self, event: Event, session: Session) -> bool:
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for message in event.getMessageList():
                print(f'Best bid and ask at {message.getTimeISO()} are:')
                for element in message.getElementList():
                    correlationId = message.getCorrelationIdList()[0]
                    elementNameValueMap = element.getNameValueMap()
                    print(f" Correlation ID: {correlationId}")
                    for name, value in elementNameValueMap.items():
                        print(f'  {name} = {value}')
        return True  # This line is needed.


if __name__ == '__main__':
    eventHandler = MyEventHandler()
    option = SessionOptions()
    config = SessionConfigs()
    session = Session(option, config, eventHandler)
    cb_subscription = Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH')
    kr_subscription = Subscription('kraken', 'BTC-USD', 'MARKET_DEPTH')
    session.subscribe(cb_subscription)
    session.subscribe(kr_subscription)
    time.sleep(10)
    session.stop()
    print('Bye')
