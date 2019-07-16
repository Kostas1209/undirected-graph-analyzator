
#Undirected graph analyzer 
#
#     BUTTON
#press middle button to make new Top
#press left button to move the Top
#press right button on the top to choosse Tops to make the side or write number of begin top, end Top and weight of side
#
#     InputBox
#press left button on Input Rect or press right button to active the window to write in the number of top 
#
#     MinWay
#press on mode Минимальная цепь and write in just opened input Box begin and end Top
#
#   
#  



# здесь подключаются модули
import os
import pygame
import math

pygame.init()

class Top:
    radius = 5
    color = (255,0,0)

    def __init__(self,x,y,wi,st):
        self.name = st
        self.coordX=x
        self.coordY=y
        self.window = wi
        self.rect = pygame.Rect(self.coordX-3,self.coordY-3,10,10)

    def drawCircle(self):
        pygame.draw.circle(self.window , self.color , (self.coordX,self.coordY) ,self.radius )

    def getCoord(self):
        return self.coordX,self.coordY

class Text:

     def __init__(self,coord,word,wi,si):
         self.sentence = word # текст обьекта
         self.coordinate = list(coord) # координаты обьекта
         self.window = wi #экран обьекта
         self.size = si
         self.font = pygame.font.SysFont('Arial',self.size ) # шрифт текста
         self.text = self.font.render(self.sentence, 0 , (0,0,0) ) #создание готового текста обьекта  

     def drawTopText(self):  #Отрисовка обьекта
         self.window.blit(self.text,(self.coordinate[0]-20,self.coordinate[1]-20))
     
     def drawText(self):  #Отрисовка обьекта
         self.window.blit(self.text,(self.coordinate[0],self.coordinate[1]))

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
    def handle_event(self, event,matrix):
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 3:
                self.active = True
            else:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    ChangeMatrix(self.text,matrix)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        self.txt_surface = FONT.render(self.text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class InputForShortestWay(InputBox):
     def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.pressEnter = False
        self.MinWayLenght =0 
        self.MinWay = 0

     def handle_event(self, event,Amount,matrix):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.setShortestWay(self.text,Amount,matrix)
                    self.pressEnter = True
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color) 

     def setShortestWay(self,text,AmountOfTop,matrixOfSide):
         try:
            words = text.split()
            self.MinWayLenght , self.MinWay = FordBelman(int(words[0]),int(words[1]),AmountOfTop,matrixOfSide)
         except:
            ErrorText = "Начальная или конечная вершины указаны неверно"

class RadioButton:
    color = (0,0,0)
    font = pygame.font.SysFont ('Arial',20)
    interval = 30
    masText = list()
    masState = [False,False]
    masRect = list()

    def __init__(self, posx, posy):
        self.BeginCoord = (posx,posy)
        rect = pygame.Rect(self.BeginCoord[0]-5,self.BeginCoord[1]-5,10,10)
        self.masRect.append(rect)
        rect = pygame.Rect(self.BeginCoord[0]-5,self.BeginCoord[1]-5 + self.interval, 10 , 10)
        self.masRect.append(rect)

    def setText(self,text1,text2):
        a = self.font.render(text1,True,self.color)
        self.masText.append(a)

        a = self.font.render(text2,True,self.color)
        self.masText.append(a)
     

    def draw (self, window):
        pygame.draw.circle(window, self.color, (self.BeginCoord[0],self.BeginCoord[1]) ,10 ,1)
        if self.masState[0] == True:
            pygame.draw.circle(window, (0,139,139), (self.BeginCoord[0]+1,self.BeginCoord[1]) ,5)
        window.blit(self.masText[0],(self.BeginCoord[0]+30,self.BeginCoord[1]-12))

        pygame.draw.circle(window, self.color, (self.BeginCoord[0],self.BeginCoord[1] + self.interval) ,10 ,1)
        if self.masState[1] == True:
            pygame.draw.circle(window, (0,139,139), (self.BeginCoord[0]+1,self.BeginCoord[1]+self.interval),5)
        window.blit(self.masText[1],(self.BeginCoord[0]+30,self.interval+self.BeginCoord[1]-12))

    def handle_event(self,event):
        for i in range(2):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.masRect[i].collidepoint(event.pos): 
                    if self.masState[i]==False:
                       self.masState[0]=False
                       self.masState[1]=False
                       self.masState[i]=True

                    elif self.masState[i]==True:
                       self.masState[i]=False


COLOR_INACTIVE = (33,33,33)

ErrorText = ''
COLOR_ACTIVE = (0,139,139)
FONT = pygame.font.SysFont('Arial', 32)
FPS = 20
Pi = math.pi
R = 250


def ToFindShortestWay(text,mainWindow,matrixOfSide,AmountOfTop):
    print(MinWayLenght[int(words[1])])
    print(MinWay)

def ChangeMatrix(text,matrix):
    try:
       words = text.split()
       if words[0]!=words[1]:
          matrix[ int(words[0]) ][ int(words[1]) ] = int(words[2])
          matrix[ int(words[1]) ][ int(words[0]) ] = int(words[2])
    except:
       ErrorText = 'Данные были введены неправильно ,повторите ввод'

def setTops(n,window): # создание списка вершин 
    arr = list()
    for i in range(n):
        x=300 + R * math.cos(2*Pi*i/n)
        y=300 + R * math.sin(2*Pi*i/n)
        Ob = Top(int(x),int(y),window,"X"+str(i) )
        arr.append(Ob)
    return arr

def setTextToTop(n,window,arr):
     masText = list()
     for i in range(n):
         ob = Text(arr[i].getCoord(),arr[i].name, window,20)
         masText.append(ob)
     
     return masText

def search_min(tr, vizited):
   try:
      min=100000000
      for ind in vizited:
         for index, elem in enumerate(tr[ind]):
             if elem > 0 and elem<min and index not in vizited:
                min=elem#веса путей
                index2=index  # индекс конечной вершины
                index1 = ind  # индекс начальной вершины 
      return [index1, index2]
   except:
      ErrorText="Граф не связный"

def prim(matr):
    try:
       toVisit=[i for i in range(1,len(matr))]#вершины кроме начальной
       vizited=[0]
       result=list() #Список ветвей дерева
       for index in toVisit:
          ind=search_min(matr, vizited)
          vizited.append(ind[1])# посещённые вершины
          result.append(ind)
       return result
    except:
       pass

def FordBelman(begin,finish,n,matrix): # Ford-Belman
    index =[math.inf]*n
    index[begin]=0
    way=list()
    for count in range(n-1):
        for i in range( n ):
            if index[i] != math.inf:
                for j in range(n):
                    if matrix[i][j]>0 and index[i]+matrix[i][j]<index[j]:
                        index[j]=matrix[i][j]+index[i]
    i=finish
    way.append(i)
    while i!=begin:
        for j in range(n):
            if matrix[i][j]!=0 and index[i]-matrix[i][j] == index[j]:
                i=j
                way.append(j)
                break
    way.reverse()
    return index[finish],way



def main():
    ''' здесь происходит инициация, создание объектов и др. '''
    font = pygame.font.SysFont('Arial', 30)

    switch = RadioButton(850 , 300) # Переключатель между режимами 
    switch.setText("Цепь наименьшей длины","Економическое дерево")

    rightPanel = pygame.Surface( (400,600) )  #  Панель иструментов и функций справа
    rightPanel.fill( (255,255,255) ) # Заливка панели справа\

    AmountOfTop = 0 # Количетво вершин
    
    mainWindow = pygame.display.set_mode((1200 ,600))  # главное окно
    
    clock = pygame.time.Clock() # Тики процесора для регулировки количества кадров в сек
    
    InputBoxForShortestWay = InputForShortestWay(850,400,300,50)

    masTop = setTops(AmountOfTop,mainWindow)   # список из вершин графа
    TopName = setTextToTop(AmountOfTop,mainWindow,masTop)   # список из названий вершин
    Box = InputBox(850,150,200,50) # Поле ввода
    TextInput1 = Text((820,60),"Введите в поле номера",mainWindow , 28)
    TextInput2 = Text((820,100),"инцидентных вершин и вес ребра",mainWindow , 28)
    TextShortestWay = Text( (830,360), "Введите начало и конец цепи:",mainWindow, 30)

    matrixOfSide = [ [0 for y in range(AmountOfTop)] for x in range(AmountOfTop)]
    ''' если надо до цикла отобразить объекты на экране '''

    check = False #Отрисован ли кратчайший путь

    oldpos=list(pygame.mouse.get_pos())
    changeTop=-1

    # главный цикл
    while True:
       # задержка
       clock.tick(FPS)

       # цикл обработки событий
       for i in pygame.event.get():
           if i.type == pygame.QUIT:#Если нажат крестик или альт + ф4
               for i in range(AmountOfTop):
                   for j in range (AmountOfTop):
                       print(matrixOfSide[i][j],sep=' ',end=' ')
                   print()
               return 
           elif i.type == pygame.MOUSEBUTTONDOWN:   #Выделять вершины мышкой
               if i.button == 3:
                  pos = pygame.mouse.get_pos()
                  for j in range(AmountOfTop):
                     if masTop[j].rect.collidepoint(pos):
                        Box.text+=(str(j)+' ')
                        break

               if i.button == 2:
                  pos = pygame.mouse.get_pos()
                  t = Top(pos[0], pos[1] , mainWindow, 'X'+str(len(masTop)) )
                  ob = Text(t.getCoord(),t.name, mainWindow,20)
                  masTop.append(t)
                  TopName.append(ob)
                  for j in range (AmountOfTop):
                      matrixOfSide[j].append(0)
                  AmountOfTop+=1
                  arr=[0 for j in range(AmountOfTop)]
                  matrixOfSide.append(arr)

           InputBoxForShortestWay.handle_event(i,AmountOfTop,matrixOfSide)
           Box.handle_event(i,matrixOfSide) # Расматривает случаи ввода текста в поле ввода (событие,matrix)
           switch.handle_event(i)
        
       if Box.active == True:
           InputBoxForShortestWay.MinWay = 0
           InputBoxForShortestWay.active = False
           InputBoxForShortestWay.pressEnter == False
           switch.masState[0]=False
           switch.masState[1]=False

       # обновление экрана
       mainWindow.fill( (100,100,100) )  # фон приложения

       mainWindow.blit( rightPanel,(800,0) ) # Панель рядом

       switch.draw(mainWindow) # отображение RadioButton
       
       pressed = pygame.mouse.get_pressed()   #движение мышью вершины графа
       if pressed[0]==True:
           if changeTop==-1:
              pos = pygame.mouse.get_pos()
              for i in range(AmountOfTop):
                  if masTop[i].rect.collidepoint(pos):
                      changeTop=i
                      oldpos = [masTop[i].coordX,masTop[i].coordY]
                      break
           else:
               pos = pygame.mouse.get_pos()
               delposx=pos[0]-oldpos[0]
               delposy=pos[1]-oldpos[1]
               oldpos[0]=pos[0]
               oldpos[1]=pos[1]
               masTop[changeTop].rect.move_ip(delposx,delposy)
               masTop[changeTop].coordX+=delposx
               masTop[changeTop].coordY+=delposy
               TopName[changeTop].coordinate[0]+=delposx
               TopName[changeTop].coordinate[1]+=delposy
       else:
           changeTop=-1


       if switch.masState[1]==True: # Если нужно отобразить економичекое дерево
           try:
              InputBoxForShortestWay.active = False
              InputBoxForShortestWay.pressEnter == False
              InputBoxForShortestWay.MinWay = 0
              EconTreeWay = prim(matrixOfSide)
              for  i in EconTreeWay:
                 x1 = masTop[ i[0] ].getCoord()
                 x2 = masTop[ i[1] ].getCoord()
                 pygame.draw.aaline(mainWindow , (100,255,10) , x1 , x2)
                 text = font.render( str(matrixOfSide[ i[0] ][ i[1] ] ) , True , (0,0,0) )
                 mainWindow.blit(text, ( ((x1[0]+x2[0])//2) , ((x1[1]+x2[1])//2) ))
           except:
               switch.masState[1]=False

       elif switch.masState[0]==True: # Если нужно найти минимальный путь от вершины Begin To Finish
            Box.active = False
            InputBoxForShortestWay.active = True
            for i in range(AmountOfTop):  # Обработка марицы и рисование рёбер
               for j in range(i,AmountOfTop):
                   if matrixOfSide[i][j]!=0:
                      x1 = masTop[i].getCoord()
                      x2 = masTop[j].getCoord()
                      pygame.draw.aaline(mainWindow , (255,255,255) , x1 , x2)
                      text = font.render( str(matrixOfSide[i][j]) , True , (0,0,0) )
                      mainWindow.blit(text, ( ((x1[0]+x2[0])//2) , ((x1[1]+x2[1])//2) ))
            if InputBoxForShortestWay.pressEnter == True and InputBoxForShortestWay.MinWay!=0:#Отрисовывать Мин путь только после того ,как нажат был Ентер при вводе значений
                TextLenghtShortestWay = Text( (830,450) , "Длина кратчайшей цепи: " + str(InputBoxForShortestWay.MinWayLenght) 
                                             ,mainWindow,30 )
                TextLenghtShortestWay.drawText()
                for i in range(len(InputBoxForShortestWay.MinWay)-1):
                    x1 = masTop[InputBoxForShortestWay.MinWay[i]].getCoord()
                    x2 = masTop[InputBoxForShortestWay.MinWay[i+1]].getCoord()
                    pygame.draw.aaline(mainWindow , (100,255,10) , x1 , x2)
                    text = font.render( str(matrixOfSide[InputBoxForShortestWay.MinWay[i]][InputBoxForShortestWay.MinWay[i+1]]) , True , (0,0,0) )
                    mainWindow.blit(text, ( ((x1[0]+x2[0])//2) , ((x1[1]+x2[1])//2) ))
                    i = InputBoxForShortestWay.MinWay[i]
       
       else:
           InputBoxForShortestWay.MinWay = 0
           InputBoxForShortestWay.active = False
           InputBoxForShortestWay.pressEnter == False
           for i in range(AmountOfTop):  # Обработка марицы и рисование рёбер
              for j in range(i,AmountOfTop):
                  try:
                     if matrixOfSide[i][j]!=0:
                         x1 = masTop[i].getCoord()
                         x2 = masTop[j].getCoord()
                         pygame.draw.aaline(mainWindow , (255,255,255) , x1 , x2)
                         text = font.render( str(matrixOfSide[i][j]) , True , (0,0,0) )
                         mainWindow.blit(text, ( ((x1[0]+x2[0])//2) , ((x1[1]+x2[1])//2) ))
                  except:
                      pass
       
       for i in range(AmountOfTop): # Обнрвление вешин
           masTop[i].drawCircle()
           TopName[i].drawTopText()

       functions = Text( (950,0) ,"Функции" ,mainWindow, 40) # Слово функции 
       functions.drawText()

       TextInput1.drawText() # Надпись над инпутом
       TextInput2.drawText()
       Box.update()  # Обновление поля ввода
       Box.draw(mainWindow)

       if InputBoxForShortestWay.active == True: # Если нужно показать минимальный путь ,то отрисовываем окно ввода
           TextShortestWay.drawText()
           InputBoxForShortestWay.draw(mainWindow)
       f= pygame.font.SysFont('Arial',20)
       t=f.render( ErrorText,1,(0,0,0) )
       mainWindow.blit( t,(810,460) )

       pygame.display.update()

main()