from pdfrw import PdfReader, PdfWriter
import os
import img2pdf
from PIL import Image
from tkinter import *
import tkinter as tk


def focus1(event):
    # set focus on the course_field box
    entry_source.focus_set()


# Function to set focus
def focus2(event):
    # set focus on the sem_field box
    entry_destination.focus_set()



def print_msg(source,destination):

    files = []
# r=root, d=directories, f = files
    for r, d, f in os.walk(source):
        for file in f:
            if '.jpeg' or '.jpg' in file:
                files.append(os.path.join(r, file))

    for f in files:
        image = open(f)
        pdf_bytes=img2pdf.convert(image.name,dpi=280, x=None, y=None,producer="xxx",author="xxx",title="xxxx")
        filename = f.split("\\")[-1].split(".")[0]+".pdf"
        file = open(destination+"\\"+filename, "wb")
        # writing pdf files with chunks
        file.write(pdf_bytes)
        # closing image file
        image.close()
        # closing pdf file
        file.close()
        # output


if __name__ == '__main__':

    window = tk.Tk()
    window.title('Image to PDF')
    frame = tk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")
    window.grid_rowconfigure(0, weight=2)
    window.grid_columnconfigure(0, weight=2)

    lbl_source = Label(frame, text="Source Path:").grid(row=0, column=0, sticky=W)
    lbl_destination = Label(frame, text="Target Path:").grid(row=1, column=0, sticky=W)


    entry_source = Entry(frame)
    entry_source.grid(row=0, column=1,ipadx="80",ipady="4")
    entry_destination = Entry(frame)
    entry_destination.grid(row=1, column=1,ipadx="80",ipady="4")
    btn_submit = Button(frame, text="Apply", width=10, command=lambda: print_msg(entry_source.get(),entry_destination.get())).grid(row=2, column=1)
    entry_source.bind("<Return>", focus1)

    # whenever the enter key is pressed
    # then call the focus2 function
    entry_destination.bind("<Return>", focus2)

    window.geometry('400x200')
    window.mainloop()




