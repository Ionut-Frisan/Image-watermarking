import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel, Label, LEFT, SOLID
import os
from PIL import Image

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("680x175")
        self.title("Photoshop but better")
        self.initUI()
        self.selectedFiles = ()
        self.watermarkSizeValue = 0.2
        self.marginLeftValue = 20
        self.marginTopValue = 20
        self.marginsmodify = False
        self.resized = False
        self.resizable(0,0)

    def initUI(self):

        #Label containing the run options
        self.LabelOptions = tk.ttk.LabelFrame(self, text="Select files")
        self.buttonSelectFiles = tk.ttk.Button(self.LabelOptions, text="Select files", command= self.DialogSelectFiles)
        self.buttonSelectWatermark = tk.ttk.Button(self.LabelOptions, text="Select Watermark", command = self.DialogSelectWatermark)
        self.buttonRun = tk.ttk.Button(self.LabelOptions, text="Run", command = self.Run)

        self.LabelOptions.grid(row=0, column=0, padx=10, pady=10)
        self.buttonSelectFiles.grid(row=1, column=0, padx=10, pady=10)
        self.buttonSelectWatermark.grid(row=2, column=0, padx=10, pady=10)
        self.buttonRun.grid(row=3, column=0, padx=10, pady=10)

        #Label containing options to modify presets
        self.LabelEdit = tk.ttk.LabelFrame(self,text="Edit preset values")
        self.LabelEdit.columnconfigure(0, weight=3)
        self.marginLeft = tk.ttk.Entry(self.LabelEdit, justify="center", width=30)
        self.marginTop = tk.ttk.Entry(self.LabelEdit, justify="center", width=30)
        self.buttonModifyMargins = tk.ttk.Button(self.LabelEdit, text="Modify margins", command = lambda : self.modifyMargins(self.marginLeft, self.marginTop))
        self.watermarkSize = tk.ttk.Entry(self.LabelEdit, justify="center", width=30)
        self.buttonWatermarkSize = tk.ttk.Button(self.LabelEdit, text="Modify size", command= lambda : self.modifyWatermarkSize(self.watermarkSize))
        self.buttonReset = tk.ttk.Button(self.LabelEdit, text="Reset to presets", command = self.reset)
        self.buttonPreview = tk.ttk.Button(self.LabelEdit, text="Preview", command= self.imagePreview)

        self.marginLeft.insert(0,"Margin left")
        self.marginTop.insert(0,"Margin Top")
        self.watermarkSize.insert(0,"% of original size")

        self.LabelEdit.grid(row=0, column=1, padx=10, pady=10)
        self.marginLeft.grid(row=1, column=0, padx=10, pady=10)
        self.marginTop.grid(row=1, column=1, padx=0, pady=10)
        self.buttonModifyMargins.grid(row=1, column=2, padx=10, pady=10)
        self.watermarkSize.grid(row=2, column=0, padx=10, pady=10)
        self.buttonWatermarkSize.grid(row=2, column=1, padx=10, pady=10)
        self.watermarkSize.columnconfigure(0,weight=2)
        self.buttonReset.grid(row=3, column=1, padx=10, pady=10)
        self.buttonPreview.grid(row=3, column=0, padx=10, pady=10)

        self.marginLeft.bind('<Button-1>', lambda x: self.removeTextFromEntry(self.marginLeft))
        self.marginTop.bind('<Button-1>', lambda x: self.removeTextFromEntry(self.marginTop))
        self.watermarkSize.bind('<Button-1>', lambda x: self.removeTextFromEntry(self.watermarkSize))

    def DialogSelectFiles(self):
        self.selectedFiles = filedialog.askopenfilenames(initialdir = "/",title = "Select images you want to add watermark to",filetypes = [("Image files","*.jpg; *.png")])

    def DialogSelectWatermark(self):
        self.watermark = filedialog.askopenfilename(initialdir = "/",title = "Select Watermark",filetypes = [("Image files","*.jpg; *.png")])

    def Run(self):
        try:
            currentDirectory = os.getcwd()
            if not os.path.exists(f'{currentDirectory}/edited'):
                os.makedirs(f'{currentDirectory}/edited')

            i = 0
            try:
                self.watermark = Image.open(self.watermark).convert("RGBA")
            except:
                pass

            wwidth, wheidth = self.watermark.size
            if self.resized == False:
                self.watermark = self.watermark.resize((int(wwidth*self.watermarkSizeValue), int(wheidth*self.watermarkSizeValue)), Image.ANTIALIAS)
                self.resized = True

            for file in self.selectedFiles :
                image = Image.open(file).convert('RGBA')
                width, height = image.size
                if self.marginsmodify == True:
                    position = (self.marginLeftValue, self.marginTopValue)
                else:
                    if int(height-(height/10)-60) > 0:
                        position = (int(width/10), int(height-(height/10)-60))
                    else :
                        position = (int(width / 10), int(height - (height / 10)))

                newImage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                newImage.paste(image, (0, 0))
                newImage.paste(self.watermark, position, self.watermark)
                if i == 0 or i == 1:
                    newImage.show()
                newImage.save(f'edited/newImage{i}.png', format='PNG')
                i += 1
        except ValueError as ve:
            tk.messagebox.showinfo("!!! Something went wrong !!!", ve)



    def modifyWatermarkSize(self, newSize):
        try:
            nSize = int(newSize.get())
            nSize = float(nSize/100)
            self.watermarkSizeValue = nSize
        except:
            tk.messagebox.showinfo("!!! Something went wrong !!!", "The value should be a pozitive number!")

    def modifyMargins(self, newLeft, newTop):
        try:
            left = int(newLeft.get())
            top = int(newTop.get())
            self.marginLeftValue = left
            self.marginTopValue = top
            self.marginsmodify = True
        except:
            tk.messagebox.showinfo("!!! Something went wrong !!!", "The value should be a pozitive number!")

    def reset(self):
        self.watermarkSizeValue = 1
        self.marginLeftValue = 20
        self.marginTopValue = 20
        self.marginsmodify = False

    def removeTextFromEntry(self,entry):
        string = tk.StringVar()
        string = str(entry.get())
        if string == "Margin left" or string == "Margin Top" or string == "% of original size" :
            entry.delete(0,'end')

    def imagePreview(self):
        try:
            try:
                self.watermark = Image.open(self.watermark).convert("RGBA")
            except:
                pass

            wwidth, wheidth = self.watermark.size
            if self.resized == False:
                self.watermark = self.watermark.resize(
                    (int(wwidth * self.watermarkSizeValue), int(wheidth * self.watermarkSizeValue)), Image.ANTIALIAS)
                self.resized = True

            file = self.selectedFiles[0]
            image = Image.open(file).convert('RGBA')
            width, height = image.size
            if self.marginsmodify == True:
                position = (self.marginLeftValue, self.marginTopValue)
            else:
                if int(height - (height / 10) - 60) > 0:
                    position = (int(width / 10), int(height - (height / 10) - 60))
                else:
                    position = (int(width / 10), int(height - (height / 10)))

            newImage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            newImage.paste(image, (0, 0))
            newImage.paste(self.watermark, position, self.watermark)
            newImage.show()
        except:
            tk.messagebox.showinfo("!!! Something went wrong !!!", "Please select at least one image and the desired watermark")

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() - 120
        y = y + cy + self.widget.winfo_rooty() - 50
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


GUI = GUI()
if __name__ == '__main__':
    try:
        CreateToolTip(GUI.marginLeft,text="Margin left: The position of the watermark to the right \nDefault is set to: (Original photo width)/10")
        CreateToolTip(GUI.marginTop, text="Margin top: The position of the watermark from top to bottom \nDefault is set to:(Original photo height)-((Original photo height)/10)-60")
        CreateToolTip(GUI.watermarkSize, text="Resize the watermark by x % \n Default is set to: 20%")
        GUI.mainloop()
    except ValueError as ve:
        tk.messagebox.showinfo("!!! Something went wrong !!!", ve)
