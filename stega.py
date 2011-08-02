#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, png
from os import urandom
from crypto import aes
from getpwd import getpwd
from getpass import getpass
from hashlib import sha256
from struct import pack, unpack

class stega:
    def bytestobits(self, bytes):
        res = []
        for i in bytes:
            for j in range(8):
                res.append(ord(i)>>j&1)
        return res

    def bitstobytes(self, bits):
        res = ""
        for i in range(0,len(bits),8):
            c = 0
            for j in range(8):
                c += bits[i+j] << j
            res += chr(c)
        return res

    def encode(self, pixel, bytes):
        if len(pixel) < (len(bytes)+2)*8: raise Exception, "Image too short"
        bits = self.bytestobits(bytes)
        bits = self.bytestobits(pack('!H', len(bits))) + bits
        output = []
        for i in range(len(bits)):
            output.append((pixel[i] & 0xFE) | bits[i])
        while len(output) < len(pixel):
            output.append(pixel[len(output)])
        return output

    def decode(self, pixel):
        raw = []
        for i in range(16):
            raw.append(pixel[i] & 1)
        size = unpack('!H', self.bitstobytes(raw))[0]
        raw = []
        for i in range(16, size+16):
            raw.append(pixel[i] & 1)
        return self.bitstobytes(raw)

    def put(self, imgin, imgout, bytes):
        with open(imgin,'rb') as f:
            buff = f.read()
        a = png.Reader(bytes=buff).read_flat()
        x = self.encode(a[2], bytes)
        with open(imgout,'wb') as f:
            b = png.Writer(width=a[0], height=a[1],alpha=a[3]['alpha'], bitdepth=a[3]['bitdepth'], greyscale=a[3]['greyscale'], planes=a[3]['planes'], compression=9)
            b.write_array(f, x)

    def get(self, imgin):
        with open(imgin,'rb') as f:
            buff = f.read()
        a = png.Reader(bytes=buff).read_flat()
        f = self.decode(a[2])
        return f

def usage():
    print ""
    
if __name__ == '__main__':
    if sys.argv[1] == "-h":
        if len(sys.argv) < 4:
            usage()
        else:
            iv = urandom(16)
            #key = getpwd('key : ')
            ctx = aes(getpass('key : '), iv, 1, mode='cfb')
            sys.stdout.write('> ')
            sys.stdout.flush()
            plain = sys.stdin.read()
            print "[+] Encrypt and Encode ..."
            ciphertext = ctx.ciphering(plain)
            stega().put(sys.argv[2], sys.argv[3], iv+ciphertext+sha256(plain).digest())
            print "[+] Done."
    elif sys.argv[1] == "-u":
        if len(sys.argv) < 3:
            usage()
        else:
            ciphertext = stega().get(sys.argv[2])
            iv = ciphertext[:16]
            ciphertext = ciphertext[16:]
            #key = getpwd('key : ')
            ctx = aes(getpass('key : '), iv, 0, mode='cfb')
            plain = ctx.ciphering(ciphertext[:len(ciphertext)-32])
            if sha256(plain).digest() != ciphertext[len(ciphertext)-32:]:
                raise Exception, "[!] Fail to decode/decrypt ..."
            print plain
    else: usage()
