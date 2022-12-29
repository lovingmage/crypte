
import random
import sys
import math
import os
import gmpy2
import time
 
class SecretKey(object):
    def __init__(self, public_key, p, q):
        assert p*q == public_key.n, "given public key does not match the given p and q."
        self.public_key = public_key
        if q < p: #ensure that p < q. 
            self.p = q
            self.q = p
        else:
            self.p = p
            self.q = q
          
        # variables for using CRT
        self.psquare = self.p * self.p
        self.qsquare = self.q * self.q
        self.p_inverse = invert(self.p, self.q)
        self.hp = self.h_function(self.p, self.psquare);
        self.hq = self.h_function(self.q, self.qsquare);

    def __repr__(self):
        pub_repr = repr(self.public_key)
        return "<PaillierPrivateKey for {}>".format(pub_repr)
    
    def decrypt(self, encryptedNumber):
        """
        Decryption algorithm using CRT(Chinese Remainder Theorem)
        """
        cipher = encryptedNumber.enc_value
        decrypt_to_p = (self.l_function(powmod(cipher, self.p-1, self.psquare), self.p) * self.hp) % self.p
        decrypt_to_q = (self.l_function(powmod(cipher, self.q-1, self.qsquare), self.q) * self.hq) % self.q
        plain = self.crt(decrypt_to_p, decrypt_to_q)
        
        if plain > self.public_key.max_int:
            plain -= self.public_key.n
        return plain
    
    def l_function(self, x, p):
        """
        Computes the L function as defined in Paillier's paper. L(x,p) = (x-1)/p
        """
        return (x - 1) // p
    
    def crt(self, mp, mq):
        """
        The Chinese Remainder Theorem as needed for decryption.
        Returns the solution modulo n=pq.
        
        Args:
           mp(int): the solution modulo p.
           mq(int): the solution modulo q.
        """
        u = (mq - mp) * self.p_inverse % self.q
        return mp + (u * self.p)
    
    def h_function(self, x, xsquare):
        """
        Computes the h-function as defined in Paillier's paper page 12, 
        'Decryption using Chinese-remaindering'.
        """
        return invert(self.l_function(powmod(self.public_key.g, x - 1, xsquare),x), x)
    

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
    
    def encrypt(self, plain):
        """
        Ecryption algorithm 
        """
        # check plaintext type
        assert isinstance(plain, int), "plaintext should be an integer"
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
        self.pk = publicKey
        self.enc_value = enc_value
        
    def __add__(self, other):
        # Enc(a) + Enc(b)
        if isinstance(other, EncryptedNumber):
            result = (self.enc_value * other.enc_value) % self.pk.nsquare
            return EncryptedNumber(self.pk, result)    

        # Enc(a) + b
        else:  
            #assert abs(other) <= self.pk.max_int
            if other < 0:
                other += self.pk.n
            other_encode = (self.pk.n * other + 1) % self.pk.nsquare
            result = (self.enc_value * other_encode) % self.pk.nsquare
            return EncryptedNumber(self.pk, result)    

    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        #assert isinstance(other, int) #scalar
        result = powmod(self.enc_value, other, self.pk.nsquare)
        return EncryptedNumber(self.pk, result)    
    
    def __sub__(self, other):
        return self + (other * -1)

    def __rsub__(self, other):
        return other + (self * -1)


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


def getprimeover(bits_length):
    randfunc = random.SystemRandom()
    r = gmpy2.mpz(randfunc.getrandbits(bits_length))
    r = gmpy2.bit_set(r, bits_length - 1)
    return int(gmpy2.next_prime(r))


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
