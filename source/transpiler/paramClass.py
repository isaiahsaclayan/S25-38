'''
Author: Theo Barrett-Johnson
Created: 02/03/25
File: paramClass.py
Description: The file for the design and implementation of the class that holds the data structures for parameter inputs
'''
import numpy as np
class Parameters:
    def __init__(self):
        #params will be a 2 by n array, The first row will be for nScrypt params,
        #second row will be for Optomec params, any param that is not set by user
        #to any specific value will be -1 by default
        #currently making n=16 as a base estimate for the number of relevant parameters for a given printer
        self.params = np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], dtype=float)


#TESTING
#below is example of calling on Parameters to initialize a Parameter array. This will need to be done upon toolpath import
#tmp = Parameters()