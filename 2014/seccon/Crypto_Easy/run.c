#include <stdint.h>
#include <stdio.h>
char chk_rand(char guess)
{
    char real = rand() & 0xff;
//    printf("%2X, %2X", real, guess);

    return real == guess;
}


void decrypt(int seed)
{

    char filename[0x100], ch;
    FILE *out, *in;
    srand(seed);

    sprintf(filename, "file.%8X.png", seed);
    out = fopen(filename, "wb");
    in = fopen("ecrypt1.bin", "rb");

    while(fread(&ch, 1, 1, in) == 1)
    {
        ch ^= rand();
        fwrite(&ch, 1, 1, out);
    }

    fclose(in);
    fclose(out);
}

int main()
{
    uint32_t seed;

    seed = time(NULL);
    srand(seed);
    for (seed = time(NULL); seed >= 0; seed--)
    {
//        89 50 4E 47
//        34 70 F0 2D
        srand(seed);
        //printf("%2X\n",rand());
        if (chk_rand(0x34 ^ 0x89) &&
                chk_rand(0x50 ^ 0x70) &&
                chk_rand(0x4e ^ 0xf0) &&
                chk_rand(0x47 ^ 0x2d))
        {
            printf("[*] Guessed seed : %8X\n", seed);
            decrypt(seed);
            break;
        }

        if ((seed % 0x10000) == 0)
            printf("%8X\n", seed);
    }
}
