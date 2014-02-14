#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:13:48 2014

@author: balhar
"""

try:
    import pygtk
    import gtk
    import sys
except:
    print "Error: Cannot import modules!"
    sys.exit(1)


class application():

    def __init__(self, spamfilter):
        # basic configuration
        self.win = gtk.Window()
        self.win.set_title("Bayes SpamFilter")
        self.win.set_border_width(10)
        self.win.connect("destroy", gtk.main_quit)

        # Prvky pro vykresleni

        # Napojeni vytvprenych prvku na funkce

        # layout

        # Prirazeni jednotlivych prvku do table layoutu
        