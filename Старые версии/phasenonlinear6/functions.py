import numpy as np
import math

''' Набор линейных и нелинейных функций.
    также вспомогательные функции.'''

def signx(t,x, input_bound=0, out_upper=1, out_down=-1):
    '''Идеальное реле - два выхода'''
    if x > input_bound:
        return out_upper
    else:
        return out_down


def sign(t,x, input_bound=0, out_upper=1, out_mid=0, out_down=-1):
    '''Идеальное реле - три выхода'''
    if x > input_bound:
        return out_upper
    else:
        return out_down
  

  
def saturation(t, x, dx, upper=0.5, down=-0.5):
    ''' Насыщение -
    все значения выше upper = upper
    все значения ниже down = down
    '''
    if x> upper:
        x = upper
        dx = 0
    elif x< down:
        x = down
        dx = 0
    return x, dx

def sin(x):
    return np.sin(x)

def cos(x):
    return np.cos(x)

def step(x, delay=0, amp=1, initial_output=0):
    '''Ступенька, с задержкой delay, 
    амплитудой amp и 
    начальным выходом initial_output
    '''
    if x>delay:
        x= amp
    else:
        x= initial_output
    return x

def ramp(t,x,dx, slope=1):
    '''Линейная зависимость с коэфициентом slope'''
    return x*slope, dx

def linear(x):
    return x
    
def find_nearest(array, value):
    '''Найти ближайшие значение value
    в массиве array'''
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx
