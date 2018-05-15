//////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2003-2012 Daniel Vik
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
//
//////////////////////////////////////////////////////////////////////////////

#include "Crc32.h"

// If INVERSE_CRC is set, the algorithm returns the inverse CRC. This is the
// normal behavior. Some implementations does not inverse the CRC. Uncomment
// the define if the latter is the desired behavior.

#define INVERSE_CRC

//////////////////////////////////////////////////////////////////////////////
// Macros used for reverse CRC to ASCII. These macros allows characters
// A-Z, a-z, and 0-9 to be part of the patch string. 
//////////////////////////////////////////////////////////////////////////////

#define TO_CHAR(a) ((a) < 10 ? (a) + '0' : (a) < 36 ? ((a) - 10 + 'A') : (a) - 36 + 'a')
#define IS_CHAR(a) (((a) >= '0' && (a) <= '9') || ((a) >= 'A' && (a) <= 'Z') || ((a) >= 'a' && (a) <= 'z'))


#ifdef INVERSE_CRC
#define INV(x) ~(x)
#else
#define INV(x) (x)
#endif

//////////////////////////////////////////////////////////////////////////////
// CRC lookup table
//////////////////////////////////////////////////////////////////////////////

UInt32 Crc32::crc32Table[256] =
{
	0x00000000, 0x77073096, 0xee0e612c, 0x990951ba,
	0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,
	0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988,
	0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,
	0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de,
	0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
	0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec,
	0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,
	0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172,
	0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,
	0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940,
	0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
	0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116,
	0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,
	0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924,
	0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,

	0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a,
	0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
	0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818,
	0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,
	0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e,
	0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,
	0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c,
	0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
	0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2,
	0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,
	0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0,
	0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,
	0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086,
	0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
	0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4,
	0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,

	0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a,
	0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,
	0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8,
	0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
	0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe,
	0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,
	0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc,
	0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,
	0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252,
	0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
	0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60,
	0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,
	0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236,
	0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,
	0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04,
	0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,

	0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a,
	0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,
	0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38,
	0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,
	0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e,
	0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
	0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c,
	0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,
	0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2,
	0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,
	0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0,
	0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
	0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6,
	0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,
	0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94,
	0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d,
};

int Crc32::reverseCrc32Table[256] =
{
    0x00, 0x41, 0xc3, 0x82, 0x86, 0xc7, 0x45, 0x04,
    0x4d, 0x0c, 0x8e, 0xcf, 0xcb, 0x8a, 0x08, 0x49,
    0x9a, 0xdb, 0x59, 0x18, 0x1c, 0x5d, 0xdf, 0x9e,
    0xd7, 0x96, 0x14, 0x55, 0x51, 0x10, 0x92, 0xd3,
    0x75, 0x34, 0xb6, 0xf7, 0xf3, 0xb2, 0x30, 0x71,
    0x38, 0x79, 0xfb, 0xba, 0xbe, 0xff, 0x7d, 0x3c,
    0xef, 0xae, 0x2c, 0x6d, 0x69, 0x28, 0xaa, 0xeb,
    0xa2, 0xe3, 0x61, 0x20, 0x24, 0x65, 0xe7, 0xa6,

    0xea, 0xab, 0x29, 0x68, 0x6c, 0x2d, 0xaf, 0xee,
    0xa7, 0xe6, 0x64, 0x25, 0x21, 0x60, 0xe2, 0xa3,
    0x70, 0x31, 0xb3, 0xf2, 0xf6, 0xb7, 0x35, 0x74,
    0x3d, 0x7c, 0xfe, 0xbf, 0xbb, 0xfa, 0x78, 0x39,
    0x9f, 0xde, 0x5c, 0x1d, 0x19, 0x58, 0xda, 0x9b,
    0xd2, 0x93, 0x11, 0x50, 0x54, 0x15, 0x97, 0xd6,
    0x05, 0x44, 0xc6, 0x87, 0x83, 0xc2, 0x40, 0x01,
    0x48, 0x09, 0x8b, 0xca, 0xce, 0x8f, 0x0d, 0x4c,

    0x95, 0xd4, 0x56, 0x17, 0x13, 0x52, 0xd0, 0x91,
    0xd8, 0x99, 0x1b, 0x5a, 0x5e, 0x1f, 0x9d, 0xdc,
    0x0f, 0x4e, 0xcc, 0x8d, 0x89, 0xc8, 0x4a, 0x0b,
    0x42, 0x03, 0x81, 0xc0, 0xc4, 0x85, 0x07, 0x46,
    0xe0, 0xa1, 0x23, 0x62, 0x66, 0x27, 0xa5, 0xe4,
    0xad, 0xec, 0x6e, 0x2f, 0x2b, 0x6a, 0xe8, 0xa9,
    0x7a, 0x3b, 0xb9, 0xf8, 0xfc, 0xbd, 0x3f, 0x7e,
    0x37, 0x76, 0xf4, 0xb5, 0xb1, 0xf0, 0x72, 0x33,

    0x7f, 0x3e, 0xbc, 0xfd, 0xf9, 0xb8, 0x3a, 0x7b,
    0x32, 0x73, 0xf1, 0xb0, 0xb4, 0xf5, 0x77, 0x36,
    0xe5, 0xa4, 0x26, 0x67, 0x63, 0x22, 0xa0, 0xe1,
    0xa8, 0xe9, 0x6b, 0x2a, 0x2e, 0x6f, 0xed, 0xac,
    0x0a, 0x4b, 0xc9, 0x88, 0x8c, 0xcd, 0x4f, 0x0e,
    0x47, 0x06, 0x84, 0xc5, 0xc1, 0x80, 0x02, 0x43,
    0x90, 0xd1, 0x53, 0x12, 0x16, 0x57, 0xd5, 0x94,
    0xdd, 0x9c, 0x1e, 0x5f, 0x5b, 0x1a, 0x98, 0xd9
};

//////////////////////////////////////////////////////////////////////////////
// Storage for patch bytes
//////////////////////////////////////////////////////////////////////////////

UInt8 Crc32::patchBytes[4];
char  Crc32::patchChars[7];


//////////////////////////////////////////////////////////////////////////////
// Constructor. Initializes CRC object
//////////////////////////////////////////////////////////////////////////////

Crc32::Crc32() : crc_(INV(0))
{
}


//////////////////////////////////////////////////////////////////////////////
// Destructor
//////////////////////////////////////////////////////////////////////////////

Crc32::~Crc32()
{
}


//////////////////////////////////////////////////////////////////////////////
// Calculate lookup tables for any polynomial. The default tables use the
// polynomial 0x04c11db7.
//////////////////////////////////////////////////////////////////////////////
void Crc32::CalculateTables(UInt32 polynomial)
{
    // Create CRC lookup table
    for(int i = 0; i < 256; i++) {
        crc32Table[i] = Reflect(i, 8) << 24;
        for (int j = 0; j < 8; j++) {
            crc32Table[i] = (crc32Table[i] << 1) ^ (crc32Table[i] & (1 << 31) ? 
                            polynomial : 0);
        }
        crc32Table[i] = Reflect(crc32Table[i], 32);
    }
    
    // Create reverse CRC lookup table
    for (int j = 0; j < 256; j++) {
        for (int i = 0; i < 256; i++) {
            if ((j ^ (crc32Table[i] >> 24)) == 0) {
                reverseCrc32Table[j] = i;
                break;
            }
        }
    }
}


//////////////////////////////////////////////////////////////////////////////
// Helper method to reflect a value, i.e. swap positions of bits 0 and 7,
// 1 and 6, etc.
//////////////////////////////////////////////////////////////////////////////
UInt32 Crc32::Reflect(UInt32 value, int count)
{
    for(int i = 0; i < count / 2; i++) {
        UInt32 tmp = ((value >> i) ^ (value >> (count - 1 - i))) & 1;
        value ^= ((tmp << i) | (tmp << (count - 1 - i)));
    }
    return value;
} 


//////////////////////////////////////////////////////////////////////////////
// Appends data to the CRC object. The CRC hash is updated with CRC
// calculations of the provided buffer.
//////////////////////////////////////////////////////////////////////////////

void Crc32::append(const void* buffer, UInt32 size)
{
    const UInt8* ptr = (const UInt8*)buffer;
    crc_ = INV(crc_);

    while (size--) {
    	crc_ = (crc_ >> 8) ^ crc32Table[*ptr++ ^ (crc_ & 0xff)];
    }
    
    crc_ = INV(crc_);
}


//////////////////////////////////////////////////////////////////////////////
// Appends a byte to the CRC object. The CRC hash is updated with CRC
// calculations of the provided value.
//////////////////////////////////////////////////////////////////////////////

void Crc32::append(UInt8 value)
{
    crc_ = INV(crc_);
    crc_ = (crc_ >> 8) ^ crc32Table[value ^ (crc_ & 0xff)];
    crc_ = INV(crc_);
}


//////////////////////////////////////////////////////////////////////////////
// Finds reverse CRC patch bytes. The method returns four bytes that
// can be appended to the CRC in order to get the desired CRC
//////////////////////////////////////////////////////////////////////////////

const UInt8* Crc32::findReverse(UInt32 desiredCrc) const
{
    int crcIdx[4];
    
    UInt32 iterCrc = INV(desiredCrc);
    for (int j = 3; j >= 0; j--) {
        crcIdx[j] = reverseCrc32Table[iterCrc >> 24];
        iterCrc = (iterCrc ^ crc32Table[crcIdx[j]]) << 8;
    }

    UInt32 crc = INV(crc_);
    for (int j = 0; j < 4; j++) {
        patchBytes[j] = (crc ^ crcIdx[j]) & 0xff;
    	crc = (crc >> 8) ^ crc32Table[patchBytes[j] ^ (crc & 0xff)];
    }

    return patchBytes;
}

//////////////////////////////////////////////////////////////////////////////
// Finds reverse CRC patch bytes. The method returns eight ASCII characters
// (a-z,A-Z,0-9) that can be appended to the CRC in order to get the desired 
// CRC.
//////////////////////////////////////////////////////////////////////////////

const char* Crc32::findReverseAscii(UInt32 desiredCrc) const
{
    Crc32 crc32;

    for (int a = 0; a < 62; a++) {
        for (int b = 0; b < 62; b++) {
            crc32.set(crc_);
            crc32.append(TO_CHAR(a));
            crc32.append(TO_CHAR(b));
            const UInt8* reverse = crc32.findReverse(desiredCrc);

            // If the reverse CRC has valid ASCII characters, we found a solution.           
            if (IS_CHAR(reverse[0]) && IS_CHAR(reverse[1]) && 
                IS_CHAR(reverse[2]) && IS_CHAR(reverse[3])) {
                patchChars[0] = (char)TO_CHAR(a);
                patchChars[1] = (char)TO_CHAR(b);
                patchChars[2] = (char)reverse[0];
                patchChars[3] = (char)reverse[1];
                patchChars[4] = (char)reverse[2];
                patchChars[5] = (char)reverse[3];
                patchChars[6] = 0;
                return patchChars;
            }
        }
    }

    return "";
}


//////////////////////////////////////////////////////////////////////////////
// Sets a new CRC hash value
//////////////////////////////////////////////////////////////////////////////

void Crc32::set(UInt32 crc)
{
    crc_ = crc;
}


//////////////////////////////////////////////////////////////////////////////
// Gets current CRC hash value
//////////////////////////////////////////////////////////////////////////////

UInt32 Crc32::get() const
{
    return crc_;
}
