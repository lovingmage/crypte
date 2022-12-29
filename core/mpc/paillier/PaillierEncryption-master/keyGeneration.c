/**
 * Functions to generate keys for encryption
 */

#include <stdio.h>
#include "keyGeneration.h"

int calculateLambda(int p, int q) {

    int a = p - 1;
    int b = q -1;

    // Find LCM of a and b
   
    // Start search for LCM from p or q, whichever is greater

    int i;

    if (a < b) {
        i = b;
    } else {
        i = a;
    }

    while (i < MAX_ITER) {
        if ((i % a == 0) && (i % b == 0)) {
            // Found lCM
            return i;
        }
        i++;
    }

    return 0;
}

int calculateMu(int lambda, int p, int q) {

    // Find mu = lamba^-1 (mod p*q)
    /** We do this iteratively by testing all numbers from 1 to pq to see if
     * it satifies the criteria: mu * lambda = 1 (mod pq)
     */

    int mu;

    for (mu = 1; mu <= p*q; mu++) {
        if (((mu*lambda)% (p*q)) == 1) {
            return mu;
        }
    }
   
    // There's no inverse modulo of lambda
    return NOINVMODERR;
}

