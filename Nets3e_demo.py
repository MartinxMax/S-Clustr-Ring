#!/usr/bin/python3
# @Мартин.
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝

import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import binascii
import hashlib
import re
import os

class S_Clustr_AES_CBC():
    def aes_cbc_encode(self,key, data,iv=16):
        if not self.__is_md5_hash(key):
            key = hashlib.md5(key.encode('utf-8')).hexdigest().encode()
        else:
            key = key.encode()
        iv_b = get_random_bytes(iv)
        cipher = AES.new(key, AES.MODE_CBC, iv_b)
        padded_data = pad(data.encode('utf-8'), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        ciphertext = iv_b + encrypted_data
        ciphertext_hex = binascii.hexlify(ciphertext).decode('utf-8')
        return ciphertext_hex

    def aes_cbc_decode(self,key,data,iv=16):
        try:
            if not self.__is_md5_hash(key):
                key = hashlib.md5(key.encode('utf-8')).hexdigest().encode()
            else:
                key = key.encode()
            if self.__is_hex_string(data):
                ciphertext = binascii.unhexlify(data)
            else:
                ciphertext = data.encode('utf-8')
            iv_b = ciphertext[:iv]
            encrypted_data = ciphertext[iv:]
            cipher = AES.new(key, AES.MODE_CBC, iv_b)
            decrypted_data = cipher.decrypt(encrypted_data)
            data = unpad(decrypted_data, AES.block_size).decode('utf-8')
        except Exception as e:
            return None
        else:
            return data

    def __is_md5_hash(self,value):
        if len(value) == 32:
            md5_pattern = re.compile(r"^[a-fA-F0-9]{32}$")
            return bool(md5_pattern.match(value))
        return False


    def __is_hex_string(self, data):
        try:
            _ = binascii.unhexlify(data)
            return True
        except binascii.Error:
            return False

info = '''
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝
'''

def main():
    AESS = S_Clustr_AES_CBC()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_ADDRESS = ('192.168.8.105', 10000)
    KEY = "7e03d4872b1e14d51d75ad4b16341a5e"
    client_socket.connect(SERVER_ADDRESS)
    data = AESS.aes_cbc_encode(KEY, '{"TYPE": "Nets3e"}')
    client_socket.send(data.encode('utf-8'))
    while True:
        data=AESS.aes_cbc_decode(KEY,client_socket.recv(1024).decode('utf-8'))
        print("Recv:",data)
        if data=="RUN":
            print(info)
            os.system(r".\Nets3eClient_debug.exe")
            print("Run...")
            client_socket.send("True".encode('utf-8'))
        elif data=="STOP":
            print("Exit")
            client_socket.send("False".encode('utf-8'))
            break
    client_socket.close()

if __name__ == '__main__':
    main()
