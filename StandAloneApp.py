# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 00:34:08 2018

@author: Luisa
"""
    
import os
import json
import base64
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


    
def encrypt(cipher, plaintext):
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return ciphertext

def decrypt(cipher, ciphertext):
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ct) + decryptor.finalize()
    
    return plaintext

def loadPublicKey(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    publicKey = load_pem_public_key(pemlines, default_backend())
    return publicKey

def loadPrivateKey(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    privateKey = load_pem_private_key(pemlines, b"brivatekeyle", default_backend())
    return privateKey

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

def rsaDecrypt(ciphertext, privateKey):
    plaintext = privateKey.decrypt(
            ciphertext,
            padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
            )
    )
            
    return plaintext

def sign(messageToSign):
    h.update(messageToSign)
    signature = h.finalize()
    
    return signature   
    
if __name__ == '__main__':
    #Setup encryption variables
    public_key_hold = loadPublicKey(b"C:\Users\Luisa\Documents\RSA_public.pem")    
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
    
    #Save data in JSON file    
    with open(b"C:\Users\Luisa\Documents\data.json", "w") as outfile:
        json.dump(
                {'RSA ciphertext': str(base64.b64encode(cipherKeys), 'utf-8'), 
                 'AES ciphertext': str(base64.b64encode(ct), 'utf-8'), 
                 'HMAC signature': str(base64.b64encode(signature), 'utf-8')
                },
            outfile
        )
                
    #----------------------------- DECRYPTION PART --------------------------------------
    
    #Load private key
    privateKey = loadPrivateKey(b"C:\Users\Luisa\Documents\RSA_private.pem")
    
    #Extract JSON file data
    with open(b"C:\Users\Luisa\Documents\data.json") as infile:
        data = json.load(infile)
    
    rsaCiphertext = base64.b64decode(data['RSA ciphertext'])
    aesCiphertext = base64.b64decode(data['AES ciphertext'])
    hmacSignature = base64.b64decode(data['HMAC signature'])
    
    #Decrypt RSA ciphertext
    aesAndHmac = rsaDecrypt(rsaCiphertext, privateKey)
    
    #Get AES key and HMAC key from RSA plaintext
    aesKey = aesAndHmac[:32]
    hmacKey = aesAndHmac[32:]
    
    #Regenerate HMAC tag with decrypted HMAC key
    hmacTag = hmac.HMAC(hmacKey, hashes.SHA256(), backend=default_backend())
    hmacTag.update(aesCiphertext)
    
    #Verify ciphertext has not been corrupted
    hmacTag.verify(hmacSignature)
    
    #Load AES Key
    decCipher = Cipher(algorithms.AES(aesKey), modes.CBC(iv), backend=backend)
    
    #Decrypt
    print(decrypt(decCipher, aesCiphertext))
    
            