import numpy as np
import functions
import BacklashClass
import SignClass
import SignHystClass

class Equation():
    
    created= False    
    def __init__(self):
        self.x_func =[]

    @staticmethod
    def get_instance():
        if Equation.created == False:
            equa = Equation()
            Equation.created = equa
            return equa
        else:
            return Equation.created
  
    def set_t_func(self, func):
        '''Добавляем функцию для времени t'''
        self.t_func = func()
    
    def set_x_func(self, func):
        ''' Добавляем нелинейную функцию'''
        self.x_func.append(func())

    def set_initial_conditions(self, y0, dy0, ):
        ''' Задаем начальные значения '''
        self.y0, self.dy0, = y0, dy0, 
    
    def set_step(self, step):
        ''' Задаем шаг '''
        self.step = step
    
    def set_time(self, time_start, time_end):
        ''' Задаем промежуток времени для модуляции'''
        self.time_start = time_start
        self.time_end = time_end
        self.range_sol = np.arange(time_start, time_end, self.step)
    
    def set_os(self, os):
        ''' Задаем обратную связь'''
        if os == 'Нет':
            self.os = 0
        elif os == 'Отрицательная':
            self.os = 1
        else:
            self.os = -1 
    
    def dx(self, t, x):
        if self.array.size == 3:
            
            dx = np.gradient([self.array[1],x],[self.array[0],t])[-1]
        elif self.array.size < 16:
            index = self.array.size//2
            dx = np.gradient(self.array[-index :, 1],self.array[-index:, 0])[-1]
        else:
            index = 8
            dx = np.gradient(self.array[-index :, 1], self.array[-index:, 0])[-1]
        
        return dx
    
    def dx_prec(self, t, x):
        index_time = functions.find_nearest(self.array[:,0],t) #найдем ближашее время

        if self.array[:index_time].size < 16:
            index = self.array.size//2
            dx = np.gradient(self.array[ :, 1],self.array[:, 0])[-1]
        else:
            index = 8
            dx = np.gradient(self.array[ :, 1],self.array[:, 0])[-1]
        self.array = np.insert(self.array, index_time, [t,x], axis=0)
        
        return dx

    def d2x(self, t, x):
        if self.array.size < 16:
            index = self.array.size//2
            dx = np.gradient(self.array[-index :, 2],self.array[-index:, 0])[-1]
        else:
            index = 8
            dx = np.gradient(self.array[-index :, 2], self.array[-index:, 0])[-1]
        print(f'd2x is {dx}')
        return dx
    
    def d2x_prec(self, t, x):
        index_time = functions.find_nearest(self.array[:,0],t) #найдем ближашее время
        if self.array[:index_time].size < 16:
            index = self.array.size//2
            dx = np.gradient(self.array[ :, 2],self.array[:, 0])[-1]
        else:
            index = 8
            dx = np.gradient(self.array[ :, 2],self.array[:, 0])[-1]
        print(f'd2xprec is {dx}')
        return dx
    
    def backlash(self,):
        # Создаем обьект люфта и возращаем его метод возрат значения  
        blash = BacklashClass.Backlash()
        return blash.get_response

    def saturation(self):
        return functions.saturation
    
    def sign(self):
        signf = SignClass.Sign()
        return signf.get_response
       
    def sign_hyst(self):
        signf = SignHystClass.SignHyst()
        return signf.get_response

    def func_step(self):
        return functions.step
   
    def linear(self):
        return functions.linear
    
    def cos(self):
        return functions.cos
    
    def sin(self):
        return functions.sin
    
    def ramp(self):
        return functions.ramp
    
    def none(self):
        return lambda t: 0

    def get_function(self, string):
        func={
            'Время': self.linear,
            'Реле': self.sign,
            'Насыщение': self.saturation,
            'Люфт': self.backlash,
            'Косинус': self.cos,
            'Синус': self.sin,
            'Ступенька': self.func_step,
            'Линейная' : self.ramp,
            'Автономная(нет)': self.none,
            'Реле(гистерезис)': self.sign_hyst
            }
        return func[string]


