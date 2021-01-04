# coding: utf8
import time
import random
import base64
import hashlib

class Cipher(object):

    def __init__(self):
        self.PRE_KEYMAP = "abcdefghijklmnopqrstuvwxyz+=0123456789"
        self.SUF_KEYMAP = "zyxwvutsrqponmlkjihgfedcba_#9876543210"
        self.SEPARATOR  = "&NBSP;"

    def encrypt(self, key, origin):
        origin = str(base64.b64encode((key + self.SEPARATOR + origin).encode("utf8"))).lstrip("b")
        encoded = str.maketrans(self.PRE_KEYMAP, self.SUF_KEYMAP)
        ret = origin.translate(encoded)
        return ret

    def decrypt(self, key, origin):
        decoded = str.maketrans(self.SUF_KEYMAP, self.PRE_KEYMAP)
        ret = origin.translate(decoded)
        ret = base64.b64decode(ret).decode('utf8', 'replace').lstrip((key+self.SEPARATOR))
        return ret

    def md5(self, origin):
        if origin == "":
            origin = random.shuffle(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))[0:10]
        origin = origin.encode("utf8")
        md5 = hashlib.md5()
        md5.update(origin)
        return md5.hexdigest()


if __name__ == '__main__':
    origin = "Anonymous_'Jp4CU8A2MqA5NDpbMA##'"
    key = ""
    cipher = Cipher()
    # ret = cipher.encrypt(key, origin)
    # print(ret)
    # print("================")
    ret = cipher.decrypt(key, origin)
    print(ret)
    print(cipher.md5("ABC"))