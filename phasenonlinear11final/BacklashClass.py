import functions
import numpy as np

''' Класс реализующий обьект типа "люфт"'''
class Backlash():

    def __init__(self, epsylon=0.7, amp=1,trashold =0):
        ''' Инициализация '''
        self.epsylon = 0.7
        self.amp = 1
        self.state = 0 # -1 убывает, 0 - стоит, 1 - возрастает
        self.array = np.array([[],[]]) # Массив значений уже полученных [t, y]
        self.trashold = trashold # Точка где началось измнение функции
        self.last_x = 0 # Предыдущий запрос
    
    def get_response(self,t,x,dx):
        ''' Получить выход'''
        
        if self.array.size < 10 or t > self.array[-1,0]: # Проверка, это продолжение во времени или запрос на уточнение 
            if self.state == 1:
                if self.last_x < x: # Случай когда функция возрастает 
                    y= x - self.epsylon/2
                else: # Случай когда возрастающая функция перестала возрастать
                    self.trashold = self.last_x-self.epsylon/2
                    self.state = 0
                    y= self.trashold
            
            elif self.state == -1:
                if self.last_x > x: # Случай когда функция убывает
                    y= x + self.epsylon/2  
                else: # Случай когда убывающая функция перестала убывать
                    self.trashold = self.last_x+self.epsylon/2
                    self.state = 0
                    y = self.trashold
            
            elif self.state == 0:
                if abs(self.trashold - x) < self.epsylon/2:
                    pass
                elif x < self.last_x:
                    self.state = -1
                elif x > self.last_x:
                    self.state = 1
                y = self.trashold
                
            self.last_x = x
            # Записуем в массив состояние обьекта
            if self.array.size == 0:
                self.array = np.array([t,x,y,self.state,self.trashold])
            else:
                self.array = np.vstack((self.array, [t,x, y, self.state, self.trashold]))
            # Считаем производную
            if self.array.size < 25:
                if self.array.size < 6:
                    dy=0
                else:
                    index = self.array.size//5
                    print(self.array.size)
                    dy = np.gradient(self.array[-index :, 2],self.array[-index:, 0])[-1]
            else:
                index = 5
                dy = np.gradient(self.array[-index :, 2], self.array[-index:, 0])[-1]
            return y, dy
        else: # Время уже было
            index = functions.find_nearest(self.array[:,0],t) #найдем ближашее время
            last_x, last_y, state, trashold = self.array[index,1], self.array[index, 2], self.array[index, 3], self.array[index, 4]
            
            if state == 1: # Если функция возрастала
                if x > last_x:
                    y = x - self.epsylon/2
                else:
                    trashold = last_x- self.epsylon/2
                    state = 0
                    y= trashold
            elif state == -1: # Если функция убывала
                if x < last_x:
                    y = x + self.epsylon/2
                else:
                    trashold = last_x + self.epsylon/2
                    state = 0
                    y= trashold
            elif state == 0:
                if abs(trashold - x) < self.epsylon/2:
                    pass
                elif x < last_x:
                    state = -1
                elif x > self.last_x:
                    state = 1
                y = trashold
            self.array = np.insert(self.array, index, [t,x, y, state, trashold], axis=0)
            dy = np.gradient(self.array[index-2 :index, 2], self.array[index-2:index, 0])[-1]
            return y, dy