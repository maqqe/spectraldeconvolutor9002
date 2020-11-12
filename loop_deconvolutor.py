import csv
import sys


file_path = 'testdata/complex.csv'


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
    def __init__(self):
        
        self.mix = data_loader(get_file_names(sys.argv)[0])
        self.pure1 = data_loader(get_file_names(sys.argv)[1])
        self.pure2 = data_loader(get_file_names(sys.argv)[2])



if __name__ == '__main__':
    pass

