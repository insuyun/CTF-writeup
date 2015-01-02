#include <string.h>
#include <iostream>
#include <unordered_map>
#include <stdint.h>
#include <openssl/sha.h>
#include <openssl/md5.h>

#define LENGTH 4166

using namespace std;

unordered_map<uint64_t, uint32_t> table;
uint8_t prefix[64];
uint8_t blocks[32][2][128];

bool calculate_truncated_sha1(void* input, unsigned long length, uint64_t* value)
{
		uint8_t sha1[20];
		int i;
    SHA_CTX context;
    if(!SHA1_Init(&context))
        return false;

    if(!SHA1_Update(&context, (unsigned char*)input, length))
        return false;

    if(!SHA1_Final(sha1, &context))
        return false;

		uint8_t* ptr = (uint8_t*)value;
		for (i = 0; i < 8; i ++)
			ptr[i] = sha1[i + 12];
    
		return true;
}

void init()
{
	int i;
	int j;
	char filename[0x100];
	// Read prefix
	FILE* fp = fopen("./blocks/prefix.txt", "rb");
	if (fp == NULL)
	{
		printf("init : prefix.txt failed\n");
		exit(-1);
	}
	fread(prefix, 1, 64, fp);
	fclose(fp);

	// Read blocks
	memset(filename, 0, sizeof(filename));
	for (i = 0; i < 32; i++)
	{
		for(j = 0; j < 2; j++)
		{
			sprintf(filename, "./blocks/%d_%d", i + 1, j);
			fp = fopen(filename, "rb");
			if (fp == NULL)
			{
				printf("init : %s failed\n", filename);
				exit(-1);
			}
			fread(blocks[i][j], 1, 128, fp);
			fclose(fp);
		}
	}
}

void fill_buffer(uint8_t* buf, uint32_t index, uint32_t prev)
{
	int i = 0;
	for (i = 0; i < 32; i++)
	{
		if ( (prev & 1) != (index & 1))
			memcpy(&buf[64 + 128 * i], blocks[i][index & 1], 128);
		
		prev = prev >> 1;
		index = index >> 1;
	}
}

void print_buffer(uint8_t* buf)
{
	int i = 0;
	for(i = 0; i < LENGTH; i ++)
	{
		printf("%02X", buf[i]);
	}
	printf("\n");
}

bool print_md5(uint8_t* input)
{
	uint8_t md5[16];
	int i;
	MD5_CTX context;
	if(!MD5_Init(&context))
		return false;

	if(!MD5_Update(&context, (unsigned char*)input, LENGTH))
		return false;

	if(!MD5_Final(md5, &context))
		return false;

	for (i = 0; i < 16; i ++)
		printf("%02X", md5[i]);
	printf("\n");
	
	return true;

}

int main ()
{
  init();
	uint8_t buf[LENGTH];
	uint32_t i;
	uint64_t value;
	memset(buf, 0, LENGTH);
	memcpy(buf, prefix, 64); 
	memcpy(buf + 4160, "HITCON", 6);

	uint32_t prev = 0xffffffff;

	for(i = 0; i < 0xffffffff; i++)
	{
		fill_buffer(buf, i, prev);
		calculate_truncated_sha1(buf, LENGTH, &value);
		//print_md5(buf);
		if (table.find(value) == table.end())
		{
			// New hash
			table[value] = i;
		}
		else
		{
			printf("[*] WOOOOOOOOOOOW I found!\n");
			printf("Index1 : %d, index2 : %d\n", table[value], i);
			fill_buffer(buf, table[value], ~table[value]);
			print_buffer(buf);
			fill_buffer(buf, i, ~i);
			print_buffer(buf);
			exit(-1);
		}
		if (i % 0x10000 == 0)
			printf("%x times\n", i);

		prev = i;

//		print_md5(buf);
	}
}
