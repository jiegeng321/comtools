# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES


class AEScoder():
    def __init__(self):
        self.__key = b'0123456789ABCDEF'   # key的长度可以为16、24、32位

    # AES加密
    def encrypt(self, data):
        """
        :param  data: bytes, input data to encrypt
        :returns:  bytes, encrypted data
        """
        BS = 16
        if isinstance(data, bytes) and not isinstance(data, str):  # py3
            def pad(s): return s + bytes((BS - len(s) % BS)
                                         * chr(BS - len(s) % BS), encoding="utf-8")
        else:  # py2
            def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(self.__key, AES.MODE_ECB)
        encrData = cipher.encrypt(pad(data))
        return encrData

    # AES解密
    def decrypt(self, encrData):
        """
        :param  encrData: bytes, input data to decrypt
        :returns:  bytes, decrypted data
        """
        if isinstance(encrData, bytes) and not isinstance(encrData, str):  # py3
            def unpad(s): return s[0:-s[-1]]
        else:  # py2
            def unpad(s): return s[0:-ord(s[-1])]
        cipher = AES.new(self.__key, AES.MODE_ECB)
        decrData = unpad(cipher.decrypt(encrData))
        return decrData
