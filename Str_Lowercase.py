# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
sentence = "I would love to join your company." 
print("The original string is: " + str(sentence))
result = lambda string: sentence[:len(sentence)].lower() if str else ''
print("The string after lowercasing: " +str(result(sentence)))
