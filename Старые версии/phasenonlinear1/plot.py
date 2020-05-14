import matplotlib.pyplot as plt
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

def draw_3d_plot(x, y, z, x_label, y_label, z_label, title):
    fig = plt.figure()
    plt.title(title)
    ax = plt.axes(projection='3d')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.plot3D(x, y, z,)
    plt.grid()
    plt.show() 

def main():
    '''for test'''
    x=[0,1,2,3,4]
    y=[0,2,4,6,12]
    z=[0,4,8,12,16]
    draw_3d_plot(x,y,z)
    plt.show()

if __name__ == '__main__':
    main()
