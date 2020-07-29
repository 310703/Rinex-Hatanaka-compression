# Rinex Hatanaka compression
Use to compress Observations Rinex files (.o) to Hatanaka compression and compress them with navigation files (".n", ".g") on "zip" format".
The "zip" compress files are moved on folder for FTP Transfert.

# Sample data files
 Receiver INdependent EXchange format files contain raw satellite navigation system data relative to a specified interval of time
 
 The standard name format for RINEX files is: ssssdddh.yyt, where:

    ssss is a the marker name of the ground station where the recording was performed.
    ddd is a three digits number indicating the day of the year when the recording started.
    h is a letter indicating the hour of the day when the recording started.
    yy is a two digits number indicating the year when the recording started.
    t is a letter indicating the type of the RINEX file. Most common types are:
        .**o files: observation data files, contain satellites position data.
        .**d files: compressed observation data files.
        .**n files: navigation data files, contain GPS ephemeris data.
        .**g files: navigation data files, contain GLONASS ephemeris data.
        .**l files: navigation data files, contain GALILEO epephemeris data.

Examples: FRGN208A.20o, FRGN208A.20n, FRGN208A.20g

# Prerequisites
Debian 9.12

Python 2.7.13

RNX2CRX from RNXCMP Hatanaka software

Rinex files (.o, .n, .g)

# Usage

Copy the python program in a desired folder on your server 

Download on https://terras.gsi.go.jp/ja/crx2rnx.html exectuable file "RNXCMP_4.0.8_Linux_x86_64bit.tar.gz" (choose the version according to your processor)

Decompress the programm and copy only RNX2CRX in the same folder than the code 

Prepare folders:
- For source Rinex files
- For backup Rinex observations files
- For Transfert files on FTP deposit
Replace paths on declaration part of python programm (Source, Dest, TRansfertRGP)

A gmail account is required

A file for gmail password is required

# Version
Laste stable version: rinex5.py

# Author
Sandrine Morey alias 310703

# Licence
Free licence



