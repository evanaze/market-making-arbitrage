import time
from ccapi import EventHandler, SessionOptions, SessionConfigs, Session, Subscription, Event
from log import logger


class MyEventHandler(EventHandler):
    def __init__(self):
        super().__init__()

    def processEvent(self, event: Event, session: Session) -> bool:
        if event.getType() == Event.Type_SUBSCRIPTION_DATA:
            for message in event.getMessageList():
                correlationId = message.getCorrelationIdList()[0]
                print(f'Best bid and ask for cID {correlationId} at {message.getTimeISO()} are:')
                for element in message.getElementList():
                    elementNameValueMap = element.getNameValueMap()
                    for name, value in elementNameValueMap.items():
                        print(f'  {name} = {value}')
        return True  # This line is needed.


if __name__ == '__main__':
    eventHandler = MyEventHandler()
    option = SessionOptions()
    config = SessionConfigs()
    session = Session(option, config, eventHandler)
    cb_subscription = Subscription('coinbase', 'BTC-USD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=1", "1")
    kr_subscription = Subscription('kraken', 'XXBTZUSD', 'MARKET_DEPTH', "MARKET_DEPTH_MAX=10", "2")
    session.subscribe(cb_subscription)
    session.subscribe(kr_subscription)
    time.sleep(10)
    session.stop()
    print('Bye')
