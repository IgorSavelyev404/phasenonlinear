import integrate
import EquationClass
import SignHystClass1
import functions
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from window import Win

'''Файл создает пользовательский интерфейс, 
   обрабатывает с него ввод, и запускает решение'''

fields = ('coef','a0', 'a1', 'a2','b0','b1','time','t','func','x','ic','y(0)', "y'(0)",'Обратная связь','pr','Начало расчета', 'Конец расчета','Шаг')
root = tk.Tk()
root.title('Построения фазовых траекторий')
root.minsize(600,400)
entries_matr={}

def makeform_for_system(root, fields):
    row = tk.Frame(root)
    lab_primer= tk.Label(row, width=20, text="Выбрать пример", anchor='w')
    lab_primer.pack(side=tk.LEFT)
    combo_primer = Combobox(row, width=10)
    combo_primer.pack(side=tk.LEFT,)
    combo_primer['values'] = ('1','2','5','6','7','8','9')
    combo_primer.bind("<<ComboboxSelected>>", combo_primer_callback)
    lab = tk.Label(row, width=20, text="Размеры матрицы А:", anchor='w')
    lab.pack(side=tk.LEFT)
    combo_size_A = Combobox(row, width=10)
    combo_size_A.pack(side=tk.LEFT,)
    combo_size_A['values'] = ('1x1', '2x2',
                       '3x3', '4x4', '5x5')
    combo_size_A.current(2)
    combo_size_A.bind("<<ComboboxSelected>>", combo_size_A_callback)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row = tk.Frame(root)
    size_A = int(combo_size_A.get()[0])
    
    entries_matr['A'] =make_matrix(size_A,row)
    row = tk.Frame(root)
    lab1 = tk.Label(row, width=20, text="B=", anchor='w')
    lab1.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row = tk.Frame(root)
    entries_matr['B'] = make_B(size_A, row)
    row= tk.Frame(root)
    lab2 = tk.Label(row, width=20, text="Г=", anchor='w')
    lab2.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row = tk.Frame(root)
    entries_matr['G'] =make_G(size_A, row)
    row= tk.Frame(root)
    lab2 = tk.Label(row, width=20, text="Реле с гистерезисом:", anchor='w')
    lab2.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row= tk.Frame(root)
    lab_l1 = tk.Label(row, width=20, text="Переключение вверх l2", anchor='w')
    lab_l1.grid(row=0, column=0)
    ent_l1 = tk.Entry(row, width=5)
    ent_l1.insert(0, "1")
    ent_l1.grid(row=0, column=1)
    entries_matr['l1'] = ent_l1

    lab_l2 = tk.Label(row, width=20, text="Переключение вниз l1", anchor='w')
    lab_l2.grid(row=0, column=2)
    ent_l2 = tk.Entry(row, width=5)
    ent_l2.insert(0, "1")
    ent_l2.grid(row=0, column=3)
    entries_matr['l2'] = ent_l2

    lab_m1 = tk.Label(row, width=20, text="Верхнее значение m2", anchor='w')
    lab_m1.grid(row=0, column=4)
    ent_m1 = tk.Entry(row, width=5)
    ent_m1.insert(0, "1")
    ent_m1.grid(row=0, column=5)
    entries_matr['m1'] = ent_m1

    lab_m2 = tk.Label(row, width=20, text="Нижнее значение  m1", anchor='w')
    lab_m2.grid(row=0, column=6)
    ent_m2 = tk.Entry(row, width=5)
    ent_m2.insert(0, "1")
    ent_m2.grid(row=0, column=7)
    entries_matr['m2'] = ent_m2
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)

    row = tk.Frame(root)
    lab = tk.Label(
        row, width=40, text="Начальные условия", anchor='w')
    lab.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row = tk.Frame(root)
    entries_matr['ic'] = make_ic(size_A, row)

    row = tk.Frame(root)
    lab_par = tk.Label(row, width=20, text="Параметры расчета:", anchor='w')
    lab_par.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    #начало расчета
    row = tk.Frame(root)
    lab_start = tk.Label(row, width=15, text="Начало расчета:", anchor='w')
    ent_start = tk.Entry(row, width=10)
    ent_start.insert(0, "0")
    lab_start.pack(side=tk.LEFT)
    ent_start.pack(side=tk.LEFT)
    entries_matr['Начало расчета'] = ent_start
    # конец расчета
    lab_end = tk.Label(row, width=15, text='Конец расчета:', anchor='w')
    lab_end.pack(side=tk.LEFT)
    ent_end = tk.Entry(row, width=10)
    ent_end.insert(20, "20")
    ent_end.pack(side=tk.LEFT)
    entries_matr['Конец расчета'] = ent_end
    # Шаг
    lab_step = tk.Label(row, width=10, text='Шаг:', anchor='w')
    lab_step.pack(side=tk.LEFT)
    ent_step = tk.Entry(row, width=10)
    ent_step.insert(0, "0.01")
    ent_step.pack(side=tk.LEFT)
    entries_matr['step'] = ent_step
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row=  tk.Frame(root) 
    lab_type = tk.Label(row, width=15, text='Тип гистерезиса:', anchor='w')
    lab_type.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    combo_hyst = Combobox(row, width=20)
    combo_hyst.pack(side=tk.LEFT,padx=10)
    combo_hyst['values'] = ['С запаздыванием', 'С опережением']
    combo_hyst.current(0)
    entries_matr['hyst'] = combo_hyst
    lab_vkl = tk.Label(row, width=30, text='Начальное положение реле:', anchor='w')
    lab_vkl.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    combo_vkl = Combobox(row, width=20)
    combo_vkl.pack(side=tk.LEFT,padx=10)
    combo_vkl['values'] = ['Верх', 'Низ']
    combo_vkl.current(0)
    entries_matr['vkl'] = combo_vkl
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row=  tk.Frame(root) 
    lab5 = tk.Label(row, width=45, text="X'= AX+Bu(X,Г)-f(t)", anchor='w')
    lab5.configure(font=("Times New Roman", 12, ))
    lab5.pack(padx=100)
    row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=10, 
                 pady=10)
    row=  tk.Frame(root)
    lab_par = tk.Label(row, width=30, text="Возмущающее воздействие:", anchor='w')
    lab_par.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    row = tk.Frame(root)
    lab_f1 = tk.Label(row, width=5, text="f1:", anchor='w')
    ent_f1 = tk.Entry(row, width=10)
    ent_f1.insert(0, "1")
    lab_f1.pack(side=tk.LEFT)
    ent_f1.pack(side=tk.LEFT)
    entries_matr['f1'] = ent_f1
    
    lab_f2 = tk.Label(row, width=5, text="f2:", anchor='w')
    ent_f2 = tk.Entry(row, width=10)
    ent_f2.insert(0, "1")
    lab_f2.pack(side=tk.LEFT)
    ent_f2.pack(side=tk.LEFT)
    entries_matr['f2'] = ent_f2
    
    lab_f3 = tk.Label(row, width=5, text="f3:", anchor='w')
    ent_f3 = tk.Entry(row, width=10)
    ent_f3.insert(0, "1")
    lab_f3.pack(side=tk.LEFT)
    ent_f3.pack(side=tk.LEFT)
    entries_matr['f3'] = ent_f3
 
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
            
    row=  tk.Frame(root) 
    lab_type = tk.Label(row, width=35, text='Тип возмущающего воздействия:', anchor='w')
    lab_type.pack(side=tk.LEFT)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    combo_f = Combobox(row, width=40)
    combo_f.pack(side=tk.LEFT,padx=10)
    combo_f['values'] = ['f(t) = v0 + exp(alpha*t)*k*sin(phi + wt))', 'Нет']
    combo_f.current(1)
    combo_f.bind("<<ComboboxSelected>>", combo_f_callback)
    entries_matr['f'] = combo_f
    
    row = tk.Frame(root)
    lab_v0 = tk.Label(row, width=5, text="v0:", anchor='w')
    ent_v0 = tk.Entry(row, width=10)
    ent_v0.insert(0, "1")
    lab_v0.pack(side=tk.LEFT)
    ent_v0.pack(side=tk.LEFT)
    entries_matr['v0'] = ent_v0
    
    
    lab_al = tk.Label(row, width=5, text="alpha:", anchor='w')
    ent_al = tk.Entry(row, width=10)
    ent_al.insert(0, "1")
    lab_al.pack(side=tk.LEFT)
    ent_al.pack(side=tk.LEFT)
    entries_matr['al'] = ent_al
    
    lab_k = tk.Label(row, width=5, text="k:", anchor='w')
    ent_k = tk.Entry(row, width=10)
    ent_k.insert(0, "1")
    lab_k.pack(side=tk.LEFT)
    ent_k.pack(side=tk.LEFT)
    entries_matr['k'] = ent_k
    
    lab_phi = tk.Label(row, width=5, text="phi:", anchor='w')
    ent_phi = tk.Entry(row, width=10)
    ent_phi.insert(0, "1")
    lab_phi.pack(side=tk.LEFT)
    ent_phi.pack(side=tk.LEFT)
    entries_matr['phi'] = ent_phi

    lab_w = tk.Label(row, width=5, text="w:", anchor='w')
    ent_w = tk.Entry(row, width=10)
    ent_w.insert(0, "1")
    lab_w.pack(side=tk.LEFT)
    ent_w.pack(side=tk.LEFT)
    entries_matr['w'] = ent_w
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=30)

    entries_matr['size'] = size_A
    
    ents = entries_matr
    b1 = tk.Button(root, text='Построить фазовую плоскость',
                   command=(lambda e=ents: phase_plane(e)))
    b1.pack(side=tk.LEFT, padx=10, pady=5)
    b4 = tk.Button(root, text='Выход', command=root.quit)
    b4.pack(side=tk.RIGHT, padx=10, pady=5)

def combo_primer_callback(event):
    primer = int(event.widget.get()[0])
    frames = root.pack_slaves()
    if primer==1:
        a= frames[2].grid_slaves()
       
        for i in range(9):
            a[2*i].delete(0,'end')
            a[2*i].insert(0,'1')
        a[16].insert(0, "-")
        a[12].delete(0,'end')
        a[12].insert(0, "0")
        a[10].insert(0, "-")
        a[8].insert(0, "-")
        a[6].delete(0,'end')
        a[6].insert(0, "0")
        a[4].delete(0,'end')
        a[4].insert(0, "0")
        a[2].delete(0,'end')
        a[2].insert(0, "0")
        a[0].delete(0,'end')
        a[0].insert(0, "-3")

        b = frames[4].grid_slaves()
        for i in range(3):
            b[i*2].delete(0,'end')
            b[i*2].insert(0,'1')
        b[2].insert(0, "0.")
        b[4].insert(0, "0.")

        g = frames[6].grid_slaves()
        for i in range(3):
            g[i*2].delete(0,'end')
            g[i*2].insert(0,'1')
        g[0].delete(0,'end')
        g[0].insert(0, "-2")
        g[2].insert(0, "-0.")
        g[4].insert(0, "-0.")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-2")
        l[2].delete(0,'end')
        l[2].insert(0, "2")
        l[4].delete(0,'end')
        l[4].insert(0, "-1")
        l[6].delete(0,'end')
        l[6].insert(0, "1")
    if primer==2:
        a= frames[2].grid_slaves()
        for i in range(9):
            a[2*i].delete(0,'end')
            a[2*i].insert(0,'1')
        a[16].insert(0, "-")
        a[14].delete(0,'end')
        a[14].insert(0, "-1.5")
        a[12].delete(0,'end')
        a[12].insert(0, "0")
        a[10].delete(0,'end')
        a[10].insert(0, "-1.5")
        a[8].insert(0, "-")
        a[6].delete(0,'end')
        a[6].insert(0, "0")
        a[4].delete(0,'end')
        a[4].insert(0, "0")
        a[2].delete(0,'end')
        a[2].insert(0, "0")
        a[0].delete(0,'end')
        a[0].insert(0, "-2")

        b = frames[4].grid_slaves()
        for i in range(3):
            b[i*2].delete(0,'end')
            b[i*2].insert(0,'1')
        b[0].insert(0, "0.")

        g = frames[6].grid_slaves()
        for i in range(3):
            g[i*2].delete(0,'end')
            g[i*2].insert(0,'1')
        g[0].delete(0,'end')
        g[0].insert(0, "0")
        g[4].delete(0,'end')
        g[4].insert(0, "0")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-10")
        l[2].delete(0,'end')
        l[2].insert(0, "10")
        l[4].delete(0,'end')
        l[4].insert(0, "-1.5")
        l[6].delete(0,'end')
        l[6].insert(0, "1.5")
    if primer==5:
        a= frames[2].grid_slaves()
        for i in range(9):
            a[2*i].delete(0,'end')            
        a[16].insert(0, "-1")
        a[14].insert(0, "1")
        a[12].insert(0, "0")
        a[10].insert(0, "-1")
        a[8].insert(0, "0")
        a[6].insert(0, "0")
        a[4].insert(0, "0")
        a[2].insert(0, "0")        
        a[0].insert(0, "-2")
        b = frames[4].grid_slaves()
        for i in range(3):
            b[i*2].delete(0,'end')
        b[4].insert(0, "2")
        b[2].insert(0, "-1")
        b[0].insert(0, "-2")

        g = frames[6].grid_slaves()
        for i in range(3):
            g[i*2].delete(0,'end')
        g[4].insert(0, "0")
        g[2].insert(0, "-0.13")
        g[0].insert(0, "2.9")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-1.4024")
        l[2].delete(0,'end')
        l[2].insert(0, "1.4024")
        l[4].delete(0,'end')
        l[4].insert(0, "-3.5")
        l[6].delete(0,'end')
        l[6].insert(0, "3.5")
    if primer==6:
        a= frames[2].grid_slaves()
        for i in range(9):
            a[2*i].delete(0,'end')            
        a[16].insert(0, "-0.05")
        a[14].insert(0, "0")
        a[12].insert(0, "0")
        a[10].insert(0, "0")
        a[8].insert(0, "-0.1")
        a[6].insert(0, "1")
        a[4].insert(0, "0")
        a[2].insert(0, "-1")        
        a[0].insert(0, "-0.1")
        b = frames[4].grid_slaves()
        for i in range(3):
            b[i*2].delete(0,'end')
        b[4].insert(0, "-1")
        b[2].insert(0, "-1")
        b[0].insert(0, "-1")

        g = frames[6].grid_slaves()
        for i in range(3):
            g[i*2].delete(0,'end')
        g[4].insert(0, "0.2")
        g[2].insert(0, "0.2")
        g[0].insert(0, "0")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-1")
        l[2].delete(0,'end')
        l[2].insert(0, "1")
        l[4].delete(0,'end')
        l[4].insert(0, "-1")
        l[6].delete(0,'end')
        l[6].insert(0, "1")
    if primer==7:
        a= frames[2].grid_slaves()
        for i in range(9):
            a[2*i].delete(0,'end')            
        a[16].insert(0, "-0.05")
        a[14].insert(0, "1")
        a[12].insert(0, "0")
        a[10].insert(0, "-1")
        a[8].insert(0, "-0.05")
        a[6].insert(0, "0")
        a[4].insert(0, "0")
        a[2].insert(0, "0")        
        a[0].insert(0, "1")
        b = frames[4].grid_slaves()
        for i in range(3):
            b[i*2].delete(0,'end')
        b[4].insert(0, "1")
        b[2].insert(0, "1")
        b[0].insert(0, "1")

        g = frames[6].grid_slaves()
        for i in range(3):
            g[i*2].delete(0,'end')
        g[4].insert(0, "-0.9615")
        g[2].insert(0, "0")
        g[0].insert(0, "-0.9615")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-1")
        l[2].delete(0,'end')
        l[2].insert(0, "1")
        l[4].delete(0,'end')
        l[4].insert(0, "-1")
        l[6].delete(0,'end')
        l[6].insert(0, "1")
    if primer==8:
        a= frames[2].grid_slaves()
        for i in range(4):
            a[2*i].delete(0,'end')            
        a[6].insert(0, "-4")
        a[4].insert(0, "0")
        a[2].insert(0, "1")
        a[0].delete(0, "-4")
        a[0].insert(0, "-4")
        b = frames[4].grid_slaves()
        for i in range(2):
            b[i*2].delete(0,'end')
        b[2].insert(0, "-1")
        b[0].insert(0, "0")

        g = frames[6].grid_slaves()
        for i in range(2):
            g[i*2].delete(0,'end')
        g[2].insert(0, "1")
        g[0].insert(0, "1")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-5.8")
        l[2].delete(0,'end')
        l[2].insert(0, "2.2")
        l[4].delete(0,'end')
        l[4].insert(0, "-1")
        l[6].delete(0,'end')
        l[6].insert(0, "1")
    if primer==9:
        a= frames[2].grid_slaves()
        for i in range(4):
            a[2*i].delete(0,'end')            
        a[6].insert(0, "-2")
        a[4].insert(0, "0")
        a[2].insert(0, "0")
        a[0].delete(0, "-4")
        a[0].insert(0, "-3")
        b = frames[4].grid_slaves()
        for i in range(2):
            b[i*2].delete(0,'end')
        b[2].insert(0, "-1")
        b[0].insert(0, "-1")

        g = frames[6].grid_slaves()
        for i in range(2):
            g[i*2].delete(0,'end')
        g[2].insert(0, "2")
        g[0].insert(0, "0")
        l = frames[8].grid_slaves()
        l[0].delete(0,'end')
        l[0].insert(0, "-2")
        l[2].delete(0,'end')
        l[2].insert(0, "2")
        l[4].delete(0,'end')
        l[4].insert(0, "-1")
        l[6].delete(0,'end')
        l[6].insert(0, "1")
        
        
        



def combo_size_A_callback(event):
    size = int(event.widget.get()[0])
    frames = root.pack_slaves()
    entries_matr['A'] = make_matrix(size, frames[2])
    entries_matr['B'] = make_B(size, frames[4])
    entries_matr['G'] = make_G(size, frames[6])
    entries_matr['x0'] = make_ic(size, frames[10])
    entries_matr['size'] = size
def combo_f_callback(event):
    pass
def make_B(size, frame):
    list1 = frame.grid_slaves()
    for l in list1:
        l.destroy()
    lab_B=[[None] for i in range(size)]
    ent_B=[[None] for i in range(size)]
    for i in range(size):
        lab_B[i] = tk.Label(frame, width=5, text="b" +
                               str(i), anchor='w')
        lab_B[i].grid(row=0, column=i*2)
        ent_B[i] = tk.Entry(frame, width=5)
        ent_B[i].insert(0, "1")
        ent_B[i].grid(row=0, column=i*2+1)
    frame.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
    entries_matr['B'] = ent_B
    return ent_B

def make_G(size, frame):
    list1 = frame.grid_slaves()
    for l in list1:
        l.destroy()
    lab_G=[[None] for i in range(size)]
    ent_G=[[None] for i in range(size)]
    for i in range(size):
        lab_G[i] = tk.Label(frame, width=5, text="г" +
                               str(i), anchor='w')
        lab_G[i].grid(row=0, column=i*2)
        ent_G[i] = tk.Entry(frame, width=5)
        ent_G[i].insert(0, "1")
        ent_G[i].grid(row=0, column=i*2+1)
    frame.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
    entries_matr['G'] = ent_G
    return ent_G

def make_ic(size, frame):
    list1 = frame.grid_slaves()
    for l in list1:
        l.destroy()
    lab_ic=[[None] for i in range(size)]
    ent_ic=[[None] for i in range(size)]
    for i in range(size):
        lab_ic[i] = tk.Label(frame, width=5, text="x" +
                               str(i)+'_0', anchor='w')
        lab_ic[i].grid(row=0, column=i*2)
        ent_ic[i] = tk.Entry(frame, width=5)
        ent_ic[i].insert(0, "1")
        ent_ic[i].grid(row=0, column=i*2+1)
        
    frame.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
    entries_matr['ic'] = ent_ic
    return ent_ic

def make_matrix(size_A, frame):
    list1 = frame.grid_slaves()
    for l in list1:
        l.destroy()
    lab_A=[[None]*size_A for i in range(size_A)]
    ent_A=[[None]*size_A for i in range(size_A)]
    for i in range(size_A):
        for j in range(size_A):
            lab_A[i][j] = tk.Label(frame, width=4, text="а"+str(i)+str(j), anchor='w')
            lab_A[i][j].grid(row=i, column=j*2)
            ent_A[i][j] = tk.Entry(frame, width =4)
            ent_A[i][j].insert(0, "1")
            ent_A[i][j].grid(row=i, column=j*2+1)
    frame.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
    entries_matr['A'] = ent_A
    return ent_A
            



def makeform(root, fields):
    ''' Настройка расположения элементов в интерфейсе '''
    entries = {}
    values=('Линейная','Реле','Реле(гистерезис)', 'Люфт', 'Насыщение')
    row = tk.Frame(root)
    for field in fields:
        if field == 'coef':
            row = tk.Frame(root)
            lab = tk.Label(row, width=20, text="Коэфициенты уравнения:" , anchor='w')
            lab.pack(side=tk.LEFT)
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            row = tk.Frame(root)
            continue
        if field == 'time':
            row = tk.Frame(root)
            lab = tk.Label(row, width=20, text="Функция для t:" , anchor='w')
            lab.pack(side=tk.LEFT)
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            row = tk.Frame(root)
            continue
        if field == 't':
            row = tk.Frame(root)
            lab = tk.Label(row, width=5, text=field+": ", anchor='w')
            lab.pack(side=tk.LEFT)
            combo = Combobox(row, width=20)
            combo.pack(side=tk.LEFT,)
            combo['values'] =('Время','Автономная(нет)', 'Синус', 'Косинус', 'Ступенька')
            combo.current(1)
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            combo.pack(side=tk.LEFT)
            entries[field] = combo
            continue
        
        if field == 'func':
            row = tk.Frame(root)
            lab = tk.Label(row, width=26, text="Нелинейные функциии для х:" , anchor='w')
            lab.pack(side=tk.LEFT)
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            row = tk.Frame(root)
            continue
        
        if field == 'x':
            row = tk.Frame(root)
            lab3 = tk.Label(row, width=5, text='х:', anchor='w')
            lab3.pack(side=tk.LEFT)
            combo1 = Combobox(row, width=20)
            combo1.pack(side=tk.LEFT,padx=10)
            combo1['values'] =values
            combo1.current(0)
            combo2 = Combobox(row, width=20)
            combo2.pack(side=tk.LEFT,padx=10)
            combo2['values'] =values
            combo2.current(0)
            combo3 = Combobox(row, width=20)
            combo3.pack(side=tk.LEFT,padx=10)
            combo3['values'] =values
            combo3.current(0)
            entries[field] = [combo1, combo2, combo3]
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            continue

        if field == 'ic':
            row = tk.Frame(root)
            lab = tk.Label(row, width=40, text="Начальные условия и обратная связь:" , anchor='w')
            lab.pack(side=tk.LEFT)
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            row = tk.Frame(root)
            continue
        
        if field =='y(0)':
            row = tk.Frame(root)
            lab = tk.Label(row, width=5, text=field+": ", anchor='w')
            ent = tk.Entry(row, width =10)
            ent.insert(0, "-0.5")
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.LEFT, 
                 fill=tk.X)
            entries[field] = [ent]
            continue
        if field =='Обратная связь':
            lab3 = tk.Label(row, width=3, text='', anchor='w')
            lab3.pack(side=tk.LEFT, padx =3)
            lab4 = tk.Label(row, width=12, text='Обратная связь', anchor='w')
            lab4.pack(side=tk.LEFT, padx =5)
            combo2 = Combobox(row, width=14)
            combo2.pack(side=tk.LEFT,padx=10)
            combo2['values'] =['Нет', 'Отрицательная', 'Положительная']
            combo2.current(1)
            entries[field] = [combo2]
            continue
        if field == 'pr':
            row = tk.Frame(root)
            lab = tk.Label(row, width=30, text="Параметры расчета:" , anchor='w')
            lab.pack(side=tk.LEFT)
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            row = tk.Frame(root)
            continue

        if field == 'Начало расчета':
            row = tk.Frame(root)
            lab = tk.Label(row, width=15, text=field+": ", anchor='w')
            ent = tk.Entry(row, width =10)
            ent.insert(0, "0")
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.LEFT, 
                 fill=tk.X)
            entries[field] = [ent]
            continue
        if field == 'Конец расчета':
            lab2 =tk.Label(row, width=4, text='', anchor='w')
            lab2.pack(side=tk.LEFT)
            lab = tk.Label(row, width=15, text=field+": ", anchor='w')
            ent = tk.Entry(row, width =10)
            ent.insert(20, "20")
            row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.LEFT, 
                 fill=tk.X)
            entries[field] = [ent]
            continue
        lab = tk.Label(row, width=5, text=field+": ", anchor='w')
        ent = tk.Entry(row, width =10)
        if  field == "y'(0)":
            ent.insert(0, "2")
        elif field == "a2":
            ent.insert(0, "0")
        elif field == "b0":
            ent.insert(0, "-0.5")
        elif field == "b1":
            ent.insert(0, "-0.5")
        else:
            ent.insert(1, "1")
        if field == 'Шаг':
            ent.insert(0, "0.0")                 
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.LEFT, 
                 fill=tk.X)
        entries[field] = [ent]
    row = tk.Frame(root)
    lab.pack(side=tk.LEFT)
    lab = tk.Label(row, width=45, text="a0y'''(x)+a1y''(x)+a2y'(x)+a3y(x)= b0x'(t,y)+b1x(t,y)", anchor='w')
    lab.configure(font=("Times New Roman", 12, ))
    row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=100, 
                 pady=30)
    lab.pack()
    ents=entries
    b1 = tk.Button(root, text='Построить фазовую траекторию',
                   command=(lambda e=ents: phase_trace(e)))
    b1.pack(side=tk.LEFT, padx=10, pady=5)
    b2 = tk.Button(root, text='Построить график решения уравнения',
                   command=(lambda e=ents: transition_process(e)))
    b2.pack(side=tk.LEFT, padx=10, pady=5)
    b4 = tk.Button(root, text='Выход', command=root.quit)
    b4.pack(side=tk.RIGHT, padx=10, pady=5)
    return entries


def set_input(e):
    '''Забираем значения из ввода пользователя'''
    x_func=[]
    a0 = float(e['a0'][0].get())
    a1 = float(e['a1'][0].get())
    a2 = float(e['a2'][0].get())
    b0 = float(e['b0'][0].get())
    b1 = float(e['b1'][0].get())
    
    a=e['t']
    t=a.get()
    os = e['Обратная связь'][0].get()
    y0 = float(e['y(0)'][0].get())
    dy0 = float(e["y'(0)"][0].get())
    
    start_time = int(e['Начало расчета'][0].get())
    end_time = int(e['Конец расчета'][0].get())
    step = float(e['Шаг'][0].get())
    for fun in e['x']:
        x_func.append(fun.get())
    # Настраиваем и задаем параметры для уравнения
    equa = EquationClass.Equation.get_instance()
    equa.set_step(step)
    equa.set_time(start_time, end_time)
    
    equa.a2=a2
    equa.a1=a1
    equa.a0=a0
    equa.set_initial_conditions(y0, dy0,)
    equa.b0=b0
    equa.line = False
    equa.b1=b1
    
    equa.set_t_func(equa.get_function(t))
    for fun in x_func:
        equa.set_x_func(equa.get_function(fun))
    equa.set_os(os)
      

def phase_trace(e):
    '''Обработка нажатия кнопки построения фазовой траектории'''
    try:
        set_input(e)
    except Exception as error: 
        print(error)
        messagebox.showinfo('Ошибка','Проверьте правильность заданных параметров')
    else:
        integrate.main1(phase_trace = True)
    
def transition_process(e):
    '''Обработка нажатия кнопки построения динамической характеристики
        обьекта описываемого уравнением'''
    try:
        set_input(e)
    except Exception as e: 
        print(e)
        messagebox.showinfo('Ошибка','Проверьте правильность заданных параметров')
    else:
        integrate.main1(transition=True)

def set_input_matr(e):
    '''Забираем значения из ввода пользователя'''
    
    equa = EquationClass.Equation.get_instance()
    if hasattr(equa, 'dot_window'):
        print(equa.dot_window)
        equa.dot_window.destroy()
    EquationClass.Equation.created = False
    del equa
    equa = EquationClass.Equation.get_instance()
    equa.A, equa.B, equa.G, equa.ic, equa.dots = [],[],[],[],[]
    equa.size = e['size']
    for i in e['A']:
        for j in i:
            equa.A.append(float(j.get()))
    for i in e['B']:
        equa.B.append(float(i.get()))
    for i in e['G']:
        equa.G.append(float(i.get()))
    for i in e['ic']:
        equa.ic.append(float(i.get()))
 
    l1= float(e['l1'].get())
    l2= float(e['l2'].get())
    m1= float(e['m1'].get())
    m2= float(e['m2'].get())
    hyst = e['hyst'].get()
    equa.l1=l1
    equa.l2=l2
    equa.dots= []
    start_time = int(e['Начало расчета'].get())
    end_time = int(e['Конец расчета'].get())
    step = float(e['step'].get())
    equa.set_step(step)
    equa.set_time(start_time, end_time)
    equa.line = False
    if e['vkl'].get() == 'Верх':
        vkl = True
    else:
        vkl = False
    equa.f=[]
    if e['f'].get() == 'f(t) = v0 + exp(alpha*t)*k*sin(phi + wt))':
        equa.v0=float(e['v0'].get())
        equa.k=float(e['k'].get())
        equa.al=float(e['al'].get())
        equa.phi=float(e['phi'].get())
        equa.w=float(e['w'].get())
        equa.disturb = equa.sine_dist
        
        equa.f.append(float(e['f1'].get()))
        equa.f.append(float(e['f2'].get()))
        equa.f.append(float(e['f3'].get()))
    else:
        equa.disturb = equa.none(0)
        equa.f=[0,0,0]
    equa.sign_hyst=[]
    last_x = 0
    for i in range(equa.size):
        last_x =last_x + equa.ic[i]*equa.G[i]
    print(vkl)
    if hyst == 'С запаздыванием':
        sign=SignHystClass1.SignHyst(line_up=l1, line_down=l2, up = m1, down = m2, last_x = last_x, last_t = start_time, state = vkl)
        equa.sign_hyst.append(sign.get_response_zapazdivanie)
            
    elif hyst == 'С опережением':
        sign=SignHystClass1.SignHyst(line_up=l1, line_down=l2, up = m1, down = m2, last_x =last_x, last_t = start_time, state = vkl)
        equa.sign_hyst.append(sign.get_response_operezenie)
            
        

    
def phase_plane(e):
    '''Обработка нажатия кнопки построения фазовой плоскости'''
    try:
        set_input_matr(e)
    except Exception as error: 
        print(error)
        messagebox.showinfo('Ошибка','Проверьте правильность заданных параметров')
    else:
        integrate.main1(phase_plane = True)

def make_system():
    list1 = root.pack_slaves()
    for l in list1:
        l.destroy()
    row = tk.Frame(root)
    combo_type = Combobox(row, width=20)
    combo_type.pack(side=tk.LEFT,padx=10)
    combo_type['values'] = ['Система', 'Уравнение 3 порядка']
    combo_type.bind("<<ComboboxSelected>>", combo_type_callback)
    combo_type.current(0)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    ents = makeform_for_system(root, fields)

def make_eqution2():
    list1 = root.pack_slaves()
    for l in list1:
        l.destroy()
    row = tk.Frame(root)
    combo_type = Combobox(row, width=20)
    combo_type.pack(side=tk.LEFT,padx=10)
    combo_type['values'] = ['Система', 'Уравнение 3 порядка']
    combo_type.bind("<<ComboboxSelected>>", combo_type_callback)
    combo_type.current(1)
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    ents = makeform(root, fields)
   


def combo_type_callback(event):
    if (event.widget.get()) == 'Уравнение 3 порядка':
        make_eqution2()
    elif (event.widget.get()) == 'Система':
        make_system()


if __name__ == '__main__':
    ''' Создает интерфейс в ткинтер '''
    make_system()
    root.mainloop()
