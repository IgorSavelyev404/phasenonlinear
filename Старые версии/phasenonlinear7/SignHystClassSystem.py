
import functions
import numpy as np
import EquationClass


''' Класс описывает реле с гистерезисом и различными параметрами'''

class SignHyst():

    def __init__(self, line_up=-0.1, line_down=0.1, up=1, down = -1, last_x=0, last_t=0, state = True, zapazdivanie = True):
        ''' Инициализация '''
        self.line_up= line_up
        self.line_down= line_down
        self.up = up
        self.down = down 
        self.last_x = last_x
        self.last_t = last_t
        self.in_hyst = False
        self.state = state
        self.last_state= state
        self.zapazdivanie = True

        

    def get_response(self,t,x):
        ''' получить выход'''
        equa = EquationClass.Equation.get_instance()        
        
        # Определение линии переключения 
        if self.state == True:
            self.bound = self.line_down
        else:
            self.bound = self.line_up
        # Проверка на нахождение в зоне гистерезиса
        if x < self.line_up and x >self.line_down:
                    self.in_hyst= True
        # В случае нахождения вне гистерезиса
        if self.in_hyst == False:
            # Проверка на последовательность по времени
            if t > self.last_t or t == self.last_t:
                y = functions.sign(t, x, input_bound = self.bound, out_upper= self.up, out_down= self.down)
                self.last_x = x
                self.last_t = t
                
            else:
                y = functions.sign(t, x, input_bound =self.bound, out_upper= self.up, out_down= self.down)
        else:
            # В случае нахождения в зоне гистерезиса
            y = functions.sign(t, x, input_bound = self.bound, out_upper = self.up, out_down= self.down)
            xlast=self.last_x
            self.last_x = x
            self.last_t = t
            # Определяем реле на опережение или запаздывание
            # Далее идет проверка на выход из зоны гистерезиса
            if self.zapazdivanie == True:
                if self.state == False and x > self.line_up or self.state == True and x < self.line_down:
                    self.in_hyst = False
                    self.state = not self.state
            else:
                if self.state == False and x < self.line_up or self.state == True and x > self.line_down:
                    self.in_hyst = False
                    self.state= not self.state
        return y       