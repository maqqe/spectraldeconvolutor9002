import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

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


    # Deconvolutes the provided complex spectrum using the provided spectra of pure species.

    def deconvolute(self):

        self.load_data()
        fractions = [0., 0.]
        if len(self.dsets) == 4:
            fractions.append(0.)
        residues = self.dsets[0].sum()[1]
        residue_spectrum = self.dsets[0]

        i = 0

        while i <= 100:

            if len(self.dsets) == 3:

                calc_spectrum = pd.Series(self.dsets[1].iloc[:, 1]*i*0.01 
                                + self.dsets[2].iloc[:, 1]*(1-i*0.01))
                calc_residues = abs(self.dsets[0].iloc[:, 1] - calc_spectrum).sum()

                if calc_residues < residues:
                    
                    residue_spectrum['Residues'] = self.dsets[0].iloc[:, 1] - calc_spectrum
                    residues = calc_residues
                    fractions[0] = i*0.01
                    fractions[1] = 1-i*0.01
                
            if len(self.dsets) == 4:

                j = 0

                while j <= 100 - i:

                    calc_spectrum = pd.Series(self.dsets[1].iloc[:, 1]*i*0.01 
                                    + self.dsets[2].iloc[:, 1]*j*0.01 
                                    + self.dsets[3].iloc[:, 1]*(1-j*0.01-i*0.01))                  
                    calc_residues = abs(self.dsets[0].iloc[:, 1] - calc_spectrum).sum()

                    if calc_residues < residues:
                        
                        residue_spectrum['Residues'] = self.dsets[0].iloc[:, 1] - calc_spectrum
                        residues = calc_residues
                        fractions[0] = i*0.01
                        fractions[1] = j*0.01
                        fractions[2] = 1-j*0.01-i*0.01

                    j += 1

            i += 1

        return [fractions, residue_spectrum]


    # Plots the deconvoluted data into a line graph. 
    # Shown in the graph are the original mix spectrum and the spectra of the pure species multiplied by their respective fraction.

    def plot_data(self, fractions, residues):

        frax = fractions        

        for d in self.dsets:
            d = d.set_index(d.columns[0])

        df = pd.DataFrame(self.dsets[0])

        df['Residues'] = residues.iloc[:, 2]
        df['Species 1'] = self.dsets[1].iloc[:, 1] * frax[0]
        df['Species 2'] = self.dsets[2].iloc[:, 1] * frax[1]
        if len(frax) == 3:
            df['Species 3'] = self.dsets[3].iloc[:, 1] * frax[2]

        plot = df.plot(x = df.columns[0])

        plot.figure.savefig('fit.png')

    
 # Runs the script. Reports the fractions from deconvolute() and saves figures from plot_data().

    def run(self):

        print('\nProcessing input...\n')
        i = 0

        t1 = time.time()

        frax = self.deconvolute()[0]
        
          

        while i < len(frax):
            print('Fraction of Species', i + 1, ': ', frax[i])
            i += 1
        
        t2 = time.time()

        print('\nTook', round(t2 - t1, ndigits = 1), 'seconds to deconvolute')
        print('\nCreating fit.png in current working directory')

        self.plot_data(frax, self.deconvolute()[1])
        


# d = Deconvolutor(['aa', 'testdata/3m.csv', 'testdata/3p1.csv', 'testdata/3p2.csv', 'testdata/3p3.csv'])
# d = Deconvolutor(['aa', 'testdata/complex.csv', 'testdata/pure1.csv', 'testdata/pure2.csv'])
# d.run()


if __name__ == '__main__':
    d = Deconvolutor(sys.argv)
    d.run()
