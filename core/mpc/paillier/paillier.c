/**
 * Main file to simulate paillier encryption/decrytion and computation with
 * encrypted data. This is not meant to be used for anything outside
 * educational purposes and I take no responsibility for any silliniess caused
 * by using this.
 *
 * Author: Channa Dias Perera <cdiasperera@gmail.com> 
 */

/*
 * Primes choosen in advance. The purpose of this project is to simulate
 * the encryption so small primes are chosen
 */
#define PRIME_1 3
#define PRIME_2 5

#include <stdio.h>
#include "keyGeneration.h"
#include "encryption.h"

int main() {

    // Primes used for the encryption
    int p = PRIME_1;
    int q = PRIME_2;

    // Generate public/private keys
    int publicKey = p*q;

    int privateKeyLambda = calculateLambda(p, q);

    int privateKeyMu = calculateMu(privateKeyLambda, p, q);

    // Encrypt two plain text number   
    int plainTxt1 = 2;
    int plainTxt2 = 3;

    // Have to pick r such that gdc(r,publicKey) = 1, r < N 
    int r = 2;

    int cypherTxt1 = encrypt(plainTxt1, r, publicKey);
    int cypherTxt2 = encrypt(plainTxt2, r, publicKey);

    int decryptTxt1 = decrypt(cypherTxt1, privateKeyMu, privateKeyLambda,
            publicKey);
    int decryptTxt2 = decrypt(cypherTxt2, privateKeyMu, privateKeyLambda,
            publicKey);

    int plainAdd = cypherAdd(cypherTxt1, cypherTxt2, privateKeyMu, 
            privateKeyLambda, publicKey);




    // Print out log of experiment
    printf("p=%d, q=%d\n", p, q);
    printf("publicKey: %i\n",publicKey);
    printf("privateKeyLambda: %i\n", privateKeyLambda);
    printf("privateKeyMu: %i\n", privateKeyMu);
    printf("plainTxt1 = %d\n", plainTxt1);
    printf("plainTxt2 = %d\n", plainTxt2);
    printf("decryptTxt1 = %d\n", decryptTxt1);
    printf("decryptTxt2 = %d\n", decryptTxt2);
    printf("plainAdd = %d\n", plainAdd);   

    return 0;
}
