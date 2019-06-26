import tkinter as tk
import math
from dfa.DFA import DFA

# фигуры
figures={}

# координаты
x=90
y=40
r=20

def VisualizeDFA(automata, word):
    global figures
    # фигуры
    figures = {}
    # новое окно
    window = tk.Tk()
    window.geometry("1280x720")
    canvas = tk.Canvas(window, width=1280, height=720)
    window.iconbitmap('icons/window_icons/python.ico')
    window.title('DFA')

    global x
    global y
    # координаты
    x = 90
    y = 40

    # состояния
    startState=automata.start_state

    # отрисовка начального состояния, т.к. оно одно
    DrawCircle(canvas,50,100,r,"#d8d8d8")
    canvas.create_text(50,100,font=("Comic Sans",15,"bold"),text=startState)    
    figures.update({startState:[50,100]})
    canvas.pack()

    add_offset=True

    # цикл отрисовки допускающих состояний
    for fromState, transitions in automata.transitions.items():
        if add_offset:
            y=40
            add_offset=False
        else:
            y=80
            add_offset=True
        for letter, toState in transitions.items():
            # проверяем, была ли уже нарисована такая фигура
            if toState in figures.keys():
                continue
            # проверяем, является ли состояние конечным и рисуем его
            elif toState in automata.final_states:
                DrawCircle(canvas,x,y,r,"#d8d8d8")  
                DrawNewState(canvas, toState,15)    
                print(toState,x,y)
                canvas.pack()  
                y+=105
                x+=50
            # рисуем состояние
            else:
                DrawNewState(canvas, toState,r)   
                print(toState,x,y) 
                canvas.pack()
                y+=105
                x+=50
        x+=85

    # просто проверка на то, что алфавит весь присутствует
    print(figures.keys())

    # рисуем стрелки
    for fromState, transitions in automata.transitions.items():
        revercedTransitions={}
        for letter, toState in transitions.items():
            if not toState in revercedTransitions.keys():
                revercedTransitions[toState]=[]
            revercedTransitions[toState].append(letter)
        for stateTo, letters in revercedTransitions.items():
            if stateTo==fromState:
                DrawArrowToSelf(canvas, fromState,stateTo,letters)
            else:    
                DrawArrow(canvas, fromState,stateTo,letters)
    s=[]
    s=automata.read_input(word)
    # получение возможной конечной последовательности
    finalSequence=[]
    for i in range(len(s)-1):
        finalSequence.append(s[i][0])
    print(finalSequence)

    # blink-анимация
    for key in finalSequence:
        value=figures[key]
        window.after(350, ChangeColor(canvas, key,value,20,"#FF851B"))
        if key in automata.final_states:
            window.after(250, ChangeColorBack(canvas, key,value,20,"#d8d8d8"))
            window.after(250, ChangeColorBack(canvas, key,value,15,"#7FDBFF"))
        elif key==startState:
            window.after(250, ChangeColorBack(canvas, key,value,20,"#6fabc2"))
        else:
            window.after(250, ChangeColorBack(canvas, key,value,20,"#7FDBFF"))

    if s[-1]==False:
        canvas.create_text(350, 700, font=("Comic Sans", 15, "bold"), text='Данное слово не может распознаться автоматом')
    else:
        canvas.create_text(350, 700, font=("Comic Sans", 15, "bold"), text='Данное слово распознаётся автоматом')
    canvas.pack()
    window.mainloop()

# получаем координаты для правильной отрисовки стрелочек
def GetCoords(fromState, toState):
    x1=fromState[0]
    y1=fromState[1]
    x2=toState[0]
    y2=toState[1]
    vectorLegth=abs(math.sqrt( (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)))
    x3=((x1-x2)/vectorLegth)*20
    y3=((y1-y2)/vectorLegth)*20
    return x3, y3

# функция для удобства построения кругов
def DrawCircle(canvas,x,y,rad,color):
    return canvas.create_oval(x-rad,y-rad,x+rad,y+rad, fill=color,outline="black", width=3)

# функция для отрисовки состояния (круг и надпись)
def DrawNewState(canvas, val,r):
    # добавляем координаты фигуры в лист для проверок в дальнейшем
    figures.update({val:[x,y]})
    return DrawCircle(canvas,x,y,r,"white"), canvas.create_text(x,y,font=("Comic Sans", 15,"bold"),text=val)  

# функция для отрисовки стрелок
def DrawArrow(canvas, key,val,letters):
    fromState=figures[key]
    toState=figures[val]
    print(key,val)
    print(fromState,toState)

    x3, y3 = GetCoords(fromState, toState)
    canvas.create_line(fromState[0]-x3, fromState[1]-y3,toState[0]+x3, toState[1]+y3, width=1,arrow=tk.LAST) 
    x=fromState[0]- (fromState[0]-toState[0])/2
    y=fromState[1]- (fromState[1]-toState[1])/2
    canvas.create_text(x, y,font=("Comic Sans", 12,"bold"),fill='red',text=", ".join(letters))

# рисуем стрелку в само состояние (для состояний со *)
def DrawArrowToSelf(canvas, key,val,letters):
    fromState=figures[key]
    toState=figures[val]
    canvas.create_text((fromState[0])-40,(toState[1])-25,font=("Comic Sans", 12,"bold"),fill='blue',text="*"+', '.join(letters))
    canvas.create_arc(fromState[0]-35, fromState[1]-35,toState[0]-5, toState[1]-5, width=1,extent=270,style=tk.ARC)

    newX=-1*math.sin(math.pi/7)
    newY=-1*math.cos(math.pi/7)
    canvas.create_line( fromState[0]-5+newX, fromState[1]-20+newY,fromState[0]-5, fromState[1]-20, width=1,arrow=tk.LAST) 

# функция для blink-анимирования
def ChangeColor(canvas, key,value,r,color):
    DrawCircle(canvas,value[0],value[1],r,color), canvas.create_text(value[0],value[1],font=("Comic Sans", 15,"bold"),text=key)
    canvas.update()

# функция для blink-анимирования
def ChangeColorBack(canvas, key,value,r,color):
    DrawCircle(canvas,value[0],value[1],r,color), canvas.create_text(value[0],value[1],font=("Comic Sans", 15,"bold"),text=key)
    canvas.update()


# примеры автоматов
# тест проходили на этих автоматах :3 
# http://neerc.ifmo.ru/wiki/index.php?title=Детерминированные_конечные_автоматы
""" automata=DFA(transitions=
    {
        "A": {"a":"B","b":"A"},
        "B": {"b": "C","a":"B"},
        "C": {"a":"B","b":"D"},
        "D": {"a":"E","b":"A"},
        "E": {"b":"F","a":"B"},
        "F": {} # нужно объявлять пустым, если из него нет переходов
    },
    start_state="A",
    final_states=["F"]) """

""" automata=DFA(transitions=
    {
        "1": {"b":"1","a":"2"},
        "2": {"a": "4", "b": "7"},
        "3": {"a": "3","b":"5"},
        "4": {"a": "3", "b": "5"},
        "5": {"a": "8","b":"6"},
        "6": {"a":"2","b":"1"},
        "7": {"a": "8","b":"6"},
        "8": {"a":"4","b":"7"}
    },
    start_state="1",
    final_states=["3","5","6","8"]) """
#############################################################
# вот это основная функция работы
# надо вызывать ее :3
# VisualizeDFA(automata)
#############################################################