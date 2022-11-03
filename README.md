# sampletunnel
### share sample information between two laboratory computers

labora.py detects specific sample information on input (keylogger style) and, after reformatting, publishes them as encrypted message (Type 4) on various relays via the Nostr protocol. 

ir.py listens for new nostr events published by the labora.py pubkey. After receiving an event the message will be decrypted and stored into the clipboard.

_This way sample information only needs to be typed in on one computer and can simply be pasted in the lab specific software running on the receiving computer._

#### Additional information:

**Nostr protocol:**
https://github.com/nostr-protocol/nostr
