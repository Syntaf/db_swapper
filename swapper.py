############################
# Created on May 4, 2016
#
# @Author: Grant Mercer
############################
import constants

from Tkconstants import RIGHT, END, DISABLED, BOTH, LEFT, \
    VERTICAL, Y, GROOVE, RIDGE, SOLID
from Tkinter import Tk, Label, Toplevel, Menu, PanedWindow, \
    Frame, Button, StringVar, Text
from log import logger

class ui:
    def __init__(self, r):
        self.__root = r         # root of program

        # public window dimensions
        self.width = self.__root.winfo_screenwidth()
        self.height = self.__root.winfo_screenheight()

        master_frame = Frame(self.__root, width=constants.WIDTH/3,
                             borderwidth=1, relief=SOLID)
        master_frame.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)

        sub_frame = Frame(self.__root, width=constants.WIDTH - constants.WIDTH/3,
                          borderwidth=1, relief=SOLID)
        sub_frame.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)


        """
        self.__master_db_frame = Frame(base_pane, bg="blue")
        self.__master_db_frame.pack(side=LEFT)

        self.__sub_db_frames = Frame(base_pane, bg="green")
        self.__master_db_frame.pack(side=RIGHT)
        """

    def setup_gui(self):
        self.__root.title('db_swapper')
        x = (self.width - constants.WIDTH) / 2
        y = (self.height - constants.HEIGHT) / 2

        self.__root.geometry('%dx%d+%d+%d' % (constants.WIDTH, constants.HEIGHT, x, y))

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