//////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2003-2010 Daniel Vik
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

#ifndef CRC32_H
#define CRC32_H

typedef unsigned char UInt8;
typedef unsigned int UInt32;

class Crc32
{
public:
    Crc32();
    ~Crc32();

    // Calculate CRC tables based on a polynomial. (Default values for the
    // tables are provided in the implementation. They are based on the 
    // polynomial 0x04c11db7, used in e.g. PKZip, WinZip and Ethernet.
    static void CalculateTables(UInt32 polynomial = 0x04c11db7);

    // Add data to CRC
    void append(UInt8 value);
    void append(const void* buffer, UInt32 size);
    
    // Find reverse CRC patch
    const UInt8* findReverse(UInt32 desiredCrc) const;
    
    // Find reverse CRC patch
    const char* findReverseAscii(UInt32 desiredCrc) const;

    // Accessor methods
    void set(UInt32 crc);
    UInt32 get() const;

private:
    static UInt32 Reflect(UInt32 value, int count);

    static UInt32 crc32Table[256];
    static int reverseCrc32Table[256];
    
    static UInt8 patchBytes[4];
    static char patchChars[7];

    UInt32 crc_;
    
    // Not implemented
    void operator=(const Crc32&);
    Crc32(const Crc32&);
};


#endif /*CRC_H*/
