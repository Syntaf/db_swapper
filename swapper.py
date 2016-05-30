############################
# Created on May 4, 2016
#
# @Author: Grant Mercer
############################
import constants
import csv
import tkFileDialog

from Tkconstants import RIGHT, END, DISABLED, BOTH, LEFT, \
    VERTICAL, Y, GROOVE, SUNKEN, SOLID, TOP, W, E, BOTTOM, X, \
    CENTER, S, N, MULTIPLE, EXTENDED
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, IntVar, Text, Listbox, Radiobutton
from log import logger
from PIL import ImageTk

class ui:
    def __init__(self, r):
        self.__root = r         # root of program
        self.__load_icon = ImageTk.PhotoImage(file=constants.PATH + r'/ico/load.png')

        self.__convert_list = []        # holds list of files to be converted
        self.__sub_list = []            # holds list of files to compare against master

        self.__match_rule = IntVar()    # the rule on how to merge files into master

        # public window dimensions
        self.width = self.__root.winfo_screenwidth()
        self.height = self.__root.winfo_screenheight()

        # upper left side of screen
        self.__master_frame = Frame(self.__root, width=constants.WIDTH/3, borderwidth=1, relief=SOLID,
                                    height=constants.HEIGHT/4)
        self.__master_frame.grid_propagate(False)
        self.__master_frame.grid(row=0, column=0, padx=5, pady=5)

        # lower left side of screen
        self.__convert_frame = Frame(self.__root, width=constants.WIDTH/3, borderwidth=1, relief=SOLID,
                                     height=constants.HEIGHT - constants.HEIGHT/4 - 20)
        self.__convert_frame.pack_propagate(False)
        self.__convert_frame.grid(row=1, column=0, padx=5, pady=5)

        # right side of screen
        self.__sub_frame = Frame(self.__root, width=constants.WIDTH - constants.WIDTH/3 - 20, borderwidth=1, relief=SOLID,
                                 height=constants.HEIGHT - 10)
        self.__sub_frame.grid_propagate(False)
        self.__sub_frame.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=2)

    def setup_gui(self):
        """
        Top level function which is called from main(). Sets window title and dimensions, then calls three sub
        routines which created and setup the rest of the GUI
        """
        self.__root.title('db_swapper')
        x = (self.width - constants.WIDTH) / 2
        y = (self.height - constants.HEIGHT) / 2

        self.__root.geometry('%dx%d+%d+%d' % (constants.WIDTH, constants.HEIGHT, x, y))

        self.create_master_frame()
        self.create_convert_frame()
        self.create_sub_frame()

    def create_master_frame(self):
        """
        Initialize the GUI for the upper left
        """
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
        """
        Initialize the GUI for the lower left side of the program
        """
        lbl = Label(self.__convert_frame, text="Files to split")
        lbl.pack(side=TOP)

        self.__convert_lbox = Listbox(self.__convert_frame, width=29, height=12, selectmode=EXTENDED)
        self.__convert_lbox.pack(side=TOP)

        convert = Button(self.__convert_frame, text="Convert", command=self.convert_files)
        remove = Button(self.__convert_frame, text="Remove Item",
                        command=lambda: self.remove_item(self.__convert_lbox, self.__convert_list))
        load = Button(self.__convert_frame, image=self.__load_icon, width=27, height=20,
                      command=lambda: self.import_and_append_file(self.__convert_lbox, self.__convert_list))

        convert.pack(side=LEFT, padx=(10,5), pady=5)
        remove.pack(side=LEFT, padx=(0,5))
        load.pack(side=LEFT)

    def create_sub_frame(self):
        """
        Initialize the GUI for the right side of the program
        """
        self.__sub_lbox = Listbox(self.__sub_frame, width = 30, height = 23, selectmode=EXTENDED)
        self.__sub_lbox.grid(row=0, column=0, rowspan=20, padx=5, pady=5)

        lbl = Label(self.__sub_frame, justify=LEFT,
                    text = "To use db_swapper first load a\nmaster list, the database you wish\nto"
                           " merge files into. Then add\nany sub files to compare against\nand hit"
                           " 'merge'. Use convert to\nsplit a large file into smaller files\nthat "
                           "have a matching first\ncolumn.")
        lbl.grid(row=1, column=1, rowspan=20, columnspan=4, sticky=N+W)

        lbl2 = Label(self.__sub_frame, text="Merge into master if a matched\nsub item is:", justify=LEFT)
        lbl2.grid(row=12, column=1, sticky=W, rowspan=2, columnspan=4)

        Radiobutton(self.__sub_frame, text="Less", variable=self.__match_rule, value=1).\
            grid(row=14, column=1, sticky=W)
        Radiobutton(self.__sub_frame, text="Greater", variable=self.__match_rule, value=2).\
            grid(row=14, column=2, sticky=W)
        Radiobutton(self.__sub_frame, text="Equal", variable=self.__match_rule, value=3).\
            grid(row=14, column=3, sticky=W)

        btn = Button(self.__sub_frame, text="Merge", width=24, command=self.merge_files)
        btn.grid(row=19, column=1, padx=(0,5), columnspan=4, sticky=W)

        open = Button(self.__sub_frame, image=self.__load_icon, width=73, height=35,
                      command=lambda: self.import_and_append_file(self.__sub_lbox, self.__sub_list))
        open.grid(row=18, column=1, padx=(0,0), sticky=W, columnspan=2)

        remove = Button(self.__sub_frame, text="Remove Item", width=10, height=2,
                        command=lambda: self.remove_item(self.__sub_lbox, self.__sub_list))
        remove.grid(row=18, column=2, padx=(40,0), sticky=W, columnspan=2)


    def import_master_file(self):
        """
        Method called with the user chooses to import a master file, opens a dialog for the user to browse and
        select a file, then displays the file chosen within a label and sets the internal variable __master_file
        """
        file_types = [('Semicolon Separated Text Files', ('*.csv', '*.txt')), ('All Files', '*')]
        dlg = tkFileDialog.Open(filetypes=file_types)
        fl = dlg.show()
        if fl != '':
            self.__master_file = fl
            segments = self.__master_file.rpartition('/')
            self.__lbl_file.config(text=segments[2])

    def import_and_append_file(self, lbox, lbox_list):
        """
        Method to prompt a user for a selection of files, and append those files to a list box and internal list.
        Takes a Listbox and list object, and inserts the selected filenames into the Listbox and the full path
        filenames into the list
        """
        file_types = [('Semicolon Separated Files', ('*.csv', '*.txt')), ('All Files', '*')]
        files = list(tkFileDialog.askopenfilenames(filetypes=file_types))
        if files is not None:
            for file in files:
                lbox.insert(END, file.rpartition('/')[2])
                lbox_list.append(file)

    def remove_item(self, lbox, lbox_list):
        """
        Removes any items currently selected in a listbox passed. Also ensures to remove that item from the internal
        list passed.
        """
        indexes = list(lbox.curselection())

        # Remove in reversed order so the indices do not change as we delete
        for idx in reversed(indexes):
            lbox.delete(idx)
            del lbox_list[idx]

    def convert_files(self):
        """
        Splits a large csv file into smaller csv files based upon their first column
        """

        # loop through each file in the Listbox
        for item in self.__convert_list:
            with open(item, 'rb') as file:
                # open the file and create a reader
                master_reader = csv.reader(file, delimiter=constants.DELIMITER)
                curr = None     # keeps track of current running subject
                segment = []    # rows are appended to this list as long as the subject remains the same
                for row in master_reader:
                    # if curr is empty, start a new subject
                    if curr is None: curr = row[0]
                    if curr != row[0]:
                        # sometimes the csv file contains a header sep, if so then ignore it
                        if 'sep=' in curr:
                            curr = None
                            segment=[]
                            continue
                        # create a csv file with the name of the subject
                        with open(constants.PATH + '/' + curr + '.csv', 'wb') as write_out:
                            # write out the delimiter helper, then write the segment list
                            write_out.write('sep='+constants.DELIMITER + '\n')
                            writer = csv.writer(write_out, delimiter=constants.DELIMITER)
                            for seg in segment:
                                writer.writerow(seg)
                        segment = []
                        curr = None
                    else:
                        segment.append(row)
                # if segments has data for a subject at the end of the loop, write the data to the subject
                if list is not None:
                    with open(constants.PATH + '/' + curr + '.csv', 'wb') as write_out:
                        write_out.write('sep='+constants.DELIMITER + '\n')
                        writer = csv.writer(write_out, delimiter=constants.DELIMITER)
                        for seg in segment:
                            writer.writerow(seg)


    def merge_files(self):
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