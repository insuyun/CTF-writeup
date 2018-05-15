#include <unordered_map>
#include <string>
#include <openssl/aes.h>
#include <stdint.h>
#include <string.h>

using namespace std;

void set_key(uint8_t* key, int value)
{
	int i;
	key[29] = value & 0xff;
	key[30] = (value >> 8) & 0xff;
	key[31] = (value >> 16) & 0xff;
}

int main()
{
	unordered_map<string, int> table;
	int i, j;
	uint8_t key[32], m1[16], m2[16], e1[16], e2[16], out[16], target[32], immediate[32], answer[33];
	AES_KEY enc_key, dec_key;
	string decrypted;

	// set initial value
	memcpy(m1, "AES-256 ECB mode", 16);
	memcpy(m2, "Each key zero un", 16);
	memcpy(e1, "Lv\xe9\x07\x86\xc4\xf3""dj\xdf\x99!zd\xd0\xd7", 16);
	memcpy(e2, "\xd3V\x19m*\xedkc~\xd6\x93\x9e""B\x9a""f<", 16);
	memcpy(target, "\xb3\x98]\xd1""8S\x92\xfdT\xe3\x8a\xfdi\x1c\x94\x85\xa5\xf9\xa8\x97\xb9\xebS\x19\xd7\xad;\xd6yo3\xd5", 32);

	memset(key, 0, sizeof(key));
	
	for (i = 0; i < 0xffffff; i++)
	{
		set_key(key, i);
		AES_set_encrypt_key(key, 256, &enc_key);
		AES_encrypt(m1, out, &enc_key);
		table[string((char*)out, 16)] = i;
	}

	for (i = 0; i < 0xffffff; i++)
	{
		set_key(key, i);
		AES_set_decrypt_key(key, 256, &dec_key);
		AES_decrypt(e1, out, &dec_key);
		decrypted = string((char*)out, 16);
		
		if (table.find(decrypted) != table.end())
		{
				printf("[*] Candidate is found\n");
				printf("[*] key1 : %d, key2 : %d\n", i, table[decrypted]);
				
				// Decrypt answer
				memset(answer, 0, sizeof(answer));

				set_key(key, i);
				AES_set_decrypt_key(key, 256, &dec_key);
				for (j = 0; j < 2; j++)
					AES_decrypt(target + 16 * j, immediate + 16 * j, &dec_key);

				set_key(key, table[decrypted]);
				AES_set_decrypt_key(key, 256, &dec_key);
				for (j = 0; j < 2; j ++)
						AES_decrypt(immediate + 16 * j, answer + 16 * j, &dec_key);			

				printf("[*] Answer : %s\n", answer);

		}
	}
}
