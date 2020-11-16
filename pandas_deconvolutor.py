import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time




script_dir = os.getcwd()
datafile = 'testdata/complex.csv'

mix = pd.read_csv(os.path.normcase(os.path.join(script_dir, datafile)))
mix = mix.set_index('wavelength')


pure1 = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'testdata/pure1.csv')))
pure2 = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'testdata/pure2.csv')))



f1 = 0
f2 = 0

residues = mix.sum()
i = 0

t1 = time.time()

while i <= 100:

    calc = pure1*i*0.01 + pure2*(1-i*0.01)
    calc = calc.set_index('wavelength')

    j = 0
    while j <= len(calc):
        
        calc_res = abs(mix - calc).sum()
        
        
        if calc_res.values[0] < residues.values[0]:
            residues = calc_res
            f1 = i*0.01
            f2 = 1-i*0.01 
        
        
        j += 1


    i += 1

t2 = time.time()

print(f1)
print(f2)
print('Took', t2 - t1, 'seconds to deconvolute')

