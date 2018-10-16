# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 00:34:08 2018

@author: Luisa
"""
    
import os
import json
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


    
def encrypt(cipher, plaintext):
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return ciphertext

def decrypt(cipher, ciphertext):
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ct) + decryptor.finalize()
    
    return plaintext

def load_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    public_key = load_pem_public_key(pemlines, default_backend())
    return public_key

def rsaEncrypt(plaintext, publicKey):
    ciphertext = publicKey.encrypt(
            plaintext, 
            padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
            )            
    )
            
    return ciphertext

def sign(messageToSign):
    h.update(messageToSign)
    signature = h.finalize()
    
    return signature

class Json(object):
        rsa = ""
        aes = ""
        hmac = ""
    
        # The class "constructor" - It's actually an initializer 
        def __init__(self, rsa, aes, hmac):
            self.rsa = rsa
            self.aes = aes
            self.hmac = hmac

def make_Json(rsa, aes, hmac):
    json = Json(rsa, aes, hmac)
    return json    
    
if __name__ == '__main__':
    #Setup encryption variables
    public_key_hold = load_key(b"C:\Users\Luisa\Documents\RSA_public.pem")    
    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)   
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    
    #Encrypt text
    ct = encrypt(cipher, b"Hello world!!!!!")

    #Decrypt text
    pt = decrypt(cipher, ct)
    
    #Setup signature
    key2 = os.urandom(32)
    h = hmac.HMAC(key2, hashes.SHA256(), backend=default_backend())
    
    #Sign ciphertext
    signature = sign(ct)
    
    #Setup verification signature (only for text purposes)
    h2 = hmac.HMAC(key2, hashes.SHA256(), backend=default_backend())
    h2.update(ct)
    
    #Verify signature (no message == OK)
    h2.verify(signature)
    
    #Concatenate keys to send to receiver
    concatenated = key + key2

    #Encrypt concatenated keys with RSA    
    cipherKeys = rsaEncrypt(concatenated, public_key_hold)
    
    #Print in JSON (problems while decoding bytes)
    print(json.dumps(
            {'RSA ciphertext': cipherKeys.decode('utf-8', 'replace'), 'AES ciphertext': ct.decode('utf-8', 'replace'), 'HMAC tag': signature.decode('utf-8', 'replace')},
            sort_keys=True,
            indent=4, 
            separators=(',', ': ')
        )
    )
            
    '''print("RSA ciphertext: {}" .format(cipherKeys))
    print("AES ciphertext: {}" .format(ct))
    print("HMAC tag: {}" .format(signature))'''


    