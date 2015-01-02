#include <stdio.h>
#include <stdint.h>

typedef struct _RNG
{
    uint64_t a;
    uint64_t c;
    uint64_t x;
    uint64_t mod;
} RNG;

void init_rng(RNG* r, uint64_t a, uint64_t c, uint64_t x)
{
    r->a = a;
    r->c = c;
    r->x = x;
    r->mod = 0x100000000;
}

unsigned char next_rng(RNG* r)
{
    r->x = (r->x * r->a + r->c) % r->mod;
    return (r->x) >> 31;
}

unsigned char next_byte(RNG* rng)
{
    
    int i, j ;
    char ret = 0, val;
    for (i = 0; i < 8; i++)
    {
        val = 0;
        for (j = 0; j < 4; j ++)
        {
            val += next_rng(&rng[j]);
        }
        val %= 2;
        ret |= val << i;
    }
    return ret;
}

int main()
{
    RNG rng[4];
    uint32_t i, j, brute = 0;
    for (brute = 0; brute < 0xffffffff; brute++)
    {
        init_rng(&rng[0], 94321211, 1013904217, brute & 0xff);
        init_rng(&rng[1], 34321229, 1010101011, (brute >> 8) & 0xff);
        init_rng(&rng[2], 14321233,  987654321, (brute >> 16) & 0xff);
        init_rng(&rng[3], 32452843,  982451653, (brute >> 24) & 0xff);

        for (i = 0; i < 100; i ++)
        {
            for (j = 0; j < 4; j++)
                next_rng(&rng[j]);
        }

        if (next_byte(rng) == (0x89 ^ 0xb1) &&
                next_byte(rng) == (0x1d ^ 0x50) &&
                next_byte(rng) == (0xd6 ^ 0x4e) &&
                next_byte(rng) == (0xcf ^ 0x47))
        {
            printf("FOUND : %08x\n", brute);
        }
    }
}

