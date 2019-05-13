#include <openssl/pem.h>
#include <assert.h>
#include <string.h>

#if OPENSSL_VERSION_NUMBER < 0x10100005L
static void RSA_get0_key(const RSA *r,
    const BIGNUM **n, const BIGNUM **e, const BIGNUM **d)
{
  if (n != NULL)
    *n = r->n;
  if (e != NULL)
    *e = r->e;
  if (d != NULL)
    *d = r->d;
}

#endif

int main(int argc, char** argv) {
  char * dir = argv[1];
  char buf[0x1000];
  char filename[0x100];
  EVP_PKEY* pkey = EVP_PKEY_new();
  sprintf(filename, "%s/PUB", dir);
  FILE* fp = fopen(filename, "r");
  assert(fp != NULL);
  RSA* rsa = PEM_read_RSA_PUBKEY(fp, NULL, NULL, NULL);
  const BIGNUM *n;
  const BIGNUM *e;
  RSA_get0_key(rsa, &n, &e, 0);
  printf("n: %s\n", BN_bn2dec(n));

  // read pd
  BIGNUM *pd = BN_new();
  memset(buf, 0, sizeof(buf));
  sprintf(filename, "%s/PD", dir);
  fp = fopen(filename, "r");
  assert(fp != NULL);
  fgets(buf, sizeof(buf), fp);
  fclose(fp);
  BN_dec2bn(&pd, buf);
  printf("pd: %s\n", BN_bn2dec(pd));

  // read bit
  int bit = 0;
  memset(buf, 0, sizeof(buf));
  sprintf(filename, "%s/BIT", dir);
  fp = fopen(filename, "r");
  assert(fp != NULL);
  fgets(buf, sizeof(buf), fp);
  bit = atoi(buf);
  fclose(fp);
  printf("bit: %d\n", bit);

  char* e_10 = BN_bn2dec(e);
  int e_int = atoi(e_10);
  BIGNUM *b_2 = BN_new();
  BN_dec2bn(&b_2, "2");

  BIGNUM* b_1 = BN_new();
  BN_dec2bn(&b_1, "1");

  for (int gcd = 2; gcd < 1000; gcd++) {
    char buf[0x100];
    sprintf(buf, "%d", gcd);
    BIGNUM *b_gcd = BN_new();
    BN_dec2bn(&b_gcd, buf);

    for (int k_int = 0; k_int <= e_int; k_int++) {
      if ((k_int % 0x1000) == 0)
        fprintf(stderr, "%d %d\n", gcd, k_int);

      BN_CTX *ctx = BN_CTX_new();
      char kbuf[0x100];
      BIGNUM *k = BN_CTX_get(ctx);
      sprintf(kbuf, "%d", k_int);
      BN_dec2bn(&k, kbuf);

      BIGNUM *denom = BN_CTX_get(ctx);
      BN_mul(denom, b_gcd, b_2, ctx);

      // d_a = (k * N / gcd + 1) / e
      BIGNUM *phi_g = BN_CTX_get(ctx);
      BN_div(phi_g, NULL, n, denom, ctx);

      BIGNUM* t = BN_CTX_get(ctx);
      BN_mul(t, k, phi_g, ctx);

      BN_add(t, t, b_1);

      BIGNUM* d_h = BN_CTX_get(ctx);
      BN_div(d_h, NULL, t, e, ctx);

      BN_rshift(d_h, d_h, bit);
      BN_lshift(d_h, d_h, bit);

      // d = t | pd
      BIGNUM *d = BN_CTX_get(ctx);
      BN_add(d, d_h, pd);

      BN_mul(t, e, d, ctx);

      BIGNUM *t2 = BN_CTX_get(ctx);
      BN_mod_exp(t2, b_2, t, n, ctx);

      if (!BN_cmp(t2, b_2)) {
        printf("Found: %s, %s", dir, BN_bn2dec(d));
        exit(-1);
      }

next:
      BN_CTX_free(ctx);
    }
    BN_free(b_gcd);
  }

  BN_free(pd);
  EVP_PKEY_free(pkey);
}
