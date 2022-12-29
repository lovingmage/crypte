/**
 * Function headers  to encrypt/decrypt plaintext numbers for paillier 
 * encryption
 */

#include <math.h>

int encrypt(int t, int r, int N);

int decrypt(int c, int mu, int lambda, int N);

int cypherAdd(int c1, int c2, int mu, int lambda, int N);
