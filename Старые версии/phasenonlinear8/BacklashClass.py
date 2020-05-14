import functions
import numpy as np


class Backlash():

    def __init__(self, epsylon=0.7, amp=1,trashold =0):
        ''' Инициализация '''
        self.epsylon = 0.7
        self.amp = 1
        self.state = 0 #-1 убывает, 0 - стоит, 1 - возрастает
        self.array = np.array([[],[]]) # массив значений уже полученных [t, y]
        self.trashold = trashold # точка где началось измнение функции
        self.last_x = 0 # предыдущий запрос
    
    def get_response(self,t,x,dx):
        ''' получить выход'''
        
        if self.array.size < 10 or t > self.array[-1,0]: #проверка, это продолжение во времени или запрос на уточнение 
            if self.state == 1:
                if self.last_x < x: # случай когда функция возрастает 
                    y= x - self.epsylon/2
                else: #случай когда возрастающая функция перестала возрастать
                    self.trashold = self.last_x-self.epsylon/2
                    self.state = 0
                    y= self.trashold
            
            elif self.state == -1:
                if self.last_x > x: # случай когда функция убывает
                    y= x + self.epsylon/2  
                else: #случай когда убывающая функция перестала убывать
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
            # записуем в массив состояние обьекта
            if self.array.size == 0:
                self.array = np.array([t,x,y,self.state,self.trashold])
            else:
                self.array = np.vstack((self.array, [t,x, y, self.state, self.trashold]))
            # считаем производную
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
        else: #время уже было
            index = functions.find_nearest(self.array[:,0],t) #найдем ближашее время
            last_x, last_y, state, trashold = self.array[index,1], self.array[index, 2], self.array[index, 3], self.array[index, 4]
            
            if state == 1: #если функция возрастала
                if x > last_x:
                    y = x - self.epsylon/2
                else:
                    trashold = last_x- self.epsylon/2
                    state = 0
                    y= trashold
            elif state == -1: #если функция убывала
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

def main():
    'test'
    import plot
    n=1000 #number of steps
    x=np.linspace(0,10, n)
    y= np.array([])
    cos=np.array([])
    blash = Backlash(trashold =functions.sin(x[0]))
    for t in x:
        q= functions.sin(t)
        y=np.append(y,blash.get_response(t,q))
        cos = np.append(cos,q)
    
    for t in range(10):
        print(f'ask time {t}, fun {functions.sin(t)} get blash is {blash.get_response(t,functions.sin(t))}')
    plot.draw_plot(x,y,'t','y','test')
    plot.draw_plot(cos,y,'q','y','test')

if __name__ == '__main__':
    main()


