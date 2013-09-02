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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Participation (idagent integer, idactivitee integer, conjoint integer, enfant integer, externe integer, etat text)')

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
	
    def commission_synthese(self, commission = None) :
        """
        Synthèse des commissions
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
        self.cursor.execute("INSERT into Activitee (nom, idcommission) values ('" + nom + "'," + str(idcommission) + ")")
	
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
    
    
    def participation_ajout(self, nom, prenom, activitee, conjoint = 0, enfant = 0, externe = 0, etat = "Inscrit") :
        """
        Ajoute une participation
        """
        # on recupère l'ID du nom
        self.cursor.execute("SELECT rowid from Agent where nom = '" + nom + "' and prenom ='" + prenom + "'")
        try :
            idagent = self.cursor.fetchone()[0]
        except TypeError :
            raise TypeError("Agent inconnut")
        # on recupère l'ID de la commission
        self.cursor.execute("SELECT rowid from Activitee where nom = '" + activitee +"'")
        try :
            idactivitee = self.cursor.fetchone()[0]
        except TypeError :
            raise TypeError("Activitee inconnut")
        self.cursor.execute("INSERT into Participation (idagent, idactivitee, conjoint, enfant, externe, etat) values (" + str(idagent) + "," + str(idactivitee) + "," + str(conjoint) + "," + str(enfant) + "," + str(externe) + ",'" + etat +"')")
    
    def participation_liste(self, activitee = None) :
        """
        Liste les participations
        Filtre par activitee
        """
        if activitee :
            rapport = ''
            for lis in activitee :
                rapport = rapport + "'" + lis + "',"
            self.cursor.execute("SELECT ag.nom, ag.prenom, ac.nom, pa.conjoint, pa.enfant, pa.externe, pa.etat FROM Participation pa INNER JOIN Agent ag ON pa.idagent = ag.rowid INNER JOIN Activitee ac ON pa.idactivitee = ac.rowid WHERE ac.nom in (" + rapport[:-1] + ")")
        else :
            self.cursor.execute("SELECT ag.nom, ag.prenom, ac.nom, pa.conjoint, pa.enfant, pa.externe, pa.etat FROM Participation pa INNER JOIN Agent ag ON pa.idagent = ag.rowid INNER JOIN Activitee ac ON pa.idactivitee = ac.rowid")
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
    
    print Table("COMMISSION SYNTHESE", ["Commission","Activitée"], base.commission_synthese())
    print
    
    print Table("ACTIVITEE", ["Nom","Commission","Date"], base.activitee_liste())
    print
    
    print Table("Participations", ["Nom","Prenom","Activitée","Conjoint","Enfant","Externe","Etat"], base.participation_liste())
    print
    
