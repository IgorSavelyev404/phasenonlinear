import matplotlib.pyplot as plt
import numpy as np
import copy
from mpl_toolkits import mplot3d

def draw_plots2(x,y,x1,y1):
    '''Draw 2 graph on one plot with x and y'''
    plt.rcParams.update({'font.size': 14})  # increase the font size
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(x, y,x1,y1)
    plt.grid()
    plt.show()   

def draw_plot(x,y, abcyss, ordinat, title):
    '''Draw plot with x and y'''
    plt.rcParams.update({'font.size': 14})  # increase the font size
    plt.xlabel(abcyss)
    plt.ylabel(ordinat)
    plt.title(title)
    plt.plot(x, y)
    plt.grid()
    plt.show()   

def f(x,y,g):
    g11=[[g]*len(x[0])]*len(x)
    
    return np.array(g11)

def draw_3d_plot(x, y, z, x_label, y_label, z_label, title,g,l1,l2,dots):
    fig = plt.figure()
    plt.title(title)
    ax = plt.axes(projection='3d')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.plot3D(x, y, z,)
    max_x1=max(x)
    min_x1=min(x)
    max_x2=max(y)
    min_x2=min(y)
    max_x3=max(z)
    min_x3=min(z)
    if g[2]!=0:
        X = np.arange(min_x1-0.25, max_x1+0.25, 0.25)
        Y = np.arange(min_x2-0.25, max_x2+0.25, 0.25)
        X, Y, = np.meshgrid(X,Y,)
        Z = (l1-X*g[0]-Y*g[1])/g[2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    alpha =0.3)
        Z = (l2-X*g[0]-Y*g[1])/g[2]    
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    alpha =0.3)   
    elif g[0] !=0:
        Z = np.arange(min_x3-0.25, max_x3+0.25, 0.25)
        Y = np.arange(min_x2-0.25, max_x2+0.25, 0.25)
        Y, Z = np.meshgrid(Y,Z)
        X= (l1-Y*g[1]-Z*g[2])/g[0]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    alpha =0.3)
        X= (l2-Y*g[1]-Z*g[2])/g[0]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    alpha =0.3)
    else:
        X = np.arange(min_x1-0.25, max_x1+0.25, 0.25)
        Z = np.arange(min_x3-0.25, max_x3+0.25, 0.25)
        X, Z = np.meshgrid(X,Z)
        Y= (l1-X*g[0]-Z*g[2])/g[1]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    alpha =0.3)
        Y= (l2-Y*g[0]-Z*g[2])/g[1]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    alpha =0.3)
    # Рисуем две последние точки
    if len(dots)>1:
        last_dot=dots[-1]
        x=last_dot[1]
        y=last_dot[2]
        z=last_dot[3]
        ax.scatter(x,y,zs = z, s=50, color='red')
        text = str(round(x,4)) + ', ' + str(round(y,4)) + ', ' + str(round(z,4))
        ax.text(x, y, z, text, zdir='x',)    
        if len(dots)>2:
            last_dot=dots[-2]
            x=last_dot[1]
            y=last_dot[2]
            z=last_dot[3]
            ax.scatter(x,y,zs = z, s=50, label='True Position',color='red')
            text = str(round(x,4)) + ', ' + str(round(y,4)) + ', ' + str(round(z,4))
            ax.text(x, y, z, text, zdir='x') 
    #X, Y = np.meshgrid([x[0],x[-1]], [z[0],z[-1]])
    #Z = f(X,Y,l1/g[1])
    #ax.plot_surface(X, Z, Y, rstride=1, cstride=1,
    #            alpha =0.3)
    #X, Y = np.meshgrid([y[0],y[-1]], [z[0],z[-1]])
    #Z = f(X,Y,l1/g[0])
    #ax.plot_surface(Z, X, Y, rstride=1, cstride=1,
    #            alpha =0.3)
    #X = np.arange(-5, 5, 0.25)
    #Y = np.arange(-5, 5, 0.25)
    #Z = f(X/g[0],Y/g[1],l2/g[2])
    #print(Y)
    #ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
    #            alpha =0.3)
    #X, Y = np.meshgrid([x[0],x[-1]], [z[0],z[-1]])
    #Z = f(X,Y,l2/g[1])
    #ax.plot_surface(X, Z, Y, rstride=1, cstride=1,
    #            alpha =0.3)
    #X, Y = np.meshgrid([y[0],y[-1]], [z[0],z[-1]])
    #Z = f(X,Y,l2/g[0])
    #ax.plot_surface(Z, X, Y, rstride=1, cstride=1,
    #            alpha =0.3)
    plt.grid()
    plt.show() 

def main():
    '''for test'''
    x=[0,1,2,3,4]
    y=[0,2,4,6,12]
    z=[0,4,8,12,16]
    draw_3d_plot(x,y,z,'1','2','3','test',[1,2,3],1,-1,[[1.3,2,3],[4,5,6]])
    plt.show()

if __name__ == '__main__':
    main()
