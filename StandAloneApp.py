# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 00:34:08 2018

@author: Luisa
"""
    
import os
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
    
if __name__ == '__main__':
    public_key_hold = load_key(b"C:\Users\Luisa\Documents\RSA_public.pem")
    #print(public_key_hold.key_size)
    
    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    ct = encrypt(cipher, b"Hello world!!!!!")
    #print(ct)
    pt = decrypt(cipher, ct)
    #print(pt)
    
    key2 = os.urandom(32)
    h = hmac.HMAC(key2, hashes.SHA256(), backend=default_backend())
    h.update(ct)
    signature = h.finalize()
    #print(signature)
    
    
    h2 = hmac.HMAC(key2, hashes.SHA256(), backend=default_backend())
    h2.update(ct)
    #print(h2.verify(signature))
    
    concatenated = key + key2
    #print(concatenated)
    
    cipherKeys = public_key_hold.encrypt(
            concatenated, 
            padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
            )            
    )
            
    print("RSA ciphertext: {}" .format(cipherKeys))
    print("AES ciphertext: {}" .format(ct))
    print("HMAC tag: {}" .format(signature))


    