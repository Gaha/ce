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
	base.commission_ajout("Activitees,Decouverte")
	base.commission_ajout("Service au personnel")
	base.commission_ajout("Sport")
	base.commission_ajout("Jeunesse")
	base.commission_ajout("Voyage")
	base.commission_ajout("Hebergement")
    
