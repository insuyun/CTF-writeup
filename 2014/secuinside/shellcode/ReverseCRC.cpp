#include <stdio.h>
#include "Crc32.h"
#include <stdlib.h>

void testOne(UInt32 startCrc, UInt32 wantedCrc)
{
    Crc32 crc;
    
    crc.set(startCrc);

    const UInt8* patch = crc.findReverse(wantedCrc);
    crc.append(patch, 4);

    printf("    initial: 0x%.8x %s -  bytes to add: { 0x%.2x, 0x%.2x, 0x%.2x, 0x%.2x }\n", 
           startCrc, (wantedCrc == crc.get() ? "OK  " : "FAIL"),
           patch[0], patch[1], patch[2], patch[3]);
}

void testMany(UInt32 wantedCrc, UInt32 count)
{
    UInt32 startCrc = 7;

    printf("\n\nCRC Test - Wanted output: 0x%.8x\n\n", wantedCrc);
    for (UInt32 i = 0; i < count; ++i) {
        testOne(startCrc, wantedCrc);
        startCrc *= 51;
    }
}

void testOneAscii(UInt32 startCrc, UInt32 wantedCrc)
{
    Crc32 crc;
    
    crc.set(startCrc);

    const char* patch = crc.findReverseAscii(wantedCrc);
    crc.append(patch, 6);

    printf("    initial: 0x%.8x %s -  string to add: %s\n",  
           startCrc, (wantedCrc == crc.get() ? "OK  " : "FAIL"), patch);
}

void testManyAscii(UInt32 wantedCrc, UInt32 count)
{
    UInt32 startCrc = 7;

    printf("\n\nCRC Test ASCII - Wanted output: 0x%.8x\n\n", wantedCrc);
    for (UInt32 i = 0; i < count; ++i) {
        testOneAscii(startCrc, wantedCrc);
        startCrc *= 51;
    }
}
int main(int argc, char** argv)
{
	char   *ptr;
	long    value;

	Crc32 crc;
	UInt32 start = strtoul( argv[1], &ptr, 16);
	UInt32 target = strtoul( argv[2], &ptr, 16);

	crc.set(start);
	const UInt8* patch = crc.findReverse(target);

	crc.append(patch, 4);

	int i;
	for(i =0; i < 4; i ++)
		printf("%02x", patch[i]);


    return 0;
}
