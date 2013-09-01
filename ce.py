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
        """
        Ajout un commission
        """
        self.cursor.execute("INSERT into Commission (nom) values ('" + nom + "')")
		
    def commission_liste(self) :
        """
        Liste les commissions
        """
        self.cursor.execute("SELECT * from Commission")
        return self.cursor.fetchall()
	
    def activitee_ajout(self, nom, commission) :
        """
        Ajoute une activitée
        """
        # on recupère l'ID de la commission
        self.cursor.execute("SELECT rowid from Commission where nom = '" + commission +"'")
        try :
            idcommission = self.cursor.fetchone()[0]
        except TypeError :
            raise TypeError("Commission inconnut")
        self.cursor.execute("INSERT into activitee (nom, idcommission) values ('" + nom + "'," + str(idcommission) + ")")
	
    def activitee_liste(self, commission = None) :
        """
        Liste les activitées
        Peuvent être filtré par commission
        """
        if commission :
            rapport = ''
            for lis in commission :
                rapport = rapport + "'" + lis + "',"
            self.cursor.execute("SELECT ac.nom, co.nom, ac.date from Activitee ac INNER JOIN Commission co ON ac.idcommission = co.rowid WHERE co.nom in (" + rapport[:-1] + ")")
        else :
            self.cursor.execute("SELECT ac.nom, co.nom, ac.date from Activitee ac INNER JOIN Commission co ON ac.idcommission = co.rowid")
        return self.cursor.fetchall()
    
    def activitee_synthese(self, commission = None) :
        """
        Synthèse des activitées
        Peuvent être filtré par commission
        """
        if commission :
            rapport = ''
            for lis in commission :
                rapport = rapport + "'" + lis + "',"
            self.cursor.execute("SELECT co.nom, count(ac.idcommission) as Total from Activitee ac inner join Commission co ON ac.idcommission = co.rowid WHERE co.nom in (" + rapport[:-1] + ") group by co.nom")
        else :
            self.cursor.execute("SELECT co.nom, count(ac.idcommission) as Total from Activitee ac inner join Commission co ON ac.idcommission = co.rowid group by co.nom")
        return self.cursor.fetchall()

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
