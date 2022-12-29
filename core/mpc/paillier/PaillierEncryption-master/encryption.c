/**
 * Functions to encrypt/decrypt for paillier encryption
 */

#include "encryption.h"

#include <stdio.h>

int encrypt(int t, int r, int N) { 

    int power =(pow(N+1, t)*pow(r,N));
    return power % (N*N);
}

int decrypt(int c, int mu, int lambda, int N) {

    int power =  pow(c,lambda);

    int x = power % (N*N);

    int intermediate = (x-1)/N*mu;

    return intermediate % N;
}

int cypherAdd(int c1, int c2, int mu, int lambda, int N) {

    int wholeCypherTxt = c1*c2;

    int cypherTxt = wholeCypherTxt % (N*N);

    return decrypt(cypherTxt, mu, lambda, N);
}
