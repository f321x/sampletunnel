import time
import ssl
import json
import pyperclip
from nostr.event import Event, EventKind
import nostr.key
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import get_public_key
from nostr.filter import Filter, Filters

prikey = "d4a78905f4fb815fa31a3c651e9e7720b105443e7649e1833bb328e6a1c9b2de"  # unused example
pubkey = get_public_key(prikey)
relay_manager = RelayManager()
ss = nostr.key.compute_shared_secret(prikey, pubkey)


def nostr_connect():
    try:
        filters = Filters([Filter(authors=[pubkey], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE], limit=0)])
        subscription_id = str(pubkey) + "dl"
        request = [ClientMessageType.REQUEST, subscription_id]
        request.extend(filters.to_json_array())
        relay_manager.add_relay("wss://relay.damus.io")
        relay_manager.add_relay("wss://nostr-pub.wellorder.net")
        relay_manager.add_subscription(subscription_id, filters)
        relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
        time.sleep(1.25)
        message = json.dumps(request)
        relay_manager.publish_message(message)
    except:
        pass


def nostr_receive():
    nostr_connect()
    time.sleep(2)
    while True:
        try:
            event_msg = relay_manager.message_pool.get_event()
            time.sleep(2)
            x = nostr.key.decrypt_message(event_msg.event.content, ss)
            pyperclip.copy(x)
            print(x)
        except:
            nostr_connect()
            time.sleep(2)


nostr_receive()
