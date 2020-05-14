from scipy.integrate import solve_ivp
import plot
import numpy as np
import functions
import EquationClass
import math

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
    x = y
    u=x
    dy=y
    for i in range(equa.size):
        u[i]=equa.sign_hyst[i](t,x[i]*g[i]) # выход с реле 
        dy[i]=0 # чтобы суммировать в цикле
        for j in range(equa.size):
            
            dy[i] = dy[i]+a[i*equa.size+j]*y[j]+b[i]*u[i] #итоговый выход
    y = dy
    
    return y

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

def main1(phase_trace=False, transition=False, phase_plane = False):
    '''Решение уравнения и построения графика'''
    if phase_plane == True:
        equa = EquationClass.Equation.get_instance()
        solve = second_ode_solver(set_function_system,equa.ic,[equa.time_start, equa.time_end],  equa.step)
        t, y = solve.t, solve.y
        EquationClass.Equation.created = False
        
        if equa.size ==1:
            plot.draw_plot(t,y[0], 't, с', 'x1, значение', 'Решение уравнения')
            del equa
        elif equa.size == 2:
            plot.draw_plot(y[0],y[1],'x1, значение', 'x2, значение', 'Фазовая траектория')
            del equa
        else:
            del equa
            plot.draw_3d_plot(y[0], y[1], y[2],'x1, значение', 'x2, значение','x3, значение', 'Фазовое пространство')
           
        return 
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
