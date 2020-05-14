import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

def draw_plot(x,y, abcyss, ordinat, title):
    '''Отрисовка двухмерного графика'''
    plt.rcParams.update({'font.size': 14})  
    plt.xlabel(abcyss)
    plt.ylabel(ordinat)
    plt.title(title)
    plt.plot(x, y)
    plt.grid()
    plt.show()   

def draw_3d_plot(x, y, z, x_label, y_label, z_label, title,g,l1,l2,dots):
    '''Отрисовка трехмерного графика с поверхностью и точками переключения'''
    # Настраиваем полотно
    fig = plt.figure()
    plt.title(title)
    ax = plt.axes(projection='3d')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.plot3D(x, y, z,)
    # Определяем максимальные значения для автомасштабирования
    max_x1=max(x)
    min_x1=min(x)
    max_x2=max(y)
    min_x2=min(y)
    max_x3=max(z)
    min_x3=min(z)
    # Находим плоскость поверхности переключения и отрисовываем графики
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
    if len(dots)>0:
        last_dot=dots[-1]
        x=last_dot[1]
        y=last_dot[2]
        z=last_dot[3]
        ax.scatter(x,y,zs = z, s=50, color='red')
        text = str(round(x,4)) + ', ' + str(round(y,4)) + ', ' + str(round(z,4))
        ax.text(x, y, z, text, zdir='x',)    
        if len(dots)>1:
            last_dot=dots[-2]
            x=last_dot[1]
            y=last_dot[2]
            z=last_dot[3]
            ax.scatter(x,y,zs = z, s=50, label='True Position',color='red')
            text = str(round(x,4)) + ', ' + str(round(y,4)) + ', ' + str(round(z,4))
            ax.text(x, y, z, text, zdir='x') 
    plt.grid()
    plt.show() 