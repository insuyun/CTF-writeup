#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

using namespace std;
int bitXor(int, int);

int check(unsigned char* buffer)
{
	return buffer[0] == 0x89 && buffer[1] == 0x50 && buffer[2]==0x4e && buffer[3] == 0x47;
}

int main(int argc, char **argv)
{
	srand(time(NULL));
	char *path=new char[30];
	char *outPath = new char[30];
	if(argc > 1)
		path = argv[1];
	else
	{
		printf("\nenter file\n");
		scanf("%s",path);
	}
	int g = rand() % 512 + 32;
	int n = rand() % g;
	int mask = rand() % 256;

	strcpy(outPath, path);
	strcat(outPath, "_Crypted");


	FILE *inFile = fopen(path, "rb");
	FILE *outFile = fopen(outPath, "wb");

	if(inFile == NULL || outFile == NULL)
	{
			printf("Error\ncant read/write file\n");
			return 1;
	}
	unsigned char H, L;
	unsigned char *readBuffer = new unsigned char[512], *writeBuffer = new unsigned char[512];
	int len = fread(readBuffer, 1, 512, inFile);

	// assume g > 4
	for (g = 0; g < 512; g++)
	{
			for (n = 0; n < g; n++)
			{
					for (mask = 0; mask < 256; mask ++)
					{
							for(int i = 0 ; i < g ; i++)
							{
									int nIndex = i + n;
									int pIndex = i - n;
									if(nIndex >= g) 
											nIndex -= g;
									if(nIndex < 0) 
											nIndex += g;
									if(pIndex >= g) 
											pIndex -= g;
									if(pIndex < 0) 
											pIndex += g;
									H = readBuffer[nIndex] / 16;
									L = readBuffer[pIndex] % 16;
									writeBuffer[i] = bitXor(16 * H + L, mask);
							}

							if (check(writeBuffer))
							{
									printf("\nsave decryption code: %d.%d.%d\n", g, n, mask);
							}
					}
			}
	}
}
int bitXor(int x, int y)
{
    int a = x & y;
    int b = ~x & ~y;
    int z = ~a & ~b;
    return z;
}
