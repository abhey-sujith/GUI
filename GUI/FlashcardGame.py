
from decorator import decorator
#standard library for modifying the behaviour of functions 

from tkinter import *
#standard Python interface to the Tk GUI toolkit
import tkinter.font as font
import pandas as pd
#software library for data access
import sys
#provides functions and variables used to manipulate different parts of the Python Runtime Environment


@decorator
def begin(fun,*args, **kwargs):
    #args*  is used to pass a variable number of arguments to a function
    if kwargs !={}:
        #kwargs** is used to pass a keyworded, variable-length argument list
        try:
            if kwargs['Start']:
                if 'Verbose' in kwargs['Settings']:
                    if kwargs['Settings']['Verbose']:
                        print(fun)
                        pass
                response= fun(*args,**kwargs)
                return response
            else:
                kwargs['Start'] = False
                print(fun,"DID NOT START")
                return(kwargs)
        except Exception as e:
            global ekwargs
            global efun
            ekwargs = kwargs
            efun = fun
            print('HALTING')
            raise
    else:
        print('Empty')
        return ()



def start():
    return {'Start':True,'Settings':{'Verbose':True},'Status':{},'Data':[],'Threads':[]}

 
@begin
def datafromexcel(*args,**kwargs):
    
    dt = pd.read_excel('FlashCard_GUI.xlsx')
    #data is accessed from the excel file containing flash card information
    kwargs['Data'] = dt
    
    return kwargs
      
 
@begin
def showFlashCard(*args,**kwargs):        
    
    global thisCard, returnCardBtn, removeCardBtn
    
    def flipCard():
        
        global thisCard, removeCardBtn, returnCardBtn
        
        lab.configure(text=thisCard.Back.values[0], fg='red', font=100,width=15, pady=12, wraplength=400, justify=CENTER)
        myFont = font.Font(family='Helvetica')
        lab['font'] = myFont
        myFont = font.Font(size=25)
        lab['font'] = myFont
        #creating a label for answer
        flipb.grid_forget()
        returnCardBtn = Button(window, text="Return flashcard", bg='red', command=returnCard) #creating a button for return flashcard
        returnCardBtn.grid(column=0, row=1)
        removeCardBtn = Button(window, text="Remove flashcard", bg='red', command=removeCard) #creating a button for remove flashcard
        removeCardBtn.grid(column=1, row=1)
        
    def returnCard():
        
        global thisCard
        #selects a random sample from the dataframe
        thisCard = dt.sample() 
        lab.configure(text=thisCard.Front.values[0], fg='blue')
        returnCardBtn.grid_forget()
        removeCardBtn.grid_forget()
        flipb.grid(column=0, row=1, columnspan=2)
        
    def removeCard():
        global thisCard, returnCardBtn, removeCardBtn
        
        if dt.any(axis=None):
            
            dt.drop(thisCard.index, inplace=True)
            
            if not dt.empty:
                #selects a random sample from the dataframe
                thisCard = dt.sample()  
                lab.configure(text=thisCard.Front.values[0], fg='blue')

                returnCardBtn.grid_forget()
                removeCardBtn.grid_forget()
                flipb.grid(column=0, row=1, columnspan=2)
            
            else:
                lab.configure(text="Complete!", fg='white')
            
            
    dt = kwargs['Data']
    #selects a random sample from the dataframe
    thisCard = dt.sample()
    #creation of tkinter object
    window = Tk()
    window.title('Flash card application using GUI')
    #specifying the title
    window.geometry('300x200')
    #specifying the window sixe
    window.configure(bg='black')
    #specifying the window background
    #creating a label for flashcard
    lab = Label(window, text=thisCard.Front.values[0], bg='black', fg='blue', width=10, pady=12, wraplength=400, justify=CENTER)
    myFont = font.Font(family='Helvetica')
    lab['font'] = myFont
    myFont = font.Font(size=40)
    lab['font'] = myFont
    lab.grid(column=0, row=0, columnspan=2)
    #specifying the label location
    #creating a button for flipcard
    flipb = Button(window, text="Flip the card", bg='blue', command=flipCard)   #specifying the button location        
    flipb.grid(column=0, row=1, columnspan=2)
    window.mainloop()
    
    
    return kwargs
      
 
@begin
def stop(*args,**kwargs):
    print('exiting')
    sys.exit()
 
 


class Node:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=stop(**showFlashCard(**datafromexcel(**kwargs)))
        return (self.kwargs)

class flash:
    def __init__(self):
        self.status="pending"
    def run(self,expname):
        self.response=stop(**showFlashCard(**datafromexcel(**start())))
        self.status="completed"
        return(self.status)

if __name__ == '__main__':
    process = flash()
    process.run('Local')
   
    
