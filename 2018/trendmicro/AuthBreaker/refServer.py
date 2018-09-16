# REQUIRED: PyCrypto 2.6.1
#     To install: pip install pycrypto
#     Homepage: https://www.dlitz.net/software/pycrypto/

import argparse
import sys
import socket
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from Crypto.Cipher import AES


from refServer import *

class Client:

    nonceLengthInBytes = 8

    def __init__(self, host, port, username, password):
        self.username = username
        self.password = password
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(1)
        self._socket.connect((host, port))
        self._f = self._socket.makefile("rw")

    def close():
        self._f.close()
        self._socket.close()

    def execute(self, command):
        self._sendMessage_Command(command)
        return self._expectMessage_CommandResult()

    def authenticate(self):
        self._sendMessage_LogonRequest()
        (nonce, challengeCookie) = self._expectMessage_LogonChallenge()
        r = self._computeChallengeResponse(nonce)
        self._sendMessage_LogonResponse(r, challengeCookie)
        self.ticket = self._expectMessage_LogonSuccess()

    def _sendMessage_LogonRequest(self):
        self._f.write("\x01")
        self._f.write(toNullTerminatedUtf8(self.username))
        self._f.flush()

    def _expectMessage_LogonChallenge(self):
        self._expectMessageType(0x02)
        nonce = self._readBytes(self.nonceLengthInBytes)
        challengeCookie = self._expectString()
        return (nonce, challengeCookie)

    def _computeChallengeResponse(self, nonce):
        return SHA256.new(nonce + self.password).digest()

    def _sendMessage_LogonResponse(self, r, challengeCookie):
        self._f.write("\x03")
        self._f.write(r)
        self._f.write(toNullTerminatedUtf8(challengeCookie))
        self._f.flush()

    def _expectMessage_LogonSuccess(self):
        messageType = self._readMessageType()
        if messageType == 0x04:
            ticket = self._expectString()
            return ticket
        elif messageType == 0x05:
            return None
        else:
            raise Exception("Unexpected message type: 0x%02x" % messageType)


    def _sendMessage_Command(self, command):
        self._f.write("\x06");
        self._f.write(toNullTerminatedUtf8(self.ticket))
        self._f.write(toNullTerminatedUtf8(command))
        self._f.flush()

    def _expectMessage_CommandResult(self):
        messageType = self._readMessageType()
        if messageType == 0x07:
            result = self._expectString()
            return result
        elif messageType == 0x05:
            sys.stderr.write("Unauthorized\n")
            exit(1)
        else:
            raise Exception("Unexpected message type: 0x%02x" % messageType)

    def _readMessageType(self):
        messageTypeByte = self._readBytes(1)
        if (len(messageTypeByte) == 0):
            raise Exception("Server has disconnected")
        return ord(messageTypeByte)

    def _expectMessageType(self, expectedMessageType):
        messageType = self._readMessageType()
        if messageType != expectedMessageType:
            raise Exception("Unexpected message type: 0x%02x" % messageType)

    def _readBytes(self, nBytes):
        result = self._f.read(nBytes)
        if len(result) != nBytes:
            raise Exception("Connection was closed")
        return result

    def _expectString(self):
        buf = b''
        while True:
            if len(buf) > 1 << 20:
                raise Exception("Overly long input")
            c = self._f.read(1)
            if len(c) == 0:
                raise Exception("End of stream reached")
            if ord(c[0]) == 0:        # Indicates NULL termination of a UTF-8 string.
                break
            buf += c
        return unicode(buf, encoding="utf-8", errors="strict")

def sxor(s1,s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

# Validates ticket and returns a tuple (identity, error).
# On success, identity is an identity object and error is None.
# On failure, identity is None and error is a string indicating the type of error
def validateTicket(ticket):
    try:
        logger.debug("Ticket: %s", ticket)
        d = BytesIO(decrypt(b64decode(ticket), serverKey))
        # print(repr(d.read()))
        identityFromTicket = json.loads(readNullTerminatedString(d))
        timestamp = unpack("<q", readBytes(d, 8))[0]
        if len(d.read(1)) != 0:		# Not at end of string
            raise Exception("Ticket is not well formed")
        currentTime = getCurrentTimestamp()
        logger.debug("Ticket timestamp: %d. Current time: %d", timestamp, currentTime)
        if timestamp < currentTime - 1 * 60 * 60 * 1000 or timestamp > currentTime:
            return (None, "EXPIRED")
        username = identityFromTicket["user"]
        if not (isinstance(username, str) or isinstance(username, unicode)):
            raise Exception("Ticket is not well formed: username is not a string")
        groups = []
        for group in identityFromTicket["groups"]:
            if not (isinstance(group, str) or isinstance(group, unicode)):
                raise Exception("Ticket is not well formed: group name not a string")
            groups.append(group)
        identity = { "user": username, "groups": groups }
        return (identity, None)
    except:
        logger.info("Ticket is not well formed", exc_info=True)
        return (None, "INVALID")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("command")

    args = parser.parse_args()

    # client = Client(args.host, args.port, args.username, args.password)
    # client.authenticate()
    # if not client.ticket:
    #     sys.stderr.write("Failed to authenticate\n")
    #     exit(1)
    # print client.execute(args.command)

    import json
    identity = json.dumps( \
        { "user" : "admin", "groups": ["admin"] }, \
        ensure_ascii = False)

    asz = (len(identity) + 15) / 16 * 16 - 8
    identity = identity.ljust(asz - 1, ' ')

    client = Client(args.host, args.port, "A"*8 + identity, args.password)
    client._sendMessage_LogonRequest()
    (nonce, challengeCookie) = client._expectMessage_LogonChallenge()
    decoded = b64decode(challengeCookie)
    iv, msg = decoded[:16], decoded[16:]

    ticket = b64encode(msg)
    #validateTicket(ticket)
    client.ticket = ticket
    print client.execute("getflag")

