import tkinter as tk
import tkinter.filedialog as fd
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import font as tkFont 

import pandas as pd
import xlsxwriter

from PIL import Image, ImageTk

import numpy as np

import DC_Recipe as recipe
import DC_Vision as vis
import DC_Pyplot as pl

import os
import sys

def file_open():
   file = fd.askopenfilenames(parent=root, title='Open Images', filetypes=[
                    ("image", ".jpeg"),
                    ("image", ".png"),
                    ("image", ".jpg"),
                    ("image", ".bmp"),
                    ])
   file=file[::-1] 
   files.set([])
   for i in range(len(file)):
       listbox.insert(0,os.path.basename(file[i]))
   pathlabel.config(text=os.path.split(file[0])[0])
   

def recipe_open():
    
    file = fd.askopenfilename(parent=root, title='Open Recipe', filetypes=[
                    ("recipe", ".ini"),
                    ])

    recipe.open_ini(file)
    recipe_read()
    recipelabel.config(text=os.path.basename(file))  
    recipe_settings()
    pl.clearplots()
    pl.fig.canvas.draw()  
    
   
def recipe_save():
    f = fd.asksaveasfile(mode='w', defaultextension=".ini", filetypes=[
                    ("recipe", ".ini"),
                    ])
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = "" # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.
 
    recipe.save_ini(f.name)

    recipelabel.config(text=os.path.basename(f.name))     
    if recipelabel.cget("text")[-1]=="*":
        recipelabel.config(text=recipelabel.cget("text")[:-1])


#Get recipe setting declare global containers
tres_white={"size": 0, "tres": 0} 
tres_black={"size": 0, "tres": 0} 
eqlz_hist={"active": 0, "clip": "", "size": 0}
morph_open={"active": 0, "size": 0}
morph_close={"active": 0, "size": 0}
data={"columns": 0, "rows": 0, "dpi": 0}
stats={"lb": 0, "ub": 0}

def recipe_settings():
    
    stats['lb']=recipe.readint("statistics","lower_bound")
    stats['ub']=recipe.readint("statistics","upper_bound")    
    
    tres_black['size']=recipe.readint("black_defects","local_size")
    tres_black['tres']=recipe.readint("black_defects","treshold")
    #print(tres_black)
    
    tres_white['size']=recipe.readint("white_defects","local_size")
    tres_white['tres']=recipe.readint("white_defects","treshold") 
    #print(tres_white)
    
    eqlz_hist['active']=recipe.readint("equalize_histogram","active")
    eqlz_hist['clip']=recipe.readint("equalize_histogram","clip") 
    eqlz_hist['size']=recipe.readint("equalize_histogram","size")    
    #print(eqlz_hist)
    
    morph_open['active']=recipe.readint("morphing_open","active") 
    morph_open['size']=recipe.readint("morphing_open","size") 
 
    morph_close['active']=recipe.readint("morphing_close","active") 
    morph_close['size']=recipe.readint("morphing_close","size") 
 
    data['columns']=recipe.readint("data","columns")
    data['rows']=recipe.readint("data","rows") 
    data['dpi']=recipe.readint("data","dpi")  

      
    
def recipe_read():
    
    #fill tree with recipe
    tree.delete(*tree.get_children())
   
    sec=1
    for each_section in recipe.config.sections():
        ite=1
        tree.insert("", sec,each_section, text=each_section)   
        for (each_key, each_val) in recipe.config.items(each_section):
            tree.insert(each_section, ite, text=each_key,values=each_val)
            ite+=1   
        sec+=1 

def recipe_changed():
  
    #print("changed")
    if recipelabel.cget("text")[-1]!="*":
        recipelabel.config(text=recipelabel.cget("text") + "*")
    
    print("Recipe Changed")


def vision_calc(path, n):

    black_total=0
    black_summary=[]

    white_total=0
    white_summary=[]        
    
    #if len(listbox.curselection())==0:

    #    print("no image selected")   
    #else:
    gray=vis.openimage(path)
    #print(out_tres)
    #recipe_settings()
    pl.clearplots()
    pl.setplots()
    pl.ax1.imshow(gray, cmap='gray') 
    pl.ax1.set_xlabel(str(os.path.basename(path)))
    pl.ax1.set_ylabel("raw image grayscale")

    gray=vis.equal_hist(gray,eqlz_hist['active'],eqlz_hist['clip'],eqlz_hist['size'])

    hist=vis.histogram(gray,stats["lb"],stats["ub"])   
    pl.histogram(hist['ravel'],hist['mean'],hist['stdev'],tres_black['tres'],tres_white['tres'],stats["lb"],stats["ub"])
    
    gray_RGB=vis.gray_RGB(gray)
    
    black_defects=vis.blackdefects(n,coordinate_xy(n)[0],coordinate_xy(n)[1],gray, gray_RGB, tres_black['size'], hist['stdev']*tres_black['tres'],morph_close,morph_open)
    pl.ax2.imshow(black_defects['image'], cmap='gray')  
    
    black_total=black_defects['defects_all']
    black_summary=black_defects['defect_count']
    
    
    gray_RGB=black_defects['image']
    
    white_defects=vis.whitedefects(n,coordinate_xy(n)[0],coordinate_xy(n)[1],gray, gray_RGB, tres_white['size'],hist['stdev']*tres_white['tres'],morph_close,morph_open)
    pl.ax2.imshow(white_defects['image'], cmap='gray')              
    
    white_total=white_defects['defects_all']
    white_summary=white_defects['defect_count']

    pl.ax2.set_ylabel("processed image, treshold")
    pl.ax2.set_xlabel("black defects: " + str(black_summary) + ", white defects: " + str(white_summary))


    
    if n==1:
        pl.fig.canvas.draw()   
        #pl.fig.subplots_adjust(hspace=0.001,wspace=0.1)



    return [n,coordinate_xy(n)[0], coordinate_xy(n)[1], black_summary,white_summary,black_total,white_total]

def vision_batch():
    


    save_path=pathlabel.cget("text") + "/analysis/"
    if not os.path.isdir(save_path):
       os.mkdir(save_path)   
 
    total_defect_summary=[]
    total_white_summary=[]
    total_black_summary=[]
        
    for i, listbox_entry in enumerate(listbox.get(0, tk.END)):    
        listbox.select_clear(0, tk.END)
        listbox.select_set(i)
        listbox.see(i)
        
        path=pathlabel.cget("text") + '/' + listbox_entry        
        #print(path)
        output=vision_calc(path, i+1)
        
        total_defect_summary.append([output[0],output[1],output[2],output[3],output[4]])
        total_black_summary=total_black_summary+output[5]       
        total_white_summary=total_white_summary+output[6]
        
        
        #save image and graphs
        q=str("%04d" % (i+1))
        path=save_path +  str(q)   +   "_analysis.jpg"
        pl.plt.savefig(path, dpi=int(data['dpi']), bbox_inches='tight')
        
        root.update()



    #save data in textfiles 
    path=save_path + '\\Defects_Analysis_Setting.ini'    
    np.savetxt(path, [], delimiter='\t',header="", newline='\n',comments='')  
    recipe.save_ini(path)    
    
    path=save_path + '\\Defects_Analysis_Results.txt'
    np.savetxt(path, total_defect_summary, delimiter='\t',header='n\tx\ty\tcount_black\tcount_white', newline='\n',comments='')  
    
    path=save_path + "\\Defects_All_Count_White.txt"
    df2 = pd.DataFrame (total_white_summary,columns = ['n','x_total','y_total','spot','x_img','y_img','area_white'])  
    np.savetxt(path, total_white_summary, delimiter='\t',header='n\tx_total\ty_total\tspot\tx_img\ty_img\tarea_white', newline='\n',comments='')  

    path=save_path + "\\Defects_All_Count_Black.txt"
    df3 = pd.DataFrame (total_black_summary,columns = ['n','x_total','y_total','spot','x_img','y_img','area_black'])
    np.savetxt(path, total_black_summary, delimiter='\t',header='n\tx_total\ty_total\tspot\tx_img\ty_img\tarea_black', newline='\n',comments='')  

    #Save to excel file    
    path=save_path + '\\Defects_Analysis_Results.xlsx'
    df1 = pd.DataFrame (total_defect_summary,columns = ['n', 'x','y','count_black','count_white'])
    df2 = pd.DataFrame (total_white_summary,columns = ['n','x_total','y_total','spot','x_img','y_img','area_white'])    
    df3 = pd.DataFrame (total_black_summary,columns = ['n','x_total','y_total','spot','x_img','y_img','area_black'])   
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    df1.to_excel(writer, sheet_name='total_defect_summary')
    df2.to_excel(writer, sheet_name='Defects_All_Count_White')
    df3.to_excel(writer, sheet_name='Defects_All_Count_Black')
    
    writer.save()
    writer.close()

xprev=0   
def coordinate_xy(n):
    #Calculate x and y grid while scanning is z-shape
    #note: scan must always start upper left corner  under microscope. 
    i=n-1
    
    x=(i)%data["columns"]
    y=int(np.floor(i/data["columns"]))
   
    if y%2==0:     
        x=(i)%data["columns"]
    else:
        x=(data["columns"]  -1)-(i)%data["columns"]        
        xprev=x
   
    return [x,y]
   
   
# create the root window
#root = tk.Tk()

root_main = tk.Tk()
root_main.withdraw()

#root = tk.Toplevel(rootTk)
#root.protocol("WM_DELETE_WINDOW", root.destroy)



root = tk.Toplevel()
root.geometry('1280x720')
root.minsize(1280, 720)

#root.resizable(False, False)
root.title('DEFECTdet')  
#root.withdraw()

#photo = tk.PhotoImage(file = 'Settings/ICON.ico')
#root_main.iconphoto(False, photo)


root.iconbitmap(default='Settings/ICON.ico')



root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=20)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=20)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)


root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=10)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=50)
root.rowconfigure(4, weight=1)

files = tk.StringVar()

#File Listbox
def OnEntryUpDown(event):
    selection = event.widget.curselection()[0]
    
    if event.keysym == 'Up':
        selection += -1

    if event.keysym == 'Down':
        selection += 1

    if 0 <= selection < event.widget.size():
        event.widget.selection_clear(0, tk.END)
        event.widget.select_set(selection)
        
    items_selected(event)
    recipe_settings()
    
pathlabel = tk.Label(root, text="",width=40, anchor=tk.W)
pathlabel.config(font=('helvetica', 12))
pathlabel.grid(
    column=1,
    row=0,
    columnspan = 1, rowspan =1,
    sticky=tk.S+tk.W)

listbox = tk.Listbox(
    root,
    listvariable=files,
    selectmode=tk.SINGLE,
    exportselection=0,
    height=10,
    width=10,
)

listbox.config(font=('helvetica', 12)) 
listbox.grid(
    column=1,
    row=1,
    columnspan = 1, rowspan =1,
    sticky=tk.N+tk.S+tk.E+tk.W
)

listbox.bind("<Down>", OnEntryUpDown)
listbox.bind("<Up>", OnEntryUpDown)

# link a scrollbar to a list
scrollbar = ttk.Scrollbar(
    root,
    orient='vertical',
    command=listbox.yview,
)

scrollbar.grid(
    column=2,
    row=1,
    columnspan = 1, rowspan = 1,
    sticky=tk.N+tk.S+tk.W
)

def items_selected(event):
    #get path from listbox
    if len(listbox.curselection())==0:

        print("no image selected")       
    else:
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        path=pathlabel.cget("text") + '/' + value
        #print(path)
    
        vision_calc(path,1)
        #recipe_settings()

listbox.bind('<<ListboxSelect>>', items_selected)    
listbox['yscrollcommand'] = scrollbar.set
    
#View Recipe in tree view
recipelabel = tk.Label(root, text="Recipe",width=40, anchor=tk.W)
recipelabel.config(font=('helvetica', 12))
recipelabel.grid(
     column=3,
     row=0,
     columnspan = 1, rowspan =1,
     sticky=tk.S+tk.W)
     

style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('helvetica', 12)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('helvetica', 12)) # Modify the font of the headings

tree = ttk.Treeview(root,style="mystyle.Treeview", selectmode='browse')
tree["columns"]=("one")
tree.column("one", width=100 )
tree.heading("#0",text="Root",anchor=tk.W)
tree.heading("one", text="Value",anchor=tk.W)

tree.grid(
     column=3,
     row=1,
     columnspan = 1, rowspan =1,
     sticky=tk.N+tk.S+tk.E+tk.W,
)


def recipe_click(event):
    
    item = tree.selection()[0]
    parent =tree.parent(item)
    
    parent_text=tree.item(parent)['text']
    item_text=tree.item(item)['text']
    value_text=tree.item(item)['values']    

    if parent:
        if item_text=='comment':
            showinfo(title='comment: ' + str(parent_text), message=value_text, parent=root)
            #tk.tkMessageBox.showinfo(title='comment: ' + str(parent_text), message=value_text, parent=tree)
            
            
        else:
            #print(tree.item(parent)['text'])
            #print(tree.item(item)['text'])
            
            value = tk.simpledialog.askinteger(str(parent_text), str(item_text),
                             parent=tree, initialvalue=value_text, 
                             minvalue=0, maxvalue=1000)   
            if value is not None:
                tree.item(item, values=value)
                #print(parent)
                #print(item)
                recipe.set(parent_text,item_text,value)
     
                #recipe_read()
                recipe_changed()
                recipe_settings()
    
                #refresh results
                if not len(listbox.curselection())==0:
                    selection = listbox.curselection()
                    index = selection[0]
                    value = listbox.get(index)
                    path=pathlabel.cget("text") + '/' + value    
                    vision_calc(path, 1)
       
tree.bind("<Double-1>", recipe_click)

# link a scrollbar to a list
scrolltree = ttk.Scrollbar(
    root,
    orient='vertical',
    command=tree.yview,
)


scrolltree.grid(
    column=4,
    row=1,
    columnspan = 1, rowspan = 1,
    sticky=tk.N+tk.S+tk.W
)

tree['yscrollcommand'] = scrolltree.set


#open default recipe
recipe.open_ini('recipes/Default.ini')
recipe_read()
recipe_settings()
recipelabel.config(text="Default.ini")   




img = Image.open('settings/ICON.png')
#img = img.resize((int(650*0.25), int(900*0.25)), Image.ANTIALIAS)
img = img.resize((int(650*0.25), int(900*0.25)))
photo = ImageTk.PhotoImage(img)

label = tk.Label(root,image=photo)
label.image = photo
label.grid(column=4, row=1,    padx=(20,0), sticky=tk.W+tk.N+tk.E)


# Add a Button Select Files
selectfiles = tk.Button(root, text="Select Files", command=file_open,font=('helvetica', 12))
selectfiles.grid(
    column=1,
    row=2,
    columnspan = 1, rowspan =1,
    padx=0, pady=5,
    sticky=tk.N+tk.E)


# Add a Button Select Files
startbatch = tk.Button(root, text="Start Batch", command=vision_batch,font=('helvetica', 12))
startbatch.grid(
    column=4,
    row=2,
    columnspan = 1, rowspan =1,
    padx=0, pady=5,
    sticky=tk.N+tk.E)

 # Add a Button Save Recipe
saverecipe = tk.Button(root, text="Save Recipe", command=recipe_save,font=('helvetica', 12))
saverecipe.grid(
    column=3,
    row=2,
    columnspan = 1, rowspan =1,
    padx=0, pady=5,
    sticky=tk.N+tk.E)  

 # Add a Button Save Recipe
openrecipe = tk.Button(root, text="Open Recipe", command=recipe_open,font=('helvetica', 12))
openrecipe.grid(
    column=3,
    row=2,
    columnspan = 1, rowspan =1,
    padx=125, pady=5,
    sticky=tk.N+tk.E)  

#root.bind('<Return>', recalc_vision)

#Pyplot
# specify the window as master
canvas = pl.FigureCanvas(pl.fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=3, column=1, columnspan = 4, rowspan =1,    padx=0, pady=0,sticky=tk.S +tk.N+tk.W+tk.E)



# navigation toolbar
toolbarFrame = tk.Frame(master=root)
toolbarFrame.grid(row=4, column=1, columnspan = 4, rowspan =1,  padx=0, pady=5, sticky=tk.N+tk.W )
toolbar = pl.NavigationToolbar(canvas, toolbarFrame)

def on_closing():
    root.destroy()
    sys.exit()
    raise SystemExit    

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()