# spectraldeconvolutor9002

A small python script that deconvolutes up complex spectrum of up to 3 component spectra. Requires Numpy, pandas, and matplotlib.

The script takes .csv files as input as in

> $ python pandas_deconvolutor.py complex.csv component1.csv component2.csv component3.csv

The complex spectrum has to be the first .csv file in the list, followed by two or three component spectrum files


The .csv file architecture has to be as follows

> x-axis data,y-axis data, . . .  

All the files need to be of the same length, as in contain an equal amount of data points.

Upon finishing, the script will print the fractions of the component species in the complex spectra and create a graph that shows the complex spectrun, fraction scaled component spectra and any possible left over residues from the fitting. The graph is saved as 'fit.png' in the folder the script was run in.


A deconvolutor based on basic python functionalities is also included as loop_deconvolutor.py. This script takes only a maximum of 2 component spectra and does not graph the results. It is not, however, reliant on having numpy, pandas, and matplotlib installed.
