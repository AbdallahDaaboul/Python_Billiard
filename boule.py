# -*- coding: utf-8 -*-

#=========================================
#
#       o O  TP 9 : Billard   Oo
#
#==========================================
#
# Fichier : classe.py
# Date : 2 décembre 12
# Auteurs : Eynard Julien
#
# Contient le squelette de la classe Boule
# qui modélise les boules de billard
#
#===========================================


############# Quelques modules utiles #############
import numpy
import pygame
from math import sqrt

############# Quelques constantes utiles #############

RAYON = 17	# rayon des boules, en pixel
DELTA_T = 0.35	# intervalle de temps entre deux rafraîchissement de la position
ACC = 0.25	# accélération subie par les boules en mouvement
EPSILON = 0.15	# constante en dessous de laquelle la vitesse devient nulle

# taille de la fenêtre d'affichage pour pyGame
LARGEUR = 500
LONGUEUR = 800

# largeur des bandes
BORD = 25

############# Classe Boule #############

class Boule:
	""" Classe qui définit une boule.
	Une boule sera définie par :
		- ses coordonnées (x, y)
		- sa vitesse (vx, vy)
		- une image pour une représentation graphique, dimensionnée suivant le rayon
	"""


	def __init__(self, position, vitesse, nomFichierImage):
		""" Constructeur d'une Boule.
		Paramètres :
			- position : tuple des coordonnées initiales du centre de la boule
			- vitesse : tuple des coordonnées du vecteur vitesse initial
			- nomFichierImage : nom du fichier de l'image utilisée pour l'afficher
		"""
		self.nom=nomFichierImage
		# coordonnées du centre de la boule
		self.x, self.y = position

		# coordonnées du vecteur vitesse
		self.vx, self.vy = vitesse

		# l'image de la boule
		# ...			(chargement de l'image , transparence du fond, redimensionnement)
		self.image = pygame.transform.scale(pygame.image.load(nomFichierImage),(RAYON*2,2*RAYON))
		#image.transform.scale(RAYON,(30,30))

#	def __str__(self):
#		""" Renvoie une chaine de caractère décrivant la Boule (position et vitesse) """
#		return ( "La boule est a la position: (" + str(self.x) + " " + str(self.y) + ") et a une vitesse de:(" + str(self.vx) + " " +str(self.vy)+")")


	def affiche(self,ecran):
		ecran.blit(self.image,(self.x,self.y))


	def deplace(self):
		""" Déplace une Boule en fonction de sa vitesse. On utilise une intégration par rectangle (l'intervalle de temps considéré est DELTA_T, donné dans les constantes)
		"""

		self.x += self.vx * DELTA_T
		self.y += self.vy * DELTA_T


	def rebond(self):
	 	""" Permet de gérer le rebond des particules sur les bandes de la table """
	 	if not(BORD < self.x < LARGEUR -2*RAYON - BORD):
			self.vx=-self.vx
		if not(BORD < self.y < LONGUEUR -2*RAYON - BORD):
			self.vy=-self.vy
		if self.x < BORD:
			self.x = BORD
		elif self.x > LARGEUR - 2*RAYON - BORD:
			self.x=LARGEUR-2*RAYON-BORD
		if self.y < BORD:
			self.y=BORD
		elif self.y > LONGUEUR-2*RAYON-BORD:
			self.y=LONGUEUR-2*RAYON-BORD

		if ((self.x<=BORD+3 and self.y<=BORD+3) or (self.x>=LARGEUR -2*RAYON - BORD and self.y<=BORD+10) or (self.y>=LONGUEUR-2*RAYON-BORD and self.x<=BORD+10) or (self.y>=LONGUEUR-2*RAYON-BORD and self.x>=LARGEUR-BORD-2*RAYON) or(self.x<=BORD+10 and LONGUEUR/2-5<self.y<LONGUEUR/2+5) or (self.x >= LARGEUR-BORD-2*RAYON-10 and LONGUEUR/2-5<self.y<LONGUEUR/2+5)):
			self.x=1000
			self.y=1000
			self.vx=0
			self.vy=0

		if (self.nom=="boule_blanche.png" and self.x==1000):
			self.x=242
			self.y=717

	def dist(self,b):
	 	""" Calcule et renvoie la distance euclidienne entre la Boule et une autre Boule
	 	Paramètre:
	 		- b : l'autre Boule avec laquelle est calculée la distance
	 	Retour: la distance"""
	 	return (sqrt((self.x-b.x)**2+(self.y-b.y)**2))


	def collision(self,b):
	 	""" Gère la collision entre deux boules de même masse lors d'un choc élastique
	 	Paramètre :
	 		- b : l'autre boule avec laquelle la collision a lieu
	 	"""
		if self.dist(b) <=  2*RAYON:

	 		#vecteur n normal au plan de collision
	 		nx=self.x-b.x
			ny=self.y-b.y
			n=(nx,ny)
	 		#normalisation de n
			if(nx**2+ny**2!=0) :
				nx=nx/numpy.linalg.norm(n)
				ny=ny/numpy.linalg.norm(n)
				n=(nx,ny)

	 		#rotation pi/2 sens direct du vecteur n par exemple pour le vecteur tangentiel normalisé g
		 		gx=-ny
				gy=nx
				g=(gx,gy)

	 		#si les boules se superposent, on les replace en position de contact strict (ici, le vecteur g est inutile)
		 		delta=2*RAYON-self.dist(b)
				if (delta>0):
					b.x-=delta/2*nx
					self.x+=delta/2*nx
					b.y-=delta/2*ny
					self.y+=delta/2*ny

				#decomposition des vitesses sur la nouvelle base orthonormee (n,g)
				vx1=nx*self.vx+ny*self.vy
				vy1=gx*self.vx+gy*self.vy

				vx2=nx*b.vx+ny*b.vy
				vy2=gx*b.vx+gy*b.vy

				#echange des composantes normales ; les composantes tangentielles sont conservees

				self.vx=nx*vx2+gx*vy1
				self.vy=ny*vx2+gy*vy1
				b.vx=nx*vx1+gx*vy2
				b.vy=ny*vx1+gy*vy2

	def calculeVitesse(self):
			""" Calcule la vitesse en intégrant l'accélération ; le vecteur accélération a même direction et sens contraire à celui de la vitesse """
			v = sqrt(self.vx**2+self.vy**2)

			#si vitesse trop petite, on stoppe la boule
			if(v<EPSILON):
				self.vx=0
				self.vy=0
			#sinon, la vitesse diminue
			else:
				self.vx=self.vx-ACC*DELTA_T*self.vx/v
				self.vy=self.vy-ACC*DELTA_T*self.vy/v
