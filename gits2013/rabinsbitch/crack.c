#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
int main(int argc, char** argv)
{
		unsigned char ibuf[21];
		unsigned char obuf[20];
		unsigned int i, j;
		memset(ibuf, 0, sizeof(ibuf));
		memcpy(ibuf, argv[1], 16);

		for(i = 0; i < 0xffffffff; i++)
		{
				*(int*)(ibuf + 17) = i;
				for(j = 0; j < 256; j++)
				{
						*(ibuf + 16) = j;

						SHA1(ibuf, sizeof(ibuf), obuf);

						if(obuf[19] == 0xff && obuf[18] == 0xff && obuf[17] == 0xff && (obuf[16] & 3) == 3)
						{
								for (i = 0; i < 21; i++) {
										printf("%02x", ibuf[i]);
								}

								return;
						}
				}
		}

		printf("Cannot find");
}

