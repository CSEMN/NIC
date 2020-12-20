import math
from tkinter import Label,LabelFrame,Entry,Button,Tk,END,CENTER,Frame,messagebox,Spinbox
from PIL import ImageTk, Image
from Equation import Expression


#create a table for input -> by "create table" button
def createInputTable():
    
    #remove any previous results
    for child in outputTableFrame.winfo_children():
        child.destroy() 
    outputTableFrame.pack_forget()
    diffTableContainer.clear()
    
    #check if there were previous tables and remove it 
    if len(inputTableValues)>0:
        for i in inputTableValues :
            i[0].grid_remove()
            i[1].grid_remove()
        inputTableValues.clear()
    inputTableFrame.pack_forget()
    if len(calcFrameElements)>0 :
        for i in calcFrameElements:
            calcFrameElements[i].grid_forget()
    calcFrameElements.clear()
    
    # create new input table
    xLable = Label(inputTableFrame,text="x",font=("Arial",10,"bold"))
    xLable.grid(row=0,column=0)
    yLable = Label(inputTableFrame,text="f (x)",font=("Arial",10,"bold"))
    yLable.grid(row=1,column=0)
    
    for i in range(int(inputcountEnrty.get())):
        xEntry = Entry(inputTableFrame,width=8,justify=CENTER, validate = 'focusout', validatecommand = numValidate)
        xEntry.grid(row=0,column=i+1,padx=1,pady=1)
        yEntry = Entry(inputTableFrame,width=8,justify=CENTER, validate = 'focusout', validatecommand = numValidate)
        yEntry.grid(row=1,column=i+1,padx=1,pady=1)
        inputTableValues.append([xEntry,yEntry])
    
    
    calcFrame = Frame(inputTableFrame)
    calcFrameElements["lable"] = Label(calcFrame,text="Find f (",font=("Arial",10,"bold"))
    calcFrameElements["lable"].grid(row=0,column=0)
    calcFrameElements["entry"] = Entry(calcFrame,justify=CENTER,width=5,font=("Arial",10,"bold"), validate = 'focusout', validatecommand = numValidate)
    calcFrameElements["entry"].grid(row=0,column=1)
    calcFrameElements["lable2"]= Label(calcFrame,text=")",font=("Arial",10,"bold"))
    calcFrameElements["lable2"].grid(row=0,column=2)
    calcFrameElements["button"] = Button(calcFrame,text="Calc !",command=createOutputTable,font=("Arial",10,"bold"))
    calcFrameElements["button"].grid(row=0,column=3,padx=10)
    
    colspn=len(inputTableValues)+1
    calcFrame.grid(row=2,pady=10,columnspan=colspn)

    
    inputTableFrame.pack(ipadx=5)
  

def createOutputTable():
    
    #remove any previous results
    for child in outputTableFrame.winfo_children():
        child.destroy() 
    outputTableFrame.pack_forget()
    diffTableContainer.clear()
    
    #validate if any empty entries 

    for i in inputTableValues :
        if (i[0].get() == "" or i[1].get()==""):
            messagebox.showerror("Empty !","please, fill all input values !")
            return
    if (calcFrameElements["entry"].get()==""): 
        messagebox.showerror("Empty !","please, fill f(x) value !")
        return
    
    xValues = []
    for x in inputTableValues :
        xValues.append(float(x[0].get()))
    
    xVal = float(calcFrameElements["entry"].get()) # value of X to abtain f(x) for...
    x0 = float(inputTableValues[0][0].get()) #first value of X
    xn = float(inputTableValues[len(inputTableValues)-1][0].get()) #last value of X
    Xc = float(inputTableValues[int(len(inputTableValues)/2)][0].get()) # value of centerd X
    Xbc = float(inputTableValues[int(len(inputTableValues)/2)-1][0].get()) # value bafore centerd X
    Xac = float(inputTableValues[int(len(inputTableValues)/2)+1][0].get()) # value after centerd X
    
    if xVal in xValues : # if found in input table
        diffTableContainer["method"] = Label(outputTableFrame,text="Found in input table !",font=("Arial",10))
        result = float(inputTableValues[xValues.index(xVal)][1].get())
        diffTableContainer["result"] = Label(outputTableFrame,text=(f"f ({xVal}) = {result}"),font=("Arial",12,"bold"))
        colSpan=len(differenceTableValues)+2
        diffTableContainer["method"].grid(column=0,row=1,columnspan=colSpan)
        diffTableContainer["result"].grid(column=0,row=2,columnspan=colSpan)
        outputTableFrame.pack() 
        return
    elif (len(xValues)%2 != 0 and (( (xVal < Xc) and (xVal > Xbc) ) or ( (xVal > Xc) and (xVal <Xac) ) ) ): # if xVal near center of table 
        diffTableContainer["method"] = Label(outputTableFrame,text="Using Sterling centeral difference formula",font=("Arial",10))
        #use sterling
        calcDivTable()
        tableType="div."
        result = calcSterling()
    elif ( abs( x0- xVal ) < abs( xn - xVal) ) :
        calcDiffTable()
        result = calcNewtonForward()
        diffTableContainer["method"] = Label(outputTableFrame,text="Using Newton forward difference formula",font=("Arial",10))
        tableType="diff."
    elif ( abs( x0- xVal ) > abs( xn - xVal) ):
        calcDiffTable()
        result = calcNewtonBackward()
        diffTableContainer["method"] = Label(outputTableFrame,text="Using Newton backward difference formula",font=("Arial",10))
        tableType="diff."
    else :
        diffTableContainer["method"] = Label(outputTableFrame,text="Odd input count needed for central diffrence",font=("Arial",10))
        result="Unknown !"
        diffTableContainer["result"] = Label(outputTableFrame,text=(f"f ({xVal}) = {result}"),font=("Arial",12,"bold"))
        colSpan=len(differenceTableValues)+2
        diffTableContainer["method"].grid(column=0,row=1,columnspan=colSpan)
        diffTableContainer["result"].grid(column=0,row=2,columnspan=colSpan)
        outputTableFrame.pack()
        return 
    
    for i in range(len(differenceTableValues)+2) : # +2 for x and y columns
        #create X and Y columns
        if i < 2 :
            if i == 0 :
                diffTableContainer[f"col{i}"] = LabelFrame(outputTableFrame, text="X",font=("Arial",10,"bold"))
            elif i==1 :
                diffTableContainer[f"col{i}"] = LabelFrame(outputTableFrame, text="f(x)",font=("Arial",10,"bold"))
            inputValues=[]
            for k in inputTableValues :
                inputValues.append(k[i].get())
                for j in range(0,len(inputValues)) :
                    diffTableContainer[f"col{i}-row{j}"]= Label(diffTableContainer[f"col{i}"],text= inputValues[j],font=("Arial",10))
                    diffTableContainer[f"col{i}-row{j}"].grid(column=i,row=j)
        else:
            diffTableContainer[f"col{i}"] = LabelFrame(outputTableFrame, text=f"{ordinal[i-1]} {tableType}",font=("Arial",10,"bold"))
            tmp=0
            for l in differenceTableValues[i-2] :
                diffTableContainer[f"col{i}-row{j}"]= Label(diffTableContainer[f"col{i}"],text=l,font=("Arial",10))
                diffTableContainer[f"col{i}-row{j}"].grid(column=i,row=tmp)
                tmp+=1
                
            
        diffTableContainer[f"col{i}"].grid(row=0,column=i)
    outputTableFrame.pack()
    

    diffTableContainer["result"] = Label(outputTableFrame,text=(f"f ({xVal}) = {result}"),font=("Arial",12,"bold"))
    colSpan=len(differenceTableValues)+2
    diffTableContainer["method"].grid(column=0,row=1,columnspan=colSpan)
    diffTableContainer["result"].grid(column=0,row=2,columnspan=colSpan)       

            
        
#create and calculate the difference table       
def calcDiffTable():
    
    differenceTableValues.clear()
    
    #obtains y values from the input table
    yValues=[]
    for i in inputTableValues :
        yValues.append(float(i[1].get()))
    
    #calculate delta y values 
    deltaYValues=[]
    for j in range(len(yValues)-1) :
        deltaYValues.append(yValues[j+1]-yValues[j]) 
         
    differenceTableValues.append(deltaYValues)     
    
    for i in range(len(yValues)-2) :
        deltaYValues=[]   
        for k in range(len(differenceTableValues[i])-1) :
            deltaYValues.append(differenceTableValues[i][k+1] - differenceTableValues[i][k])
        
        differenceTableValues.append(deltaYValues)

#calculate the divided table 
def calcDivTable():
    
    differenceTableValues.clear()
    
    #obtains y values from the input table
    yValues=[]
    for i in inputTableValues :
        yValues.append(float(i[1].get()))
    
    x0 = float(inputTableValues[0][0].get())
    x1 = float(inputTableValues[1][0].get())
    h  = x1-x0 
    
    #calculate divided y values 
    divYValues=[]
    for j in range(len(yValues)-1) :
        divYValues.append((yValues[j+1]-yValues[j])/h)  
      
    differenceTableValues.append(divYValues)     
    
    for i in range(len(yValues)-2) :
        divYValues=[]   
        for k in range(len(differenceTableValues[i])-1) :
            divYValues.append( (differenceTableValues[i][k+1] - differenceTableValues[i][k]) / ( (i+2)*h ) )
        
        differenceTableValues.append(divYValues)
    
#to return s(s-1)(s-2)....
def factOfS(rep) :
    if rep==0 :
        return "S"
    elif rep > 0 : 
        return (f"(S-{rep})"+" * "+factOfS(rep-1))           
                
def calcNewtonForward():
     
    xVal=float(calcFrameElements["entry"].get()) # desired value to obtain f(x) at
    x0 = float(inputTableValues[0][0].get())
    x1 = float(inputTableValues[1][0].get())
    h  = x1-x0
    sVal = (xVal-x0) / h
    f_x0 = float(inputTableValues[0][1].get())
    p_x  = f_x0
    times= len(differenceTableValues) 
    for i in range(times) :
        deltaY  = float(differenceTableValues[i][0])
        factOfSVal = Expression(factOfS(i))(sVal) 
        p_x += ((factOfSVal / math.factorial(i+1) ) * deltaY)
    return p_x
            
def calcNewtonBackward():
    
    xVal=float(calcFrameElements["entry"].get()) # desired value to obtain f(x) at
    x0 = float(inputTableValues[0][0].get())
    x1 = float(inputTableValues[1][0].get())
    xn = float(inputTableValues[len(inputTableValues)-1][0].get())
    h  = x1-x0
    sVal = (xVal-xn) / h
    f_xn = float(inputTableValues[len(inputTableValues)-1][1].get())
    p_x  = f_xn
    times= len(differenceTableValues)
    for i in range(times) :
        deltaY  = float(differenceTableValues[i][(len(differenceTableValues[i])-1)])
        factOfSVal = Expression(factOfS(i).replace("-","+"))(sVal)  #replace s(s-1)(s-2)... by s(s+1)(s+2)...
        p_x += ((factOfSVal / math.factorial(i+1) ) * deltaY)
    return p_x

def specialFactS(rep): # S(S^2 - 1^2)(s^2 - 2^2)...
    
    if rep==0 :
        return "S"
    elif rep > 0 : 
        return (f"(S^(2)-{rep}^(2))"+" * "+specialFactS(rep-1))  
    
def calcSterling():
    
    xVal=float(calcFrameElements["entry"].get()) # desired value to obtain f(x) at
    x0 = float(inputTableValues[0][0].get()) 
    x1 = float(inputTableValues[1][0].get())
    centerIndex = int(len(inputTableValues)/2) 
    xc = float(inputTableValues[centerIndex][0].get()) # x value at center of table
    h  = x1-x0
    sVal = (xVal-xc)/h
    f_xc = float(inputTableValues[centerIndex][1].get()) # f(x) at center of the table 
    p_x = f_xc
    evenSItiration = 0
    oddSItiration = 0
    times= len(differenceTableValues)
    for i in range(times) :
        current_H = h**(i+1)
        
        if (i%2 == 0) :
            divY_1  = float(differenceTableValues[i][((int(len(differenceTableValues[i])/2) - 1))])
            divY_2  = float(differenceTableValues[i][((int(len(differenceTableValues[i])/2) ))])
            current_div = (divY_1 + divY_2) / 2
            termOfSval = Expression(specialFactS(evenSItiration))(sVal)
            evenSItiration += 1
            
        else :
            current_div  = float(differenceTableValues[i][(int(len(differenceTableValues[i])/2))])
            termOfSval = Expression(specialFactS(oddSItiration) + " * S")(sVal)
            oddSItiration += 1
        
        finalValue = current_H * current_div * termOfSval
        p_x += finalValue
    return p_x


def validate(action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                messagebox.showerror("Invalid input","please, Enter only numbers")
                return False
        else:
            return False
   
main_window = Tk()
main_window.title("Newton interpolation calculator")
main_window.minsize(600,600)
main_window.iconbitmap(".\\images\\NIC.ico")

numValidate = (main_window.register(validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W') #number validation
bigLable = Label(main_window,text="Newton interpolation calculator",fg="Blue",font=('Arial',18,"bold"),anchor="center",pady=20)
bigLable.pack()

#Configuration frame
#contains input count and creat input table
configFrame= LabelFrame(main_window, text="Configuration",font=("Arial",12))
inputcountLable = Label(configFrame,text="input count",font=("Arial",10))
inputcountLable.grid(row=0,column=0,padx=5)
inputcountEnrty = Spinbox(configFrame,from_= 2, to = 10,width=3,justify=CENTER, validate = 'focusout', validatecommand = numValidate)
inputcountEnrty.delete(0)
inputcountEnrty.insert(END,"4")
inputcountEnrty.grid(row=0,column=1,padx=5)
inputcountButton = Button(configFrame,text="create table !",command=createInputTable,font=('Arial',10,"bold")) 
inputcountButton.grid(row=0,column=2,padx=5)
configFrame.pack()
#End of configuration frame

#input table frame
#contains values of X and f(x) entered by user
inputTableFrame= LabelFrame(main_window, text="Input table",font=("Arial",12))
inputTableValues= []
calcFrameElements={}

#output table frame
#contains values of X and f(x) and delta(n) of x columns
outputTableFrame= LabelFrame(main_window, text="Solution",font=("Arial",12))
differenceTableValues= []
diffTableContainer={}

ordinal=("0th","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th") #tuple of ordinal numbers

#copyright section
copyrightFrame = LabelFrame(main_window,text="Copyright",labelanchor='n',font=("Arial",12))
img = ImageTk.PhotoImage(Image.open(".\\images\\logo.png").resize((200,70)))
Label(copyrightFrame,image=img).pack()
Label(copyrightFrame,font=("Arial",12),text="Coded by : Mahmoud Nasser").pack()
Label(copyrightFrame,font=("Arial",12),text="Supervisor : Dr\\ Hany Ahmed El-Gohary").pack()

copyrightFrame.pack(fill="x",side="bottom")
#Main loop
main_window.mainloop()
