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
    #import pygtk
    import gtk
    import sys
    import os
    from spamfilter import Spamfilter
except:
    print "Error: Cannot import modules!"
    sys.exit(1)


# Uvodni funkce pro trenink spamfiltru - vezme slozky a preda je dal
def train(spam, source='emaily'):
    curdir = os.path.dirname(__file__)

    # slozky s dokumenty
    spam_dir = os.path.join(curdir, source, 'spam')
    ham_dir = os.path.join(curdir, source, 'ham')

    # nauceni se spamum
    train_spamfilter(spam, spam_dir, 'spam')

    # nauceni se normalnich dokumentu
    train_spamfilter(spam, ham_dir, 'ham')


# samotna funkce pro trenovani jednotlivych kategorii
def train_spamfilter(spam, path, category):
    for filename in os.listdir(path):
        with open(os.path.join(path, filename)) as fh:
            contents = fh.read()

        # vytazeni slov z obsahu dokumentu
        words = extract_words(contents)

        # nauceni spamfiltru a asociace se skupinama
        spam.train(words, [category])


# extrakce slov z dokumentu
def extract_words(cont, min_len=2, max_len=20):
    # extrakce slov z dokumentu o zadane minimalni a maximalni delce
    # nacteme stop slova ze souboru
    fh = open('stopwords.txt', 'r')
    stopwords = fh.read()

    tmp = []

    # pokud je aktualni slovo ve stop slovech, preskocime jej
    for w in cont.lower().split():
        if w in stopwords:
            continue
        wlen = len(w)
        if wlen > min_len and wlen < max_len:
            tmp.append(w)
    return tmp


# test cele slozky proti naucenym pravidlum
def test(spam, source='emaily2'):
    curdir = os.path.dirname(__file__)

    # slozky se zpravami
    spam_dir = os.path.join(curdir, source, 'spam')
    ham_dir = os.path.join(curdir, source, 'ham')

    correct = total = 0

    for path, category in ((spam_dir, 'spam'), (ham_dir, 'ham')):
        for filename in os.listdir(path):
            with open(os.path.join(path, filename)) as fh:
                contents = fh.read()

            # extrakce slov z dokumentu
            words = extract_words(contents)

            results = spam.filter_spam(words)

            print results

            if results[0][0] == category:
                correct += 1
            total += 1

    pct = 100 * (float(correct) / total)
    print '[%s]: zpracovano %s dokumentu, %0.2f%% uspesnost' % (source, total, pct)


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
        self.label_result_label = gtk.Label("Výsledek: ")
        self.label_result = gtk.Label("0.0 %")

        self.button_learn = gtk.Button("Incializace")
        self.button_test = gtk.Button("Test")

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
        self.table_layout.attach(self.label_learn, 0, 1, 0, 1)
        self.table_layout.attach(self.label_test, 1, 2, 0, 1)
        self.table_layout.attach(self.learn_database_menu, 0, 1, 1, 2)
        self.table_layout.attach(self.test_database_menu, 1, 2, 1, 2)
        self.table_layout.attach(self.button_learn, 0, 1, 2, 3)
        self.table_layout.attach(self.button_test, 1, 2, 2, 3)
        self.table_layout.attach(self.label_result_label, 2, 3, 0, 1)
        self.table_layout.attach(self.label_result, 2, 3, 1, 2)

        # Pridani layoutu do okna a jeho zobrazeni
        self.win.add(self.table_layout)
        self.win.show_all()

if __name__ == '__main__':
    application = Gui()
    gtk.main()
