import functions
import numpy as np
import EquationClass


class Sign():

    def __init__(self, line=0, up=1, down = -1):
        ''' Инициализация '''
        self.line = line
        self.up = up
        self.down = down
        self.switch = False

    def get_response(self,t,x,dx):
        ''' получить выход'''
        equa = EquationClass.Equation.get_instance()
        # Определяем производную
        if self.switch == True:
            dy = -2*np.sign(equa.dy)*200
            if abs(equa.dy - self.ddy) > abs(2*equa.b0):
                self.switch = False
                dy=0
        elif abs(self.line - x) < equa.step:
            dy = -2*np.sign(equa.dy)*100
            self.switch = True
            self.ddy = equa.dy
        else:
            dy = 0
        y = functions.sign(t, x)
        #print(f'y is {y}, dy is {dy} switch is {self.switch}')
        return y, dy