#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:13:48 2014

@author: balhar
"""

"""
TODO:
- Dodelat dalsi tlacitko pro novy start spamfiltru
    rozliseni mezi novym startem a uceni dalsi db
- Napojit tlacitka na funkce
- Do funkci dopsat gtk handlery pro disable prvku
    jako je stopwords po inicializaci filtru
- Prepis classy spamfiltru pro samostatne fungovani
- Import samostatne classy smapfiltru a jeji predani gtk jako parametr
- Pridat k funkcnim tlacitek funkce spamfiltru
- testovani funkcnosti
- Moznost testovani samostatneho souboru pomoci viceradkoveho inputu
"""

try:
    import pygtk
    import gtk
    import sys
except:
    print "Error: Cannot import modules!"
    sys.exit(1)


class Gui():

    def __init__(self, spamfilter=None):
        # basic configuration
        self.win = gtk.Window()
        self.win.set_title("Bayes SpamFilter")
        self.win.set_border_width(10)
        self.win.connect("destroy", gtk.main_quit)

        # Prvky pro vykresleni
        self.label_learn = gtk.Label("Naučit spamfiltr pravidla")
        self.label_test = gtk.Label("Otestovat spamfiltr")
        self.label_conf = gtk.Label("Konfigurace")
        self.label_result_label = gtk.Label("Výsledek: ")
        self.label_result = gtk.Label("0.0 %")

        self.button_learn = gtk.Button("Incializace")
        self.button_test = gtk.Button("Test")

        self.check_useStopWords = gtk.CheckButton("Použít stop slova")

        self.learn_database_menu = gtk.combo_box_new_text()
        self.test_database_menu = gtk.combo_box_new_text()
        for database in ['db1', 'db2', 'db3']:
            self.learn_database_menu.append_text(database)
            self.test_database_menu.append_text(database)
        self.learn_database_menu.set_active(0)
        self.test_database_menu.set_active(0)
        # Napojeni vytvprenych prvku na funkce

        # layout
        self.table_layout = gtk.Table(4, 3, False)
        self.table_layout.set_row_spacings(20)
        self.table_layout.set_col_spacings(20)

        # Prirazeni jednotlivych prvku do table layoutu
        self.table_layout.attach(self.label_conf, 0, 1, 0, 1)
        self.table_layout.attach(self.label_learn, 1, 2, 0, 1)
        self.table_layout.attach(self.label_test, 2, 3, 0, 1)
        self.table_layout.attach(self.learn_database_menu, 1, 2, 1, 2)
        self.table_layout.attach(self.test_database_menu, 2, 3, 1, 2)
        self.table_layout.attach(self.button_learn, 1, 2, 2, 3)
        self.table_layout.attach(self.button_test, 2, 3, 2, 3)
        self.table_layout.attach(self.check_useStopWords, 0, 1, 1, 2)
        self.table_layout.attach(self.label_result_label, 3, 4, 0, 1)
        self.table_layout.attach(self.label_result, 3, 4, 1, 2)

        # Pridani layoutu do okna a jeho zobrazeni
        self.win.add(self.table_layout)
        self.win.show_all()

if __name__ == '__main__':
    application = Gui()
    gtk.main()
