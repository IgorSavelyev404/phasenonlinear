
import functions
import numpy as np
import EquationClass


class SignHyst():

    def __init__(self, line_up=-0.1, line_down=0.1, up=1, down = -1, last_x=0, last_t=0):
        ''' Инициализация '''
        self.line_up= line_up
        self.line_down= line_down
        self.up = up
        self.down = down 
        self.last_x = last_x
        self.last_t = last_t
        self.in_hyst = False
        

    def get_response_zapazdivanie(self,t,x):
        ''' получить выход'''
        equa = EquationClass.Equation.get_instance()
        # Определяем было ли уже это время
        if self.in_hyst == False:
            if t > self.last_t or t == self.last_t:
                # Определяем направление
                if self.last_x < x:
                    self.bound = self.line_up
                else:
                    self.bound = self.line_down
                y = functions.sign(t, x, input_bound = self.bound, out_upper= self.up, out_down= self.down)
                self.last_x = x
                self.last_t = t
                if x < self.line_up or x >self.line_down:
                    self.in_hyst= True
            else:
                print('!!!!!')
                y = functions.sign(t, x, input_bound =self.bound, out_upper= self.up, out_down= self.down)
        else:
            y = functions.sign(t, x, input_bound = self.bound, out_upper= self.up, out_down= self.down)
            self.last_x = x
            self.last_t = t
            if x> self.line_up or x<self.line_down:
                self.in_hyst = False
        return y
    
    def get_response_operezenie(self,t,x):
        ''' получить выход'''
        equa = EquationClass.Equation.get_instance()
        # Определяем было ли уже это время
        if self.in_hyst == False:
            if t > self.last_t or t == self.last_t:
                # Определяем направление
                if self.last_x < x:
                    self.bound = self.line_down
                else:
                    self.bound = self.line_up
                y = functions.sign(t, x, input_bound = self.bound, out_upper= self.up, out_down= self.down)
                self.last_x = x
                self.last_t = t
                if x > self.line_up or x <self.line_down:
                    self.in_hyst= True
            else:
                print('!!!!!')
                y = functions.sign(t, x, input_bound =self.bound, out_upper= self.up, out_down= self.down)
        else:
            y = functions.sign(t, x, input_bound = self.bound, out_upper= self.up, out_down= self.down)
            self.last_x = x
            self.last_t = t
            if x< self.line_up or x>self.line_down:
                self.in_hyst = False
        return y

def main():
    #'test'
    import plot
    n=10000 #number of steps
    x=np.linspace(0,4, n)
    y= np.array([])
    cos=np.array([])
    sign = SignHyst(line_up=1, line_down=-1, up=2, down = -2, last_x =-0.01, last_t = -0.01)
    for t in x:
        q= 4*functions.sin(t)
        y=np.append(y,sign.get_response_operezenie(t,q))
        cos = np.append(cos,q)
    
    
    plot.draw_plot(x,y,'t','y','test')
    plot.draw_plot(cos,y,'q','y','test')

if __name__ == '__main__':
    main()