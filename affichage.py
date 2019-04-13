# -*- coding: utf-8 -*-

#=========================================
#
#       o O  TP 9 : Billard   Oo
#
#==========================================
#
# Fichier : affichage.py
# Date : 2 décembre 12
# Auteurs : Eynard Julien
#
# Contient le squelette du code pour la gestion
# et l'affichage du billard
#
#===========================================


############# Quelques modules utiles #############

from boule import Boule,RAYON,LARGEUR,LONGUEUR,BORD
import pygame
from pygame.locals import *


############# Quelques fonctions utiles #############

def position_initiale():
	""" On récupère dans le fichier infos_boules.txt les positions initiales de chaque boules, et on crée toutes les boules sur ces positions """
	listeBoules=[]
	fichier=open("infos_boules.txt","r")
	for ligne in fichier:
		C=""
		L=ligne.split(",")
		for i in range(len(L[2])-1):
			C=C+L[2][i]
		listeBoules.append(Boule((int(L[0]),int(L[1])),(0,0),C))
		print(C)
	return listeBoules


def gestion_collisions(listeBoules):
	""" gestion des collisions de boules contenues dans la liste passée en paramètre, en utilisant la méthode collision de la classe Boule
	Paramètre :
		- listeBoules : liste des boules auxquelles on applique les méthodes de collision
	"""
	#attention, comme la méthode collision modifie la boule sur laquelle on appelle la méthode et la boule passée en paramètre, on n'appliquera pas plus d'une fois cette méthode sur les deux mêmes boules : ie si B1.collision(B2), alors on ne fera pas B2.collision(B1)
	for i in range(len(listeBoules)):
		for j in range(i+1,int(len(listeBoules))):
			(listeBoules[i]).collision(listeBoules[j])


############# Création du billard, affichage graphique #############

# on initialise pygame
pygame.init()

# on crée une fenêtre que l'on stocke dans une variable nommée ecran. Les dimensions de la fenêtre sont celles stockées dans les variables LARGEUR et LONGUEUR (exprimées en pixels)
ecran = pygame.display.set_mode( (LARGEUR,LONGUEUR) )

# on donne un joli titre à la fenêtre
pygame.display.set_caption("SNOOKER")
# on récupère le fond qui est l'image du billard avec ses bandes, que l'on met dans une variable nommée fond
fond = pygame.image.load("Plan.png")
black=pygame.transform.scale(pygame.image.load("black.png"),(RAYON*2,2*RAYON))
logo=pygame.transform.scale(pygame.image.load("logo.png"),(480,200))
chalk=pygame.transform.scale(pygame.image.load("chalk.png"),(BORD,BORD))

# création boule(s)
# b1 = Boule((0,0),(50,20),"boule_rouge.png")
# b2 = Boule((20,40),(80,10),"boule_jaune.png")
# b3 = Boule((100,40),(50,20),"boule_jaune.png")
# b4 = Boule((20,400),(80,30),"boule_jaune.png")
Liste=position_initiale()
BB=Liste[len(Liste)-1]

# boucle de gestion des événements et d'affichage (dont on ne sort que si l'on ferme la fenêtre)
onContinue = True
horloge = pygame.time.Clock()
while onContinue:

	# Gestion des événements (on parcourt tous les événements, et si un évènement est de type QUIT, alors on ne continue plus)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			onContinue = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# clic gauche pour tirer
			if event.button == 1:
				# on récupère la position de la souris
				posM = pygame.mouse.get_pos()	# posM est un tuple d'entier : coordonnées de la position de la souris au moment du clic
				# le nouveau vecteur vitesse de la boule blanche est le vecteur allant du centre de la boule à la position de la souris
				BB.vx=posM[0]-BB.x
				BB.vy=posM[1]-BB.y
			# clic droit pour redémarrer le jeu
			if event.button == 3:
				Liste=position_initiale()
				BB=Liste[len(Liste)-1]
	# on colle le fond dans la fenêtre
	ecran.blit(fond, (0,0))
	ecran.blit(black, (0,0))
	ecran.blit(black, (LARGEUR-BORD,0))
	ecran.blit(black, (0,LONGUEUR-BORD))
	ecran.blit(black, (LARGEUR,LONGUEUR))
	ecran.blit(black, (-7,LONGUEUR/2))
	ecran.blit(black, (LARGEUR-BORD,LONGUEUR/2))
	ecran.blit(logo, (BORD-15,350))
	ecran.blit(chalk, (LARGEUR-BORD,600))

	# calcul de la nouvelle vitesse, déplacement, vérification rebonds et collisions, et affichage graphique boule(s)
	for b in Liste:
		b.affiche(ecran)
		b.deplace()
		b.rebond()
		b.calculeVitesse()

	gestion_collisions(Liste)

	# on met à jour l'affichage
	pygame.display.flip()

	# on attend un petit peu, pour ne boucler que 25 fois maxi par seconde
	horloge.tick(25)
