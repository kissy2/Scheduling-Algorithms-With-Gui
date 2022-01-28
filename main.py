import tkinter as tk
import os
import itertools
from copy import deepcopy

class colors:
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'
    BrightRed= '\u001b[31;1m'
    BrightGreen= '\u001b[32;1m'
    BrightYellow= '\u001b[33;1m'
    BrightBlue= '\u001b[34;1m'
    BrightMagenta= '\u001b[35;1m'
    BrightCyan= '\u001b[36;1m'
    BrightWhite= '\u001b[37;1m'
    reset='\033[0m'    
    bold='\033[01m'
    underline='\033[4m'
    reverse='\033[07m'


# def tri_selection(tab,s,inp):
    # for i in range(inp):
       # mini = i
       # for j in range(i+1, inp):
           # if tab[mini][s] > tab[j][s]:
    #            mini = j
    #    tmp = tab[i]
    #    tab[i] = tab[mini]
    #    tab[mini] = tmp
    # return tab

def mergeSort(tab,s,inp):
    if inp>1:
        mid = inp//2
        lefthalf = tab[:mid]
        righthalf = tab[mid:]
        mergeSort(lefthalf,s,len(lefthalf))
        mergeSort(righthalf,s,len(righthalf))
        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][s] <= righthalf[j][s]:
                tab[k]=lefthalf[i]
                i=i+1
            else:
                tab[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            tab[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            tab[k]=righthalf[j]
            j=j+1
            k=k+1
    return tab

def custom_scheduler(tab):
    ol = []
    to_add = tab[0]["dispo"]
    while len(tab) > 0:
        mini = tab[0]["fin"]-tab[0]["dispo"]-tab[0]["duree"]
        obj = tab[0]
        for j in tab:
            if j["dispo"] <= max(to_add,obj["dispo"]):
                val = j["fin"]-j["dispo"]-j["duree"]
                if mini > val:
                    mini = val 
                    obj = j
                elif mini == val and obj["dispo"] == j["dispo"]:
                    if obj["duree"] > j["duree"]:
                        obj = j
                    mini = val
            else:
                break
        tab.remove(obj)
        obj["debut"] = to_add
        to_add += obj["duree"]
        ol.append(obj)      
    return ol

def fcfs(tab):
    current = tab[0]["dispo"]   
    for i in tab:
        i["debut"] = current
        current += i["duree"]
    return tab

def sjf(tab):
    def get_sj(tab,index):
        mini = tab[0]
        for i in tab:    
            if i["dispo"] <= index:
                if i["duree"] < mini["duree"]:
                    mini = i
            else:
                break
        return mini
    index=tab[0]["dispo"]
    temp=[]
    while len(tab) > 0 :
        k = get_sj(tab,index)
        k["debut"] = index
        temp.append(k)
        index += k["duree"]
        tab.remove(k)
    return temp

def get_dispo(tab,date):
    temp = [tab[0],]
    for i in tab[1:]:
        if i["dispo"] <= date:
            temp.append(i)
        else:
            break
    return temp

def round_robin(tab,quantum):
    index = tab[0]["dispo"]
    temp = get_dispo(tab,index)
    ol=[]
    while len(tab) > 0:
        for i in temp:
            sub = min(quantum,i["duree"])
            ol.append({"indice":i["indice"],"duree": sub,"dispo": i["dispo"], "fin":i["fin"] ,"debut": index})
            i["duree"] -= sub
            index += sub
            i["dispo"] = index
            if i["duree"] < 1 :
                tab.remove(i)
        if tab:
            index = max(index,tab[0]["dispo"])
            temp = get_dispo(tab,index)
            temp = mergeSort(temp,"dispo",len(temp))
    return ol


def round_robin_gui():
    window = tk.Toplevel(root)
    window.title("Choose Quantum")
    window.geometry("550x100+550+300")
    window.focus_force()
    ent=makeform(window,('Enter Quantum Size :',),18)[0]
    b1 = hv(window, text='Exceute',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda f=round_robin,w=window,e=ent:scheduler(f,w,e)))
    b1.pack(side=tk.BOTTOM, padx=5, pady=5)
    ent.focus()
    window.mainloop()


def brute_force(tab):
    best = -1 
    for x in itertools.permutations(tab):
        retard = 0
        x=list(x)
        x[0]["debut"] = x[0]["dispo"]
        count = x[0]["dispo"] + x[0]["duree"]
        for k in x[1:]:
            if k["dispo"] > count:
                break
            k["debut"] = count
            count += k["duree"]
            if count > k["fin"]:
                retard +=  count - k["fin"]
        else:
            if retard < best or best == -1 :
                best = retard
                temp = deepcopy(x)
    return temp

    
def graph(data,r):
    window = tk.Toplevel(root)
    window.title("Commands Graph")
    c_width = len(data)*80+10
    c_height = 170
    c = tk.Canvas(window, width=c_width, height=c_height, bg='white')
    c.pack()
    x_stretch = 20
    x_width = 60
    count=0
    for x,y in enumerate(data):
        x0 = x * x_stretch + x * x_width + 15
        x1 = x * x_stretch + x * x_width + x_width + 15
        s=max(count,y['dispo'])
        color='salmon' if y['fin']<y['debut']+y['duree'] else "lightgreen"
        c.create_rectangle(x0, 50, x1,110, fill=color,activefill="sky blue")
        c.create_text(x0 + 30, 80,text=y['indice'] if len(y['indice'])<6 else y['indice'][:4]+"...",fill="white",font=("Helvetica", "13"))
        c.create_text(x0 , 118, text=str(s))
        count=s+y['duree']
        c.create_text(x1, 118,  text=str(count))
    c.create_text(c_width/2, c_height-10, anchor=tk.S, text="Retard Total : "+str(r),font=("Helvetica", "10")) 
    window.mainloop()


def add(entries):
    text = ""
    flag = True
    first = True
    focus = False
    for entry in entries:
        val=entry.get().replace(" ","")
        if val.isdigit() or (first and val != "" ) :
            text  = text + "," + val
            entry.configure(background="white",fg="black")
            first=False
        else:
            if not focus :
                focus = entry   
            entry.configure(background="tomato2",fg="white")
            flag = False
    if flag:
        with open(".\commands.txt","a+") as f:
            f.write(text[1:]+"\n")
        for e in entries:
            e.delete(0,'end')
        entries[0].focus()
    else:
        focus.focus()


def makeform(root, fields,wd=15):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=wd, text=field, anchor='w',font=("Times", "16","bold"))
        ent = tk.Entry(row,font=("Times", "16"))
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append(ent)
    return entries

def show():
    try:
        with open(".\commands.txt","r") as f :
            os.system("cls")
            data = f.readline()
            while data:
                i=data.replace("\n","").split(',')
                data= f.readline()
                print((colors.BrightYellow+'Command Name : '+colors.BrightWhite+'{}\n'+colors.BrightYellow+'Date : '+colors.BrightWhite+'{}\n'+colors.BrightYellow+'Required Time : '+colors.BrightWhite+'{}\n'+colors.BrightYellow+'Deadline : '+colors.BrightWhite+'{}\n'+colors.reset).format(i[0],i[1],i[2],i[3]))
    except:
        print("commands.txt has invalid commands !")

def get(w,x):
    x = x.get()
    if x :
        with open(".\commands.txt","r") as f :
            data=f.readline()
            nf=""
            while data:
                if x != data[0:data.find(',')].strip():
                    nf=nf+data
                data=f.readline()
        with open(".\commands.txt","w") as f :
            f.write(nf)
        w.destroy()

def remove():
    window = tk.Toplevel(root)
    window.title("Remove Gui")
    window.geometry("550x100+550+300")
    window.focus_force()
    ent=makeform(window,('Enter Command Name :',),18)[0]
    b1 = hv(window, text='Delete',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda e=ent:get(window,e)))
    b1.pack(side=tk.BOTTOM, padx=5, pady=5)
    ent.focus()
    window.mainloop()
   
def scheduler(fn,w=None,e=None):
    os.system("cls")
    tab=[]
    inp=0
    with open(".\commands.txt", "r") as f:
        data=f.readline()
        while data:
            inp+=1    
            command = data.replace("\n","").split(",")
            tab.append({"indice": command[0],
                        "duree": int(command[2]),
                        "dispo": int(command[1]),
                        "fin": int(command[3]),
                        "debut": None})
            data=f.readline()
    if tab:
        retard = 0
        if w:
            quantum = e.get().replace(" ","")
            if quantum.isdigit():
                quantum=int(quantum)
                data = fn(mergeSort(tab,"dispo",inp),quantum)
                w.destroy()
            else:
                e.focus()
                e.configure(background="tomato2",fg="white")
                return
        elif fn is brute_force:
            data = fn(tab)
        else:
            data = fn(mergeSort(tab,"dispo",inp))
        for t in data:
            ret=t["debut"] + t["duree"] > t["fin"]
            print((colors.BrightYellow+"La commande : "+colors.BrightCyan+"{}\n"+colors.BrightYellow+"Disponible à : "+colors.BrightCyan+"{}\n"+colors.BrightYellow+"Commence à : "+colors.BrightCyan+"{}\n"+colors.BrightYellow+"Dure  : "+colors.BrightCyan+"{}\n"+colors.BrightYellow+"Date limite  : "+colors.BrightCyan+"{}\n"+colors.BrightYellow+"--> En retard : "+(colors.BrightRed if ret else colors.BrightGreen)+"{}\n"+colors.reset).format(t["indice"],t["dispo"],t["debut"],t["duree"],t["fin"],ret))
            if ret:
                retard += t["debut"] + t["duree"] - t["fin"]
        print((colors.pink if ret else colors.BrightGreen)+"Retard Total : ", retard,colors.reset)
        graph(data,retard)
    else:
        print(colors.BrightYellow+"No commands found"+colors.reset)


class hv(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self.config('text')[-1] in ("Quit","Delete"):
            self['background'] = "crimson"
        else:
            self['background'] = "tomato"
        self['foreground'] = "white"

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self["foreground"] = "black"

if '__main__' == __name__:
    fields = 'Command Name : ', 'Date : ', 'Required Time : ', 'Deadline : '
    root = tk.Tk()
    root.title("Gui")
    root.geometry("1300x220+130+300")
    ents = makeform(root, fields)
    b1 = hv(root, text='Add Command',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda e=ents:add(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = hv(root, text='Show All Commands',font=("Helvetica", "16"),activebackground='lightgreen',command=show)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = hv(root, text='Remove Command',font=("Helvetica", "16"),activebackground='lightgreen',command=remove)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    b4 = hv(root, text='Custom Scheduler',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda e=custom_scheduler:scheduler(e)))
    b4.pack(side=tk.LEFT, padx=5, pady=5)
    b5 = hv(root, text='Brute Force',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda e=brute_force:scheduler(e)))
    b5.pack(side=tk.LEFT, padx=5, pady=5)
    b6 = hv(root, text='FCFS',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda e=fcfs:scheduler(e)))
    b6.pack(side=tk.LEFT, padx=5, pady=5)
    b7 = hv(root, text='SJF',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda e=sjf:scheduler(e)))
    b7.pack(side=tk.LEFT, padx=5, pady=5)
    b8 = hv(root, text='Round Robin',font=("Helvetica", "16"),activebackground='lightgreen',command=(lambda:round_robin_gui()))
    b8.pack(side=tk.LEFT, padx=5, pady=5)
    b9 = hv(root, text='Quit',font=("Helvetica", "16"), command=root.destroy)
    b9.pack(side=tk.RIGHT, padx=5, pady=5)
    root.mainloop()