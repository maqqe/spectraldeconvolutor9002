import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

"""
df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(3)), dtype='float32'),
                    'D': np.array([3] * 3, dtype='int32'),
                    'E': pd.Categorical(["test", "train", "test"]),
                    'F': 'foo'})

print(df2.iloc[0:2])



df3 = pd.DataFrame({'wl': [1,2,3,4,5,'shimadzu 5000'], 'counts': [5,6,7,8,9,'shima 5000']})

df4 = pd.DataFrame({'wl': [1,2,3,4,5], 'counts': [5,6,7,8,9]})

print(df3.iloc[:, 1])

df3 = df3.set_index('wl')
df4 = df4.set_index('wl')


df5 = df3 + df4
print(df5.dropna(how='any'))


print(df3.describe())
print(pd.isna(df4))

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD')) """



class Deconvolutor():


    # Class constructor, appends the given command line arguments to a list and checks that there are enough arguments. If not, exits script.

    def __init__(self, list_of_arguments):

        self.files = list()
        self.dsets = list()

        if len(list_of_arguments) < 4:
            print('Not enough command line arguments, please provide at least 3 file names')
            sys.exit()
        else:
            i = 1
            while i < len(list_of_arguments):
                self.files.append(list_of_arguments[i])
                i += 1
    

    # Reads the data from the files given as command line arguments using pd.read_csv().
    # Prints a warning if the files are not .csv files or if they are of different lengths. If so, exits script.

    def load_data(self):
        
        for f in self.files:
            try:
                self.dsets.append(pd.read_csv(f))
            except:
                print('A file could not be opened, please make sure all arguments given are .csv files')
                sys.exit()
        if all(len(dset) == len(self.dsets[0]) for dset in self.dsets):
            pass
        else:
            print('Not all datasets were the same length, please see that the .csv files have the same number of rows')
            sys.exit()


    # Deconvolutes the provided spectra

    def deconvolute(self):

        f1 = 0
        f2 = 0
        f3 = 0
        self.load_data()
        residues = self.dsets[0].sum()[1]
        i = 0

        t1 = time.time()

        while i <= 100:

            if len(self.dsets) == 3:
                calc_spectrum = pd.Series(self.dsets[1].iloc[:, 1]*i*0.01 + self.dsets[2].iloc[:, 1]*(1-i*0.01))
                calc_residues = abs(self.dsets[0].iloc[:, 1] - calc_spectrum).sum()

                if calc_residues < residues:
                    residues = calc_residues
                    f1 = i*0.01
                    f2 = 1-i*0.01
            
            if len(self.dsets) == 4:

                j = 0

                while j <= 100:
                    calc_spectrum = pd.Series(self.dsets[1].iloc[:, 1]*i*0.01 + self.dsets[2].iloc[:, 1]*j*0.01 + self.dsets[3].iloc[:, 1]*(1-j*0.01))
                    calc_residues = abs(self.dsets[0].iloc[:, 1] -  calc_spectrum).sum()

                    if calc_residues < residues:
                        residues = calc_residues
                        f1 = i*0.01
                        f2 = j*0.01
                        f3 = 1-j*0.01
                    
                    j += 1


            i += 1
        
        t2 = time.time()

        print(f1, f2)

        print(t2 - t1)


d = Deconvolutor(['aa', 'testdata/complex.csv', 'testdata/pure1.csv', 'testdata/pure2.csv'])
d.deconvolute()


""" script_dir = os.getcwd()
datafile = 'testdata/complex.csv'

mix = pd.read_csv(os.path.normcase(os.path.join(script_dir, datafile)))

pure1 = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'testdata/pure1.csv')))
pure2 = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'testdata/pure2.csv')))

f1 = 0
f2 = 0

residues = mix.sum()[1]

i = 0

t1 = time.time()

while i <= 100:

    #TRY AND PLAY WITH APPEND HERE
    # Adding a column to a DataFrame is relatively fast. However, adding a row requires a copy, and may be expensive. 
    # We recommend passing a pre-built list of records to the DataFrame constructor instead of building a DataFrame by iteratively appending records to it. 
    # See Appending to dataframe for more.

    calc = pd.Series(pure1['counts']*i*0.01 + pure2['counts']*(1-i*0.01))

    calc_res = abs(mix['counts'] - calc).sum()
        
    if calc_res < residues:
        residues = calc_res
        f1 = i*0.01
        f2 = 1-i*0.01 
        
    i += 1

t2 = time.time()

print(f1)
print(f2)
print('Took', t2 - t1, 'seconds to deconvolute') """

