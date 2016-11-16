import numpy as np
import random
import os, subprocess
import matplotlib.pyplot as plt
import matplotlib.cm as cm
 
class PLA:
    def __init__(self, N):
        # Initializing function f. WeightVectorith generating random points
        xA,yA,xB,yB = [random.uniform(-3, 3) for i in range(4)]

        # Hardocded value for points
        # xA = 0.17576052898751415
        # xB = 2.382994632563072
        # yA = -0.7249833011786064
        # yB = -1.0421187912441592
        # print("xA", xA, "xB", xB, "yA", yA, "yB", yB,)

        self.WeightVector = np.array([xB*yA-xA*yB, yB-yA, xA-xB])
        # print("WeightVector", self.WeightVector)
        # N = Number of random points needed
        self.X = self.random_points(N)
 
    def random_points(self, N):
        X = [] # array for random points
        for i in range(N):
            x1,x2 = [random.uniform(-5, 5) for i in range(2)]
            x = np.array([1,x1,x2])
            # s is the sign of the point based on the dot product with Transpose WeightVector of the point
            s = int(np.sign(self.WeightVector.T.dot(x)))
            # Appneding the points in to points Array
            X.append((x, s))
        return X
 
    def plot(self, mispts=None, vec=None, save=False):
    	#using mathplotlib library to plot line and points on the graph
        fig = plt.figure(figsize=(5,5))
        plt.xlim(-5,5)
        plt.ylim(-5,5)
        plt.xlabel("x1")
        plt.ylabel("x2")
        WeightVector = self.WeightVector
        a, b = -WeightVector[1]/WeightVector[2], -WeightVector[0]/WeightVector[2]
        l = np.linspace(-5,5)
        plt.plot(l, a*l+b, 'k')
        cols = {1: 'r', -1: 'b'}
        for x,s in self.X:
            plt.plot(x[1], x[2], cols[s]+'o')
        if mispts:
            for x,s in mispts:
                plt.plot(x[1], x[2], cols[s]+'.')
        if vec != None:
            aa, bb = -vec[1]/vec[2], -vec[0]/vec[2]
            plt.plot(l, aa*l+bb, 'g-', lw=2)
        if save:
            if not mispts:
                plt.title('N = %s' % (str(len(self.X))))
                plt.text(-4,-7,'Red point = +1, Blue points = -1',rotation=0)
                plt.text(-4,-8,'Black Line = Target Function',rotation=0)
            else:
                plt.title('N = %s with %s test points' \
                          % (str(len(self.X)),str(len(mispts))))
            plt.savefig('p_N%s' % (str(len(self.X))), \
                        dpi=200, bbox_inches='tight')
        # plt.text(-6.5,3,'Sign of h = -1',rotation=90)
        plt.text(-4,-7,'Red point = +1, Blue points = -1',rotation=0)
        plt.text(-4,-8,'Black Line = Target Function f',rotation=0)
        plt.text(-4,-9,'Green Line = Hypothesis Function g',rotation=0)
        # plt.text(0,-9,'Green Line = Line after new weights',rotation=0)
        # plt.show()

    def classification_error(self, vec, pts=None):
        # Error defined as fraction of misclassified points
        if not pts:
            pts = self.X
        M = len(pts)
        n_mispts = 0
        for x,s in pts:
            if int(np.sign(vec.T.dot(x))) != s:
                n_mispts += 1
        error = n_mispts / float(M)
        return error
 
    def choose_miscl_point(self, vec):
        # Choose a random point among the misclassified
        pts = self.X
        mispts = []
        for x,s in pts:
            if int(np.sign(vec.T.dot(x))) != s:
                mispts.append((x, s))
        return mispts[random.randrange(0,len(mispts))]
 
    def pla1(self, save=False):
        # Initialize the weigths to zeros
        w = np.zeros(3)
        X, N = self.X, len(self.X)
        it = 0
        # Iterate until all points are correctly classified
        while self.classification_error(w) != 0:
            # print(self.classification_error(w))
            it += 1
            # Pick random misclassified point
            x, s = self.choose_miscl_point(w)
            # Update weights
            w += s*x
            # print(w)
            if save:
                self.plot(vec=w)
                plt.title('N = %s, Iteration %s\n' \
                          % (str(N),str(it)))
                plt.savefig('p_N%s_iteration%s' % (str(N),str(it)), \
                            dpi=200, bbox_inches='tight')
            # print w
        self.w = w
        print self.w
 
    def check_error(self, M, vec):
        check_pts = self.random_points(M)
        return self.classification_error(vec, pts=check_pts)

p = PLA(100)
p.plot(save=True)
p.pla1(save=True)
print(p.check_error(100, p.w))

#define base directory to store images
basedir = 'D:\SJSU\subjects\sem3\ML'
os.chdir(basedir)
pngs = [pl for pl in os.listdir(basedir) if pl.endswith('png')]
basepng = pngs[0][:-8]

