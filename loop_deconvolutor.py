import csv
import sys


# method to convert a string into float, if possible.
# if unable, returns 'a'.

def float_converter(input):
    try:
        return float(input)
    except:
        return 'a'


# opens a .csv file and returns two lists that contain the first to columns of numbers from file.
# if a provided file name is incorrect, exits interpreter and informs user.

def data_loader(file_path):
    try:
        f = open(file_path)
        r = csv.reader(f)
        col1 = list()
        col2 = list()

        for row in r:
            
            if float_converter(row[0]) != 'a':
                col1.append(float_converter(row[0]))
            if float_converter(row[1]) != 'a':
                col2.append(float_converter(row[1]))
        
        f.close()
        return (col1, col2)
        
    except:
        print('One or more file names provided could not be found, please check input')
        sys.exit()


# takes command line arguments and puts them into a list.
# checks that a correct number of arguments present.
# if incorrect number of arguments, exits and informs user.

def get_file_names(arguments):
    if (len(arguments) == 4):
        i = 1
        file_names = list()
        while i < 4:
            file_names.append(arguments[i])
            i += 1
        return file_names
    else:
        print('Too many or too few command line arguments, please make sure 3 file names are provided')
        sys.exit()


# a class that takes care of the actual deconvolution.

class Deconvolutor():
    def __init__(self, mix, pure1, pure2):
        
        self.mix = mix
        self.pure1 = pure1
        self.pure2 = pure2
        self.residues = sum(mix[1])
        self.frac1 = 0
        self.frac2 = 0

        if len(self.mix[1]) == len(self.pure1[1]) & len(self.pure1[1]) == len(self.pure2[1]):
            pass
        else:    
            print('The files provided contain differing amounts of data, please check that the data sets are of equal lengths')
            sys.exit()
        
    
    # returns the fractions of the pure species

    def deconvolute(self):
        
        i = 0

        mix_spectrum = self.mix[1]
        pure1_spectrum = self.pure1[1]
        pure2_spectrum = self.pure2[1]
        

        while i <= 100:
            
            j = 0
            calculated_spectrum = list()

            while j < len(mix_spectrum):
                calculated_spectrum.append(pure1_spectrum[j]*i*0.01 + pure2_spectrum[j]*(1 - i*0.01))
                j += 1
            
            k = 0
            fit_residues = 0

            while k < len(mix_spectrum):
                difference = abs(mix_spectrum[k] - calculated_spectrum[k])
                
                fit_residues += difference
                k += 1

            if (fit_residues < self.residues):
                self.frac1 = i*0.01
                self.frac2 = 1 - i*0.01
                self.residues = fit_residues

            

            i += 1
        
        return [self.frac1, self.frac2]





if __name__ == '__main__':
    mix = data_loader(get_file_names(sys.argv)[0])
    pure1 = data_loader(get_file_names(sys.argv)[1])
    pure2 = data_loader(get_file_names(sys.argv)[2])
        
    d = Deconvolutor(mix, pure1, pure2)
    print('')
    print('Fraction of pure species 1:', d.deconvolute()[0])
    print('Fraction of pure species 2:', d.deconvolute()[1]) 

