#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:00:50 2018

@author: yanyanjiang
"""



filename = "movies_link.txt"  
myfile = open(filename)  
lines = len(myfile.readlines())  
print ("There are %d lines in %s"%(lines, filename))