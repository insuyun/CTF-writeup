#define BLOCK_SIZE 16
#include <openssl/aes.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
 #include <sys/types.h>
 #include <sys/stat.h>
 #include <fcntl.h>

int count = 0;
#define TARGET "\xcf\xe6\xc3\xd5\x82\xc6"
// #define TARGET "\xFA\x59\xCA\x34\x2B\x2E"
// #define TARGET "\xe9\x2b\x23\xd9\xec\x34"
//#define TARGET "\xef\x77\x85\x2b\x0a\x6b"
#define TARGET1 "\xcf\xe6\xc3\xd5\x82\xc6"
#define TARGET2 "\xaf\xcf\xec\xd2\x1a\x8d"
#define TARGET3 "\x77\x40\x56\x0a\x1d\x64"
#define TARGET4 "\x00\x00\x00\x00\x00\x00"
unsigned char key[16];

void brute(unsigned char* buf, int depth) {
  if (depth == 7) {
    /*
    for (int i = 0; i < 16; i++) {
      printf("%02X", buf[i]);
    }
    printf("\n");
    */

    AES_KEY enc_key;
    unsigned char out[BLOCK_SIZE];

    AES_set_encrypt_key(key, 128, &enc_key);
    AES_encrypt(buf, out, &enc_key);

    if (!memcmp(&out[10], TARGET1, 6) ||
        !memcmp(&out[10], TARGET2, 6) ||
        !memcmp(&out[10], TARGET3, 6) ||
        !memcmp(&out[10], TARGET4, 6)) {
      printf("FOUND!\n");
      for (int i = 0; i < 16; i++) {
        printf("%02X", buf[i]);
      }
      printf("\n");
      exit(0);
    }
  }
  else {
    for (int i = 0; i < 256; i++) {
      buf[depth] = i;
      brute(buf, depth + 1);
    }
  }
}

int main(int argc, char **argv)
{
  memset(key, 0, sizeof(key));
  unsigned char buf[16];
  memset(buf, 0, sizeof(buf));

  int fd = open("/dev/urandom", 0);
  read(fd, buf, 10);
  close(fd);

  brute(buf, 0);
}

