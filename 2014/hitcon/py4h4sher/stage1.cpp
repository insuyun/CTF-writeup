#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <unordered_map>

using namespace std;

char dict[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

unordered_map<uint64_t, uint32_t> table;

int fill_buffer(uint8_t* buf, uint32_t index, int size)
{
	int i;
	char ch;
	for (i = 0; i < size; i++)
	{
		ch = dict[index % 24];
		index = index / 24;
		buf[2*i] = ch;
		buf[2*i + 1] = 'a'+'z' - ch;
	}
}

static int
oldpw_rev(uint32_t *pnr, uint32_t *pnr2, uint32_t add,
        unsigned char *cc, unsigned len)
{
        uint32_t nr, nr2;
        uint32_t c, u, e, y;

        if (len == 0) {
                return 0;
        }

        nr = *pnr;
        nr2 = *pnr2;
        c = cc[len - 1];
        add -= c;

        u = nr2 - nr;
        u = nr2 - ((u << 8) ^ nr);
        u = nr2 - ((u << 8) ^ nr);
        nr2 = nr2 - ((u << 8) ^ nr);
        nr2 &= 0x7FFFFFFF;

        y = nr;
        for (e = 0; e < 64; e ++) {
                uint32_t z, g;

                z = (e + add) * c;
                g = (e ^ z) & 0x3F;
                if (g == (y & 0x3F)) {
                        uint32_t x;

                        x = e;
                        x = y ^ (z + (x << 8));

                        x = y ^ (z + (x << 8));
                        x = y ^ (z + (x << 8));
                        nr = y ^ (z + (x << 8));
                        nr &= 0x7FFFFFFF;
                        if (oldpw_rev(&nr, &nr2, add, cc, len - 1) == 0) {
                                *pnr = nr;
                                *pnr2 = nr2;
                                return 0;
                        }
                }
        }

        return -1;
}

int oldpw(uint8_t *cc, uint32_t len, uint32_t *pnr, uint32_t *pnr2)
{
	uint32_t nr = 1345345333, nr2 = 305419889;
	uint32_t add = 7, i;

	for(i = 0; i < len; i++)
	{
		char c = cc[i];
//		printf("%x %x\n", nr, nr2);
		nr ^= (((nr & 0x3f)+add)*c)+ (nr << 8) & 0xFFFFFFFF;
		nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF;
		add= (add + c) & 0xFFFFFFFF;
	}
	*pnr = nr & 0x7fffffff;
	*pnr2 = nr2 & 0x7fffffff;
//	printf("%d\n", add);
}

void make_table()
{
	int i;
	uint8_t buf[12];
	uint32_t nr, nr2;
	for (i = 0; i < 0x1000000; i++)
//	for (i = 0; i < 0x1; i++)
	{
		fill_buffer(buf,i, 6);
		oldpw(buf, 12, &nr, &nr2);
		table[((uint64_t)nr << 32)|nr2] = i;
	}
	printf("[*] Make table ended\n");
}

int main()
{
	uint64_t i;
	uint8_t buf[16];
	uint32_t nr, nr2;
	uint64_t key;

	make_table();
	for (i = 0 ; i < 0x10000000000; i++)
	{
		nr	= 0x41414141;
		nr2 = 0x41414141;
		fill_buffer(buf, i, 8);
		oldpw_rev(&nr, &nr2, 3073, buf, 16);
		key = ((uint64_t)nr << 32)|nr2;
		if (table.find(key) != table.end())
		{
			printf("[*] YES! FOUND\n");
			printf("index1 : %lld, index2 : %lld\n", table[key], i);
			exit(-1);
		}
	}
}
