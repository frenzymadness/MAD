#!/usr/bin/env python

# default dict pro pristup k neinicializovanemu poli
from collections import defaultdict

class Spamfilter(object):
	def __init__(self):
	        # inicializace promennych ve spamfiltru
	        # defaultdict nam umozni priradit hodnotu pri pristupu ke klici bez exceptions
	 
	        self.words = defaultdict(int)
	        self.categories = defaultdict(int)
	        self.word_counts = defaultdict(lambda: defaultdict(int))
	        self.total_count = 0
	
	# funkce pro trenink samotneho filtru
	# v podstate jen zvysujeme pocet vyskytu slova v kategorii a pocet vyskytu samotneho slova
	def train(self, words, categories):
	    # ke kterym kategorii je slovo prirazeno
	    for category in categories:
	        # uprava poctu vyskytu slova v dane kategorii
	        for word in words:
	            self.word_counts[word][category] += 1
	            self.words[word] += 1
	 
	        # zvysime pocet dokumentu zpracovanych do teto kategorie
	        self.categories[category] += 1
	 
	    # a zvysime celkovy pocet zpracovanych dokumentu
	    self.total_count += 1
	
	# vypocteme pravdepodobnost, ze je dane slovo v dane kategorii
	def word_probability(self, word, category):
	    # zjistime pocet vyskytu slova v dane kategorii
	    word_count = self.word_counts[word][category]
	 
	    # pocet zpracovanych dokumentu v dane kategorii
	    category_count = self.categories[category]
	 
		# pokud oboji zname, zjistime pomer vyskytu slova v dane kategorii k poctu kategorii (pravdepodobnost)
	    if word_count and category_count:
	        return float(word_count) / category_count
	    return 0
	
	# vazena je stejna jako predchozi, jen je porovnana s celkovym vyskytem slova
	def weighted_probability(self, word, category, weight=1.0, ap=0.5):
	    # vypocteme pocatecni pravdepodobnost vyskytu slova v kategorii
	    initial_prob = self.word_probability(word, category)
	 
	    # spocteme celkovy vyskyt slova
	    word_total = self.words[word]
	 
	    # vypocteme vazenou pravdepodobnost, ktera nam da lepsi vysledek a odstrani nam nulove hodnoty
	    return float((weight * ap) + (word_total * initial_prob)) / (weight + word_total)
	
	# suma pravdepodobnosti pro vsechny slova v documentu a danou kategorii
	def document_probability(self, words, category):
	    # spocteme pravdepodobnost jak moc se dokument (vsechy slova v nem) hodi do dane kategorie
	    p = 1
	    for word in words:
	        p *= self.weighted_probability(word, category)
	    return p
	
	# celkova pravdepodobnost podle poctu katehorii
	def probability(self, words, category):
	    if not self.total_count:
	        # zabranime deleni nulou
	        return 0
	 
	    # pravdepodobnost vyskytu dane kategorie (ku celkovemu poctu)
	    category_prob = float(self.categories[category]) / self.total_count
	 
	    # pravdepodobnost pro cely predany dokument
	    doc_prob = self.document_probability(words, category)
	 
	    # finalni pravdepodobnost dokumentu podminena pravdepodobnosti cele skupiny
	    return doc_prob * category_prob
	    
	# konecne zjistime s jakou pravdepodobnosti se jedna o spam a s jakou o ham a vratime info v serazenem poli
	def filter_spam(self, words, limit=5):
	    # Vysledne rozhodnuti
	    probs = {}
	    for category in self.categories.keys():
	        probs[category] = self.probability(words, category)
	 
	    # seradime vysledek aby sly ty s nejvetsi pravdepodobnosti jako prvni
	    return sorted(probs.items(), key=lambda (k,v): v, reverse=True)[:limit]

	
