import random
import math
import tio as t
import matplotlib.pyplot as plt     # Import the plot package as plt
import numpy as np
from scipy.optimize import curve_fit


class Dice(object):
    """
    Dice object for simulations
    """
    def __init__(self,sides = 6):
        """
        Constructor for Dice with specified number of sides
        """
        self.sides = sides

    def roll(self):
        """
        One roll of fair dice.
        """
        return random.randint(1,self.sides)
        #return int(round(self.sides*random.random() + 1.0))

    def throw(self,number = 1000):
        """
        Throw a number of dice, it will return list,
        but also hold the list internally.
        """
        self.sample = []
        while number >= 0:
            self.sample.append(self.roll())
            number -= 1

        return self.sample

    def count(self,value = 1):
        """
        Count the number of dice with a specific value, 
        Defaults to 1
        """
        n = 0
        for s in self.sample:
            if s == value:
                n += 1
        return n

def line(x, a, b, c):
    return a*np.exp(-b*x) + c
    


def main():
    sides = t.getInt("Number of sides on each dice",6)
    startsample = t.getInt("Starting Sample",1000)

    dice = Dice(sides)


    xData = []
    yData = []
    run = 0
    sample = startsample
    while sample > 10:
        #      Store generation and sample size in lists.
        xData.append(run)
        yData.append(sample)
        dice.throw(sample)

        #       Get number of dice with value 1
        n = dice.count()
        sample -= n   # Reduce sample size by that number
        run += 1

    #            Do data fitting
    x = np.array(xData)     # convert x/y data to np arrays.
    y = np.array(yData)
    sig = np.sqrt(y)/y
    #                Define a 3 parameter line
    #line = lambda x,a,b,c : a*np.exp(-b*x) + c
    #                Do a fit
    popt,pcov = curve_fit(line,x,y,p0=[startsample,1.0/sides,0.0],sigma=sig)
    t.tprint(popt)


    #                Plot data
    plt.plot(x,y,"x")
    plt.title("Decay plot for {0:d} dice with {1:d} sides".format(startsample,sides))
    #                Plot the fitted line with 200 points
    xfine = np.linspace(0.0,float(run),200)
    plt.plot(xfine,line(xfine,popt[0],popt[1],popt[2]),"r",label="Decay parameter {0:8.4f}".format(popt[1]))
    plt.xlabel("Generation")
    plt.ylabel("Dice Number")
    plt.legend(loc="upper right",fontsize="small")
    plt.show()
    

main()    
