############################
# Created on May 4, 2016
#
# @Author: Grant Mercer
############################
import constants
import tkFileDialog

from Tkconstants import RIGHT, END, DISABLED, BOTH, LEFT, \
    VERTICAL, Y, GROOVE, SUNKEN, SOLID, TOP, W, E, BOTTOM, X, \
    CENTER, S, N
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, IntVar, Text, Listbox, Radiobutton
from log import logger
from PIL import ImageTk

class ui:
    def __init__(self, r):
        self.__root = r         # root of program
        self.__load_icon = ImageTk.PhotoImage(file=constants.PATH + r'/ico/load.png')

        self.__convert_list = []
        self.__sub_list = []

        self.__match_rule = IntVar()

        # public window dimensions
        self.width = self.__root.winfo_screenwidth()
        self.height = self.__root.winfo_screenheight()

        self.__master_frame = Frame(self.__root, width=constants.WIDTH/3, borderwidth=1, relief=SOLID,
                                    height=constants.HEIGHT/4)
        self.__master_frame.grid_propagate(False)
        self.__master_frame.grid(row=0, column=0, padx=5, pady=5)


        self.__convert_frame = Frame(self.__root, width=constants.WIDTH/3, borderwidth=1, relief=SOLID,
                                     height=constants.HEIGHT - constants.HEIGHT/4 - 20)
        self.__convert_frame.pack_propagate(False)
        self.__convert_frame.grid(row=1, column=0, padx=5, pady=5)

        self.__sub_frame = Frame(self.__root, width=constants.WIDTH - constants.WIDTH/3 - 20, borderwidth=1, relief=SOLID,
                                 height=constants.HEIGHT - 10)
        self.__sub_frame.grid_propagate(False)
        self.__sub_frame.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=2)

    def setup_gui(self):
        self.__root.title('db_swapper')
        x = (self.width - constants.WIDTH) / 2
        y = (self.height - constants.HEIGHT) / 2

        self.__root.geometry('%dx%d+%d+%d' % (constants.WIDTH, constants.HEIGHT, x, y))

        self.create_master_frame()
        self.create_convert_frame()
        self.create_sub_frame()

    def create_master_frame(self):
        load_btn = Button(self.__master_frame, image=self.__load_icon, width=20, height=20,
                          command=self.import_master_file)
        load_btn.grid(row=1, column=1, padx=5, pady=5)

        lbl_master = Label(self.__master_frame, text="Master List")
        lbl_master.grid(row=1, column=2, padx=5, pady=5)

        self.__lbl_file = Label(self.__master_frame, bg="white", relief=SUNKEN, width=26)
        self.__lbl_file.grid(row=2, column=1, padx=5, pady=5, columnspan=3)

        self.__master_frame.grid_rowconfigure(0, weight=1)
        self.__master_frame.grid_columnconfigure(3, weight=1)
        self.__master_frame.grid_rowconfigure(3, weight=1)
        self.__master_frame.grid_columnconfigure(0, weight=1)

    def create_convert_frame(self):
        lbl = Label(self.__convert_frame, text="Files to convert")
        lbl.pack(side=TOP)

        self.__convert_lbox = Listbox(self.__convert_frame, width = 29, height = 12)
        self.__convert_lbox.pack(side=TOP)

        convert = Button(self.__convert_frame, text="Convert", command=self.convert_files)
        remove = Button(self.__convert_frame, text="Remove Item")
        load = Button(self.__convert_frame, image=self.__load_icon, width=27, height=20,
                      command=lambda: self.import_append_file(self.__convert_lbox))

        convert.pack(side=LEFT, padx=(10,5), pady=5)
        remove.pack(side=LEFT, padx=(0,5))
        load.pack(side=LEFT)

    def create_sub_frame(self):
        self.__sub_lbox = Listbox(self.__sub_frame, width = 30, height = 23)
        self.__sub_lbox.grid(row=0, column=0, rowspan=20, padx=5, pady=5)

        lbl = Label(self.__sub_frame, justify=LEFT,
                    text = "To use db_swapper first load a\nmaster list, the database you wish\nto"
                           " merge files into. Then add\nany sub files to compare against\nand hit"
                           " 'merge'. Use convert to\nchange space, tab, or comma\ndelimited"
                           " files into semicolon\ndelimited.")
        lbl.grid(row=1, column=1, rowspan=20, columnspan=4, sticky=N+W)

        lbl2 = Label(self.__sub_frame, text="Merge into master if a matched\nsub item is:", justify=LEFT)
        lbl2.grid(row=12, column=1, sticky=W, rowspan=2, columnspan=4)

        Radiobutton(self.__sub_frame, text="Less", variable=self.__match_rule, value=1).\
            grid(row=14, column=1, sticky=W)
        Radiobutton(self.__sub_frame, text="Greater", variable=self.__match_rule, value=2).\
            grid(row=14, column=2, sticky=W)
        Radiobutton(self.__sub_frame, text="Equal", variable=self.__match_rule, value=3).\
            grid(row=14, column=3, sticky=W)

        btn = Button(self.__sub_frame, text="Merge", width=24)
        btn.grid(row=19, column=1, padx=(0,5), columnspan=4, sticky=W)

        open = Button(self.__sub_frame, image=self.__load_icon, width=73, height=35)
        open.grid(row=18, column=1, padx=(0,0), sticky=W, columnspan=2)

        remove = Button(self.__sub_frame, text="Remove Item", width=10, height=2)
        remove.grid(row=18, column=2, padx=(40,0), sticky=W, columnspan=2)


    def import_master_file(self):
        file_types = [('Semicolon Separated Text Files', '*.txt'), ('All Files', '*')]
        dlg = tkFileDialog.Open(filetypes=file_types)
        fl = dlg.show()
        if fl != '':
            self.__master_file = fl
            segments = self.__master_file.rpartition('/')
            self.__lbl_file.config(text=segments[2])

    def import_append_file(self, lbox):
        pass

    def convert_files(self):
        pass




def main():
    logger.info('db_swapper v0.1 changelog')
    rt = Tk()
    program = ui(rt)

    # setup ui window
    program.setup_gui()
    rt.mainloop()
    logger.info('Terminated program')

if __name__ == '__main__':
    main()