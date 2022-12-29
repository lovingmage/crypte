import random
import sys
import math
import os
import gmpy2
from util import PRF, space_mapping
import hashlib

# To implement this labeled encyption scheme, Many functions come from paillier.py in phe1.3.

class SecretKey(object):
    def __init__(self, public_key, p, q):
        if not p*q == public_key.n:
            raise ValueError('given public key does not match the given p and q.')
        self.public_key = public_key
        if q < p: #ensure that p < q. 
            self.p = q
            self.q = p
        else:
            self.p = p
            self.q = q
          
        # variable for decryption using CRT
        self.psquare = self.p * self.p
        self.qsquare = self.q * self.q
        self.p_inverse = invert(self.p, self.q)
        self.hp = self.h_function(self.p, self.psquare);
        self.hq = self.h_function(self.q, self.qsquare);
        # self.l = (self.p-1)*(self.q-1)
        # self.mu = invert(self.l, public_key.n)

    def __repr__(self):
        pub_repr = repr(self.public_key)
        return "<PaillierPrivateKey for {}>".format(pub_repr)
    
    def decrypt(self, encryptedNumber):
        cipher = encryptedNumber.enc_value
        decrypt_to_p = (self.l_function(powmod(cipher, self.p-1, self.psquare), self.p) * self.hp) % self.p
        decrypt_to_q = (self.l_function(powmod(cipher, self.q-1, self.qsquare), self.q) * self.hq) % self.q
        plain = self.crt(decrypt_to_p, decrypt_to_q)
        
        if plain > self.public_key.max_int:
            plain -= self.public_key.n
        return plain
    
    def l_function(self, x, p):
        """Computes the L function as defined in Paillier's paper. That is: L(x,p) = (x-1)/p"""
        return (x - 1) // p
    
    def crt(self, mp, mq):
        """The Chinese Remainder Theorem as needed for decryption. 
           Returns the solution modulo n=pq.
        
        Args:
           mp(int): the solution modulo p.
           mq(int): the solution modulo q.
        """
        u = (mq - mp) * self.p_inverse % self.q
        return mp + (u * self.p)
    
    def h_function(self, x, xsquare):
        """Computes the h-function as defined in Paillier's paper page 12, 
        'Decryption using Chinese-remaindering'.
        """
        return invert(self.l_function(powmod(self.public_key.g, x - 1, xsquare),x), x)

    # labDecrypt is implemented for the specific functionality(protocol)
    # For general usage, these might be needed to be modified
    def labDecrypt(self, cipher):
        if isinstance(cipher, LabEncDataType1):
            return space_mapping(cipher.hm + self.decrypt(cipher.enc_mask), self.public_key.n)
        else:
            print("cipher data type error in labDecrypt()")
            assert False
    

class PublicKey(object):
    def __init__(self, n):
        self.g = n + 1
        self.n = n
        self.nsquare = n * n
        self.max_int = n // 2

    def __repr__(self):
        nsquare = self.nsquare.to_bytes(1024, 'big')
        g = self.g.to_bytes(1024, 'big')
        publicKeyHash = hashlib.sha1(nsquare + g).hexdigest()
        return "<PaillierPublicKey {}>".format(publicKeyHash[:10])

    def getSize(self):
        return self.n.bit_length()

    #for DataOwner class
    def labEncrypt(self, seed, label, plain,sigma):
        # compute mask[b](b belong to Z(n))
        mask = PRF(seed, label, self.n)
        
        # hidden message = plain - b mod pk.n, 
        hidden_message = space_mapping(plain - mask, self.n)
        
        # enc_mask = Enc(b)
        enc_mask = self.encrypt(mask)
        
        return LabEncDataType1(hidden_message, enc_mask,sigma)
    
    def encrypt(self, plain):
        #assert isinstance(plain, int), "plaintext should be an integer"
        assert abs(plain) <= self.max_int, "abs(plain) > self.max_int"
        
        # if -N/2 < plaintext < 0, then map plaintext into [N/2, N].
        if plain < 0: 
            plain += self.n

        # encryption
        encoded_plain = (self.n * plain + 1) % self.nsquare
        r = random.randrange(self.n)
        e_value = (encoded_plain * powmod(r, self.n, self.nsquare)) % self.nsquare

        return EncryptedNumber(self, e_value)
    

class EncryptedNumber(object):
    def __init__(self, publicKey, enc_value):
        self.public_key = publicKey
        self.enc_value = enc_value
        
        
    def __add__(self, other):        
        if isinstance(other, EncryptedNumber):
            result = (self.enc_value * other.enc_value) % self.public_key.nsquare
            return EncryptedNumber(self.public_key, result)  
        elif isinstance(other, LabEncDataType1):
            return other + self  
        else:  #scalar
            #result = (self.enc_value * powmod(self.g, other, self.nsquare)) % self.nsquare
            if other < 0:
                other += self.public_key.n  
            other_encode = (self.public_key.n * other + 1) % self.public_key.nsquare
            result = (self.enc_value * other_encode) % self.public_key.nsquare
            return EncryptedNumber(self.public_key, result)    

    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        #assert isinstance(other, int) #scalar
        result = powmod(self.enc_value, other, self.public_key.nsquare)
        return EncryptedNumber(self.public_key, result)    
    
    def __sub__(self, other):
        return self + (other * -1)

    def __rsub__(self, other):
        return other + (self * -1)

    def getSize(self):
        return self.enc_value.bit_length()



class LabEncDataType1(object):
    def __init__(self, hidden_message, enc_mask,sigma):
        self.hm = hidden_message
        self.enc_mask = enc_mask
        self.sigma=sigma
        
    def __repr__(self):
        pub_repr = repr(self.enc_mask.public_key)
        return "<LabEncDataType1 with {}>".format(pub_repr)

    def getSize(self):
        return self.hm.bit_length() + self.enc_mask.getSize()
        
    # homomorphic operation are implemented only for the specific protocol.
    # For the general usage, these might be required to be modified
    def __add__(self, other):
        # other should be one of (int, type1, type2)
        if isinstance(other, LabEncDataType1):
            return LabEncDataType1(self.hm + other.hm, self.enc_mask + other.enc_mask,self.sigma)
        elif isinstance(other, int):
            return LabEncDataType1(self.hm + other, self.enc_mask,self.sigma)
        elif isinstance(other, EncryptedNumber): #enc-type2
            return other + self.hm  # Enc(m2-b2) + Enc(m1-b1)
        else:
            print("type(other) :",type(other))
            assert False, "Datatype(other) error during LabEncData addition"
                    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        # other should be one of (int, type1)LabEncDataType1
        if isinstance(other, LabEncDataType1):
            return other.enc_mask*self.hm + self.enc_mask*other.hm + space_mapping(self.hm * other.hm, self.enc_mask.public_key.n)
        elif isinstance(other, int):
            return LabEncDataType1(self.hm * other, self.enc_mask * other,self.sigma)
        else:
            print("type(other) :",type(other))
            assert False, "Datatype(other) error during LabEncData multiplication"

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __sub__(self, other):
        return self + (other * -1)

    def __rsub__(self, other):
        return other + (self * -1)  



def labGen(key_length):
    # return mpk(master PublicKey), msk(master SecretKey)
    return generate_keypair(n_length=key_length)


def localGen(mpk):
    # sample seed(belongs to Z(N/2))
    seed = int(random.randrange(mpk.n) - mpk.max_int)
    return seed,mpk.encrypt(seed)


def generate_keypair(n_length=1024):
    p = q = n = None
    n_len = 0
    while n_len != n_length:
        p = getprimeover(n_length // 2)
        q = p
        while q == p:
            q = getprimeover(n_length // 2)
        n = p * q
        n_len = n.bit_length()
        
    public_key = PublicKey(n)

    return public_key, SecretKey(public_key, p, q)


def invert(a, b):
    """
    return int: x, where a * x == 1 mod b
    """
    return int(gmpy2.invert(a, b))
    

def powmod(a, b, c):
    """
    return int: (a ** b) % c
    """
    return int(gmpy2.powmod(a, b, c))


def getprimeover(bits_length):
    randfunc = random.SystemRandom()
    r = gmpy2.mpz(randfunc.getrandbits(bits_length))
    r = gmpy2.bit_set(r, bits_length - 1)
    return int(gmpy2.next_prime(r))
