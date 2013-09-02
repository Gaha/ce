#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ce import CE

import time

"""
Initialise la base de test

"""

if __name__ == '__main__':

	base = CE()

	# initialisation table agent
	base.agent_ajout("MARCEL","Henri")
	base.agent_ajout("DUPONT","Marcel")
	base.agent_ajout("BISIOT","Solange")
	base.agent_ajout("ZIMMAN","Bouffi")
	
	#initialisation table commission
	base.commission_ajout("Activitees,Decouvertes")
	base.commission_ajout("Service au personnel")
	base.commission_ajout("Sport")
	base.commission_ajout("Jeunesse")
	base.commission_ajout("Voyage")
	base.commission_ajout("Hebergement")
    
    # ajout d'activitées
	base.activitee_ajout("Tournoi de badminton","Sport")
	base.activitee_ajout("Initiation Floorball","Sport")
	base.activitee_ajout("Match Handball","Sport")
	base.activitee_ajout("Match Volley","Sport")
	base.activitee_ajout("Piece de theatre","Activitees,Decouvertes")
	base.activitee_ajout("Boowling","Activitees,Decouvertes")
	base.activitee_ajout("Saint-Nicolas cinema","Jeunesse")
	
	# ajout des participations
	base.participation_ajout("MARCEL","Henri","Match Volley")
	base.participation_ajout("DUPONT","Marcel","Match Volley",0,3)
	base.participation_ajout("ZIMMAN","Bouffi","Match Volley",1)
	base.participation_ajout("MARCEL","Henri","Boowling",1,2)
	
