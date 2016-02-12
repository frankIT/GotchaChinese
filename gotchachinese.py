#!/usr/bin/python

import os, time
from cmd import Cmd
from random import randint

from application.notification import NotificationCenter, IObserver
from application.python import Null
from threading import Event
from zope.interface import implements

from sipsimple.account import AccountManager
from sipsimple.application import SIPApplication
from sipsimple.storage import FileStorage
from sipsimple.core import ToHeader, SIPURI
from sipsimple.lookup import DNSLookup, DNSLookupError
from sipsimple.session import Session
from sipsimple.streams import AudioStream
from sipsimple.threading.green import run_in_green_thread

class TenFifty(object):
    implements(IObserver)

    def __init__(self):
        self.application = SIPApplication()
        self.quit_event = Event()

        notification_center = NotificationCenter()
        notification_center.add_observer(self, sender=self.application)

    def start(self):
        self.application.start(FileStorage(os.path.realpath('test-config')))

    def stop(self):
        self.application.stop()

    def handle_notification(self, notification):
        handler = getattr(self, '_NH_%s' % notification.name, Null)
        handler(notification)

    def _NH_SIPApplicationDidStart(self, notification):
        print 'Clem\'s gonna stress...'

    def _NH_SIPApplicationDidEnd(self, notification):
        self.quit_event.set()


class OutgoingCallHandler(object):
    implements(IObserver)

    def __init__(self):
        self.session = None

    @run_in_green_thread
    def call(self, destination):
        if self.session is not None:
            print 'Another session is in progress'
            return
        callee = ToHeader(SIPURI.parse(destination))
        try:
            routes = DNSLookup().lookup_sip_proxy(callee.uri, ['udp']).wait()
        except DNSLookupError, e:
            print 'DNS lookup failed: %s' % str(e)
        else:
            account = AccountManager().default_account
            self.session = Session(account)
            NotificationCenter().add_observer(self, sender=self.session)
            self.session.connect(callee, routes, [AudioStream()])

    def hangup(self):
        if self.session is None:
            print 'There is no session to hangup'
            return
        self.session.end()

    def handle_notification(self, notification):
        handler = getattr(self, '_NH_%s' % notification.name, Null)
        handler(notification)

    def _NH_SIPSessionGotRingIndication(self, notification):
        print 'Ringing!'

    def _NH_SIPSessionWillStart(self, notification):
        print 'connessione...'

    def _NH_SIPSessionDidStart(self, notification):
        print 'Cioccato :('
        global catched
        catched = catched + 1        

    def _NH_SIPSessionDidFail(self, notification):
        #print 'Failed to connect'
        self.session = None
        NotificationCenter().remove_observer(self, sender=notification.sender)

    def _NH_SIPSessionDidEnd(self, notification):
        #print 'Session ended'
        self.session = None
        NotificationCenter().remove_observer(self, sender=notification.sender)


def ringToClem():
    call_handler.call("sip:victim_number@voip.provider.it") # clem
    time.sleep(6)
    call_handler.hangup()

application = TenFifty()
application.start()
call_handler = OutgoingCallHandler()

rings = 0
catched = 0
interval_from = 60
interval_to = 180
interval_reset = 1

try:
    while True:
        if catched >= (10 * interval_reset):
            interval_from = interval_from * 2
            interval_to = interval_to * 2
            interval_reset = interval_reset + 1
        
        if rings > 0: # skip timeout for the first run    
            time.sleep(randint(interval_from,interval_to))
        else:
            time.sleep(5)
                       
        ringToClem()
        rings = rings + 1
        os.system('clear')
        print 'Clem is under goccia cinese now, press CTRL+C to let him free' + '\n\n'
        print 'Rings total: ', rings
        print 'Rings catched: ', catched
        
except KeyboardInterrupt:
    pass

class Stop(object):
    pass

application.stop()
application.quit_event.wait()
