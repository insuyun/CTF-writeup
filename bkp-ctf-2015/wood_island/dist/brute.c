#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
int main(int argc, char** argv)
{
  unsigned char ibuf[21];
  unsigned char obuf[20];
  unsigned int i, j;
  memset(ibuf, 'a', sizeof(ibuf) - 1);
  ibuf[20] = 0;
  memcpy(ibuf, argv[1], strlen(argv[1]));
  char end = 0x77;
  char start = 0x30;

  char a, b, c, d, e;

  for(a = 0x41; a < 0x7a; a++)
  {
    ibuf[15] = a;
    for(b = 0x41; b < 0x7a; b++)
    {
      ibuf[16] = b;
      for (c = 0x41; c < 0x7a; c++)
      {
        ibuf[17] = c;
        for (d  = 0x41; d < 0x7a; d++)
        {
          ibuf[18] = d;
          for (e = 0x41; e < 0x7a; e++)
          {
            ibuf[19] = e;

            SHA1(ibuf, sizeof(ibuf) - 1, obuf);
            if (obuf[19] == 0xff && obuf[18] == 0xff && obuf[17] == 0xff)
            {
              printf("%d\n", obuf[19]);
              printf("%s", ibuf);
              return;
            }

          }
        }
      }
    }
  }

}
