import functions
import numpy as np
import EquationClass


class SignHyst():

    def __init__(self, line_up=-0.1, line_down=0.1, up=1, down = -1):
        ''' Инициализация '''
        self.line_up= line_up
        self.line_down= line_down
        self.up = up
        self.down = down 
        self.switch = False

    def get_response(self,t,x,dx):
        ''' получить выход'''
        equa = EquationClass.Equation.get_instance()
        # Определяем производную
        if equa.dy <0:
            bound = self.line_down
        else:
            bound = self.line_up 
        if self.switch == True:
            dy = -2*np.sign(equa.dy)*200
            if abs(equa.dy - self.ddy) > abs(2*equa.b0):
                self.switch = False
                dy=0
        elif (abs(self.line_up - x) < equa.step) and equa.dy > 0:
            #print(f'line up x is {x}, dy is {equa.dy}, t is {t} abs is {abs(self.line_up - x)}')
            dy = -2*np.sign(equa.dy)*100
            self.switch = True
            self.ddy = equa.dy
        elif abs(self.line_down - x) < equa.step and equa.dy < 0:
            #print(f'line down x is {x}, dy is {equa.dy}')
            dy = -2*np.sign(equa.dy)*100
            self.switch = True
            self.ddy = equa.dy
        else:
            dy = 0
        y = functions.sign(t, x, input_bound =bound, out_upper= self.up, out_down= self.down)
        return y, dy