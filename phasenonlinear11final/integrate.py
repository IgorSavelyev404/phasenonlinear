from scipy.integrate import solve_ivp
import plot
import numpy as np
import functions
import EquationClass
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
    equa = EquationClass.Equation.get_instance() # Находим обьект уравнения содержащий функции и переменные
    a, b, g = equa.A, equa.B, equa.G # Перезаписуем переменные в локальные для удобства
    x = y[:] # Копируем выход из прошлого интегрирования
    u=0 # Инициализируем выход реле
    dy=[0] * equa.size # Создаем массив выхода нужного размера
    for i in range(equa.size): 
        u=u+x[i]*g[i] # Считаем скалярное произведение
    u = equa.sign_hyst[0](t,u) # Считаем выход с реле
    if not hasattr(equa, 'last_u'): # В случае если это первый вызов
        equa.last_u = u
    if u != equa.last_u: # Считаем переключение, записываем координаты
        if equa.size == 3:
            equa.dots.append([t,x[0], x[1], x[2],])
        elif equa.size == 2 :
            equa.dots.append([t,x[0], x[1],])
    equa.last_u=u
    for i in range(equa.size):
        dy[i]=0
        for j in range(equa.size):
            dy[i] = dy[i]+a[i*equa.size+j]*y[j] # Считаем выход относительно коэффициентов системы
        dy[i]=dy[i]+b[i]*u - equa.disturb(t)*equa.f[i] # Добавляем выход реле и возмущение
    
    return dy

def set_function_2rank(t,y):
    '''Задание функции для решателя'''
    equa = EquationClass.Equation.get_instance() # Находим обьект уравнения содержащий функции и переменные
    a2, a1, a0, b0, b1, os = equa.a2, equa.a1, equa.a0, equa.b0, equa.b1, equa.os # Перезаписуем переменные в локальные для удобства
    equa.y, equa.dy, = y[0], y[1] # Сохраняем значение выхода с прошлого цикла
    print(equa.t_func)
    source = equa.t_func(t) # Применяем функцию для возмущающего воздействия по времени
    
    source = source - os*y[0] # Считаем обратную связь
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

def new_winF(dots,width): 
    ''' Создаем окно в которое записывает точки переключения и их координаты '''
    root=tk.Toplevel()
    root.title("Точки переключения")
    height = len(dots)
    width = width
    t = tk.Label(root,width=15, text="t")
    x1 = tk.Label(root,width=15, text="x1")
    x2 = tk.Label(root,width=15, text="x2")
    if width ==4:
        x3 = tk.Label(root,width=15, text="x3")
        dt = tk.Label(root,width=15, text="dt")
        x3.grid(row=0, column=3)
        dt.grid(row=0, column=4)
    elif width  == 3:
        dt = tk.Label(root,width=15, text="dt")
        dt.grid(row=0, column=3)
    t.grid(row=0, column=0)    
    x1.grid(row=0, column=1)
    x2.grid(row=0, column=2)
    
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
    

def main(phase_trace=False, transition=False, phase_plane = False):
    '''Решение уравнения и построения графика'''
    if phase_plane == True: # Если запущено построение фазовой плоскости
        equa = EquationClass.Equation.get_instance() # Находим обьект уравнения содержащий функции и переменные
        solve = second_ode_solver(set_function_system,equa.ic,[equa.time_start, equa.time_end],  equa.step) # Интегрируем
        t, y = solve.t, solve.y # Записуем результат интегрирования
               
        if equa.size ==1: # Если система первого порядка рисуем переходной процесс
            del equa
            plot.draw_plot(t,y[0], 't, с', 'x1, значение', 'Решение уравнения')
            
        elif equa.size == 2: # Если система второго порядка рисуем фазовую траекторию
            dots=equa.dots
            equa.dot_window=new_winF(dots,3)
            del equa
            plot.draw_plot(y[0],y[1],'x1, значение', 'x2, значение', 'Фазовая траектория')
            
        else: # Иначе рисуем фазовую плоскость
            g = equa.G
            l1=equa.l1
            l2=equa.l2
            dots=equa.dots
            equa.dot_window=new_winF(dots,4)
            plot.draw_3d_plot(y[0], y[1], y[2],'x1, значение', 'x2, значение','x3, значение', 'Фазовое пространство',g,l1,l2,dots)           
        return 
    else: # Если решается фазовая траектория
        equa = EquationClass.Equation.get_instance() # Находим обьект уравнения содержащий функции и переменные
        solve = second_ode_solver(set_function_2rank,(equa.y0, equa.dy0),[equa.time_start, equa.time_end],  equa.step) # Интегрируем
        t, y = solve.t, solve.y # Записуем результат интегрирования
        EquationClass.Equation.created = False # Удаляем уравнение
        del equa
    
    if transition: # Если рисуем переходной процесс
        plot.draw_plot(t,y[0], 't, с', 'y, значение', 'Решение уравнения')
    if phase_trace: # Если рисуем фазовую траекторию
        plot.draw_plot(y[0],y[1],'y, значение', 'dy, значение', 'Фазовая траектория')
