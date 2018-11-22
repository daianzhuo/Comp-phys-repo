#Computational Physics assignment source code#
Author: Anzhuo Dai

The code is split into 5 different .py files for the 5 different questions. 
By running each script, the results described in the assignment should show up with no further operations needed.

Notes based on script number:

1) Very straightforward, only 2 print statements at the end for 5 outputs

2) Print statements set up in a way that they print out the answers and verifications in the same order as asked in the question
    Verifications are lebelled so that if unwanted, can be easily identified and commented out

3) Produces all the relevant plots directly
    Will print out all everything in Script 2 again since the whole Script 2 is imported for convenience's sake rather than the individual functions

4) Plots the Fourier transforms of the two given functions, as well as the original functions themselves and the product of their convolution
    Also prints the area of under the convolution curve

5) Again, running this should produce all the relevant plots
    The time_test() function takes a long time to run, if just want the plots, it has been labelled amd is recommended to comment it out
    Bit of a mess at the end, kept the rejection_edited() function because it can plot the generated points which makes it run slower than the rejection() function
    