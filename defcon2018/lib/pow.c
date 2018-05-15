// gcc poc.c -o poc -lssl -lcrypto
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "openssl/sha.h"
#include <byteswap.h>


char buf[0x100];

int do_hash(char *pre, uint64_t post, char *hash) {
    int len = strlen(pre);
    memcpy(buf, pre, len);
    memcpy(buf+len, &post, 8);
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, buf, len+8);
    SHA256_Final(hash, &sha256);
}

int main(int argc, char **argv) {
    if (argc < 3) exit(0);
    int n = atoi(argv[2]);
    char *pre = argv[1];

    uint64_t cand = 0;
    uint64_t hash[4];
    while(1) {
        do_hash(pre, cand, (char *)hash);
        if (!(__bswap_64(hash[3]) & ((1 << n) - 1))) {
            printf("%ld\n", cand);
            exit(0);
        }
        cand += 1;
    }
}
