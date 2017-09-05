# -*-coding:Latin-1 -*

import os
import sys



DicoInversionSigne={}
DicoInversionSigne["+"]="-"
DicoInversionSigne["-"]="+"
# Ouvrir fichier des Composants
# Charger Dico des nodes
file=open(sys.argv[1],"rb")
data=file.readlines()
file.close()



# Pour chacune de ces composantes :
for composant in data:
#	Diviser en sous-bloc
	listeNodes=composant.split(",")
#	Trier les bloc
	listeNodes.sort()
# 	Si signe du premier bloc == "-"
	inversion=False
	if(listeNodes[0].split(" ")[1].split("\n")[0]=="-"):
		# Inversion=Vrai
		inversion=True

# 	Reecriture
	ligne=""
	for soustuple in listeNodes:
		node=soustuple.split(" ")[0]
		signe=soustuple.split(" ")[1].split("\n")[0]
		# Si il faut inverser le signe
		if(inversion):
			signe=DicoInversionSigne[signe]
		ligne=ligne+","+node+" "+signe

	print(ligne[1:len(ligne)])
	
