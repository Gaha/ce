#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Permet d'analyser les participations aux activitées

"""

# on utilise sqlite3 pour stocker les évènements
import sqlite3

# pour l'affichage
from tableTexte import Table

class CE(object) :
    """
    Créé un rapport
    """
    def __init__(self) :
        # création de la base de données
        self.bdd = sqlite3.connect('bddCE.sqlite')
        self.cursor = self.bdd.cursor()
        # création des tables
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Agent (nom text primary key, prenom text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Commission (nom text primary key)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Activitee (nom text, idcommission integer, date timestamp DEFAULT current_timestamp)')
        #self.cursor.execute('CREATE TABLE IF NOT EXISTS evenement (id integer primary key, idrapport integer, famille text, genre text, message text)')
        #self.cursor.execute('CREATE TABLE If NOT EXISTS rapport (datecreation timestamp primary key DEFAULT current_timestamp, nom text)')

    def agent_ajout(self, nom, prenom) :
        """
        Ajout un agent à la liste
        """
        self.cursor.execute("INSERT into Agent (nom, prenom) values('" + nom + "','" + prenom + "')")

    def agent_liste(self) :
        """
        Liste les agents
        """
        self.cursor.execute("SELECT * from Agent")
        return self.cursor.fetchall()

    def commission_ajout(self, nom) :
        self.cursor.execute("INSERT into Commission (nom) values ('" + nom + "')")
		
    def commission_liste(self) :
        self.cursor.execute("SELECT * from Commission")
        return self.cursor.fetchall()
	
    def activitee_ajout(self, nom, commission) :
        # on recupère l'ID de la commission
        self.cursor.execute("SELECT rowid from Commission where nom = '" + commission +"'")
        try :
            idcommission = self.cursor.fetchone()[0]
        except TypeError :
            raise TypeError("Commission inconnut")
        self.cursor.execute("INSERT into activitee (nom, idcommission) values ('" + nom + "'," + str(idcommission) + ")")
	
    def activitee_liste(self) :
        self.cursor.execute("SELECT ac.nom, co.nom, ac.date from Activitee ac INNER JOIN Commission co ON ac.idcommission = co.rowid")
        return self.cursor.fetchall()
    
    def activitee_synthese(self) :
        self.cursor.execute("SELECT co.nom, count(ac.idcommission) as Total from Activitee ac inner join Commission co ON ac.idcommission = co.rowid group by co.nom")
        return self.cursor.fetchall()
        
	"""
    def rapport(self, nom) :
        #try :
        self.cursor.execute("INSERT into rapport (nom) values('" + nom + "')")
        #except sqlite3.IntegrityError :
        #    pass
        # on retourne l'id du rapport
        self.cursor.execute("SELECT rowid from rapport where nom ='" + nom + "'")
        return self.cursor.fetchone()[0]

    def rapport_nom(self, id_nom) :
        
        self.cursor.execute("SELECT nom from rapport where rowid='" + str(id_nom) + "'")
        return self.cursor.fetchone()[0]

    def rapport_liste(self) :
        
        self.cursor.execute("SELECT * from rapport")
        return self.cursor.fetchall()

    def rapport_evenement(self, liste = None) :
        
        if liste :
            # on récupère les idrapport de la liste
            rapport = ''
            for lis in liste :
                rapport = rapport + "'" + lis + "',"
            self.cursor.execute("SELECT ev.rowid, rap.nom, ev.famille, ev.genre, ev.message FROM evenement ev INNER JOIN rapport rap ON ev.idrapport = rap.rowid WHERE rap.nom in (" + rapport[:-1] + ")")
        else :
            # intérogation de la base
            self.cursor.execute("SELECT ev.rowid, rap.nom, ev.famille, ev.genre, ev.message FROM evenement ev INNER JOIN rapport rap ON ev.idrapport = rap.rowid")
        return self.cursor.fetchall()

    def rapport_synthese(self, liste = None):
        
        if liste :
            # on récupère les idrapport de la liste
            rapport = ''
            for lis in liste :
                rapport = rapport + "'" + lis + "',"
            self.cursor.execute("SELECT rap.nom, ev.famille, ev.genre, count(ev.genre) as Total from evenement ev inner join rapport rap on ev.idrapport = rap.rowid where rap.nom in (" + rapport[:-1] + ") group by rap.nom, ev.famille, ev.genre")
        else :
            self.cursor.execute("SELECT rap.nom, ev.famille, ev.genre, count(ev.genre) as Total from evenement ev inner join rapport rap on ev.idrapport = rap.rowid group by rap.nom, ev.famille, ev.genre")
        return self.cursor.fetchall()


        # pour chaque famille du rapport on compte le nombre de genre

    def evenement_nouveau(self, idrapport, famille, genre, message = "") :
        self.cursor.execute("INSERT INTO evenement VALUES(null," + str(idrapport) + ",'" + str(famille) + "','" + genre + "','" + message +"')")
	"""
    def __del__(self):
        self.bdd.commit()
        self.cursor.close()

if __name__ == '__main__':
    base = CE()
    base.agent_liste()
    print Table("AGENT", ["Nom","Prénom"], base.agent_liste())
    print

    print Table("COMMISSION", ["Nom"], base.commission_liste())
    print
    
    print Table("ACTIVITEE", ["Nom","Commission","Date"], base.activitee_liste())
    print
    
    print Table("ACTIVITEE SYNTHESE", ["Commission","Nombre"], base.activitee_synthese())
