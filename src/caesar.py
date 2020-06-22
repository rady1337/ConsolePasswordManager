# -*- coding: utf-8 -*-


def crypt(text, num):
    caesar = [chr(ord(i) + num) for i in text]
    return ''.join(caesar)


def decrypt(text, num):
    caesar = [chr(ord(i) - num) for i in text]
    return ''.join(caesar)
