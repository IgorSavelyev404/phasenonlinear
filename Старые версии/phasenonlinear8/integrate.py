from scipy.integrate import solve_ivp
import plot
import numpy as np
import functions
import EquationClass
import math
import tkinter as tk

def second_ode_solver(eqution,initial_values,range_sol, step):
    ''' Решает систему диф. уравнений 
    eqution - правая часть уравнения
    range - интервал интегрирования (t0, tf)
    initial_values - вектор начальных значений
    step - шаг интегрирования'''
    solution = solve_ivp(eqution,range_sol, initial_values, min_step=step, max_step = step,atol=1,rtol=1, first_step=step)
    return solution

def set_function_system(t,y):
    '''Задание функции для решателя'''
    equa = EquationClass.Equation.get_instance()
    a=equa.A  
    b=equa.B
    g=equa.G
    # считаем х и сохраняем запрашиваемые значения
    #source = equa.t_func(t)
    #source = source - os* y[i] 
    #x = source
    x = y[:]
    u=0
    dy=[0] * equa.size
    #print(f't is {t} y is {y}')
    for i in range(equa.size): #считаем скалярное произведение
        u=u+x[i]*g[i]
    u=equa.sign_hyst[0](t,u) # выход с реле
    if not hasattr(equa, 'last_u'):
        equa.last_u = u
    if u != equa.last_u: # переключение, записываем координаты
        equa.dots.append([t,x[0], x[1], x[2],])
    equa.last_u=u
    for i in range(equa.size):
        #print(f't is {t} i is {i} u is {u} x*g is {x[i]*g[i]} y is {y}')
        dy[i]=0
        for j in range(equa.size):
            
            dy[i] = dy[i]+a[i*equa.size+j]*y[j] #итоговый выход
            #print(f'dy[i] is {dy[i]} a is {a[i*equa.size+j]} i is {i} j is {j} y(j) is {y[j]}')
            #print(f'y is {y}')
        dy[i]=dy[i]+b[i]*u - equa.disturb(t)
    #print(dy)
    return dy

def set_function_2rank(t,y):
    '''Задание функции для решателя'''
    equa = EquationClass.Equation.get_instance()
    a2, a1, a0, b0, b1, os = equa.a2, equa.a1, equa.a0, equa.b0, equa.b1, equa.os
    equa.y, equa.dy, = y[0], y[1]
    # считаем х и сохраняем запрашиваемые значения
    source = equa.t_func(t)
    source = source - os*y[0] 
    dx=0
    x = source
    
    # Проверка, на вход поступает линейная функция или нелинейная для вычисления производной
    if equa.x_func != [functions.ramp, functions.ramp, functions.ramp]:
        for non_linear in equa.x_func:
            x, dx = non_linear(t, x, dx)
    else:    
        # запоминаем время и значения перед звеном для производной
        if equa.array.size < 4 or t > equa.array[-1,0]:
            if equa.array.size == 0:
                equa.array = np.array([t,x])
                dx = 0
            else:
                equa.array = np.vstack((equa.array, [t,x]))
                dx = equa.dx(t,x)
        else:
            dx = equa.dx_prec(t, x)
    # система для dx d2y и dy
    dy = y[1]
    d2y = -y[0] * a2/a0 - y[1] * a1/a0  + b0*dx/a0 +b1*x/a0
    y = [dy, d2y]
    return y

def new_winF(dots): # new window definition
    root=tk.Toplevel()
    root.title("Точки переключения")
    height = len(dots)
    width = 4
    t = tk.Label(root,width=15, text="t")
    x1 = tk.Label(root,width=15, text="x1")
    x2 = tk.Label(root,width=15, text="x2")
    x3 = tk.Label(root,width=15, text="x3")
    dt = tk.Label(root,width=15, text="dt")
    t.grid(row=0, column=0)    
    x1.grid(row=0, column=1)
    x2.grid(row=0, column=2)
    x3.grid(row=0, column=3)
    dt.grid(row=0, column=4)
    for i in range(height): #Rows
        for j in range(width): #Columns
            b = tk.Label(root,width=15, text=str(round(dots[i][j],8)))
            b.grid(row=i+1, column=j)
    for i in range(1,height):
        b = tk.Label(root,width=15, text=str(round(dots[i][0]-dots[i-1][0],8)))
        b.grid(row=i+1, column=width)
    if height >0:
        b = tk.Label(root,width=15, text=str(round(dots[0][0],8)))
        b.grid(row=1, column=width)
    root.grid()
    return root
    

def main1(phase_trace=False, transition=False, phase_plane = False):
    '''Решение уравнения и построения графика'''
    if phase_plane == True:
        equa = EquationClass.Equation.get_instance()
        solve = second_ode_solver(set_function_system,equa.ic,[equa.time_start, equa.time_end],  equa.step)
        t, y = solve.t, solve.y
        
        
        if equa.size ==1:
            del equa
            plot.draw_plot(t,y[0], 't, с', 'x1, значение', 'Решение уравнения')
            
        elif equa.size == 2:
            del equa
            plot.draw_plot(y[0],y[1],'x1, значение', 'x2, значение', 'Фазовая траектория')
            
        else:
            g = equa.G
            l1=equa.l1
            l2=equa.l2
            dots=equa.dots
            equa.dot_window=new_winF(dots)
            plot.draw_3d_plot(y[0], y[1], y[2],'x1, значение', 'x2, значение','x3, значение', 'Фазовое пространство',g,l1,l2,dots)
           
        return 
    else:
        equa = EquationClass.Equation.get_instance()
        equa.array=np.array([])
        equa.ardx= []
        solve = second_ode_solver(set_function_2rank,(equa.y0, equa.dy0),[equa.time_start, equa.time_end],  equa.step)
        t, y = solve.t, solve.y
        EquationClass.Equation.created = False
        del equa
    
    if transition:
        plot.draw_plot(t,y[0], 't, с', 'y, значение', 'Решение уравнения')
    if phase_plane:
        plot.draw_3d_plot(y[0], y[1], y[2],'y, значение', 'dy, значение','d2y, значение', 'Фазовая плоскость')
    if phase_trace:
        plot.draw_plot(y[0],y[1],'y, значение', 'dy, значение', 'Фазовая траектория')
