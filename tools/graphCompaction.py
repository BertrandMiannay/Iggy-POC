# -*-coding:Latin-1 -*
# Identification des tuples sur la base de la topologie du graphe

# python identificationTUplesTopologie.py grapheTest grapheSortie
import networkx as nx
import os
import sys

# Renvoie un graphe fusionné sans suppression des arcs (contrairement à la fonction pré-installée relabel_nodes)

# python tools/identificationTuplesTopologie.py graphe_0.2_MEF.sif grapheResult > result
# python tools/identificationTuplesTopologie.py NCI-pid.sif grapheResult > result

def InversionTuple(node):
	Dico={}
	Dico["+"]="-"
	Dico["-"]="+"
	tupleInverse=""
	for sousTuple in node.split(","):
		#print(sousTuple)
		sousNode=sousTuple.split(" ")[0]
		sousSigne=sousTuple.split(" ")[1]
		#print(sousNode)
	#	print(sousSigne)
		tupleInverse=tupleInverse+","+sousNode+" "+Dico[sousSigne]	
	tupleInverse=(tupleInverse[1:len(tupleInverse)+1])
	return tupleInverse



# Renvoie le nom du tuple fusionnant les prédécesseurs fusionnables (en prenant en compte le type d'arc)
def FusionTuples(PredecesseursFusionnables,node,G):
	nouveauTuple=""
	for sousTuple in PredecesseursFusionnables:
		#print(sousTuple)
		tupleCalcule=sousTuple
		arc=G[sousTuple][node][0]['edge_type']
		if(arc == "-1"):
#			print("inversion")
			tupleCalcule=InversionTuple(tupleCalcule)
			
		nouveauTuple=nouveauTuple+","+tupleCalcule
	nouveauTuple=(nouveauTuple[1:len(nouveauTuple)+1])
	return(nouveauTuple) 	



# Renvoie la liste des prédécesseurs qui peuvent fusionner
def IdentificationPredecessorsFusionnables(G,ListePredecesseurs):
	fusionnable=[]
	for node in ListePredecesseurs:
		listeSuccesseurs=G.successors(node)		
		listePredecessors=G.predecessors(node)
		if((len(listeSuccesseurs)==1) and (len(listePredecessors)==0) and (len(G[node][listeSuccesseurs[0]])==1) and (node not in Compacte) and (listeSuccesseurs[0] not in Compacte) ):
			fusionnable.append(node)
	return(fusionnable)


# Renvoie false si 
	# la target a un arc vers la source de signe différent
def FusionPossible(source,target, graphe, arc):
	resultat=True
	listeTarget=G.successors(target)
	# Parcours de successeurs de la cible
	if(source in listeTarget):
		for edge in G[target][source]:
			if(G[target][source][edge]['edge_type'] != arc):
				return False

	return True

def FusionNodes(graphe,dico,inversionArc):
	# Créer un nouveau graphe H
	H=nx.MultiDiGraph()
	ListeArcs=[]
	inversion={}
	inversion["1"]="-1"
	inversion["-1"]="1"
	# Pour chaque noeud du graphe
	for node in graphe.nodes():
		H.add_node(dico[node])
	# Pour chaque arc du graphe G
	for edges in graphe.edges():
		#print(edges)
		source=edges[0]
		target=edges[1]
		#print("ci")
		for edge in graphe[source][target]:
			#print(graphe[source][target][edge])
			arc=graphe[source][target][edge]['edge_type']
			if(source in inversionArc):
				arc=inversion[arc]
				#print(dico[source]+" => "+str(arc)+" => "+dico[target])
			edge=dico[source]+dico[target]+str(arc)
			#print(edge)
			# Si l'arc n'existe pas encore
			if(edge not in ListeArcs):
				#print("non existant")
				ListeArcs.append(edge)
				# Ajouter un arc en mappant les noeud du dico
				H.add_edge(dico[source],dico[target],edge_type=arc)
	# Renvoyer nouveauGraphe
	return(H)


# Renvoie le tuple avec les signes inversés
def inversionTuple(tuple):
	inversion={}
	inversion["+"]="-"
	inversion["-"]="+"
	TupleInverse=""
	for sousTuple in tuple.split(","):
		node=sousTuple.split(" ")[0]
		signe=inversion[sousTuple.split(" ")[1]]
		TupleInverse=TupleInverse+","+node+" "+signe
	# Enlever l'entête
	TupleInverse=TupleInverse[1:len(TupleInverse)+1]
	#print(TupleInverse)
	return(TupleInverse)
		

# Renvoie le signe du noeud du tuple connectant le noeud au tuple initialement
def ArcOriginel(TuplePred,noeudSource,grapheOriginel):
	noeudTarget=noeudSource.split(" ")[0]+" +"
	# Pour chaque noeud du Tuple	
	for sousTuple in TuplePred.split(","):
		node=sousTuple.split(" ")[0]+" +"
		signe=sousTuple.split(" ")[1]
		if(grapheOriginel.has_edge(node,noeudTarget)):
			return(signe)
		# S'il existe un arc entre ce noeud et le noeudSource
			# Renvoyer signe

# Fonction de generation des Tuples
def generationTuple(predecesseur, noeudSource, arc,grapheOriginel):
	#print("Fusion de "+predecesseur+" avec "+noeudSource)
	if(arc=="1"):
		arc="+"
	elif(arc=="-1"):
		arc="-"
	else:
		print("erreur d'arc : "+str(arc))
	if(arc=="-"):
		# Noeud source inverse
		#print("inversion")
		noeudSource=inversionTuple(noeudSource)
	# Gestion des cas de doubles inhibition
	SigneLastNode=ArcOriginel(predecesseur,noeudSource,grapheOriginel)
	#print(SigneLastNode)
	#if(SigneLastNode=="-"):
		#print("avant : "+noeudSource)
		#noeudSource=inversionTuple(noeudSource)
		#print("apres : "+noeudSource)
	nouveauTuple=predecesseur+","+noeudSource
	return(nouveauTuple)


# convertir le graphe en graphe networkX
file=open(sys.argv[1],"rb")
data=file.readlines()
file.close()
#print(data) 
G=nx.MultiDiGraph()
GOrigine=nx.MultiDiGraph()
#print(data)
separateur="\t"
node_type={}
for row in data:
	if (len(row.split(separateur)) == 3):
		sourceOrigine=row.split(separateur)[0]
		source=row.split(separateur)[0]+" +"
		modele=row.split(separateur)[1]
		targetOrigine=row.split(separateur)[2].split("\n")[0].split("\r")[0]
		target=row.split(separateur)[2].split("\n")[0].split("\r")[0]+" +"
		#G.add_edge(source,target,edge_type=str(modele))
		if(modele=="inhibitor" or modele=="-1"):
			G.add_edge(source,target,edge_type="-1")
			GOrigine.add_edge(sourceOrigine,targetOrigine,edge_type="-1")
		else:
			G.add_edge(source,target,edge_type="1")
			GOrigine.add_edge(sourceOrigine,targetOrigine,edge_type="1")
		
#print("graphe initial de "+str(len(G.nodes()))+" nodes")
#print("graphe initial de "+str(len(G.edges()))+" arcs")
Copie=G.copy()
nbreTuples=len(G.nodes())
nbreArcs=len(G.edges())
nouveauNbreTuples=0
nouveauNbreArcs=0

NxNombreTuplesGlobal=0
NombreTuplesGlobal=nbreTuples
NxNombreArcsGlobal=0
NombreArcsGlobal=len(G.edges())
listeIsole=[]

print("graph with "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")
while(NxNombreTuplesGlobal!=NombreTuplesGlobal or NombreArcsGlobal!=NxNombreArcsGlobal):
	print("cycle "+str(NombreTuplesGlobal)) 
	NxNombreTuplesGlobal=NombreTuplesGlobal
	NxNombreArcsGlobal=NombreArcsGlobal
	# REDUCTION SUR LA COHERENCE
	suppression=[]
	# Tant que le nbre de Tuples varie
	while(nbreTuples!=nouveauNbreTuples):
		nbreTuples=nouveauNbreTuples
		# Reinitialisation des fusions
		Fusion=[]
		Dico={}
		InversionArc=[]
		for node in G.nodes():
			Dico[node]=node
		# Pour chaque Noeud
		for node in G.nodes():
		
			predecesseurs=G.predecessors(node)
			# Si nbre Predecesseur == 1 ET predec ne fusionne pas ET node ne fusionne pas
			if(len(predecesseurs)==1 and predecesseurs[0] not in Fusion and node not in Fusion and len(G[predecesseurs[0]][node])==1 and FusionPossible(predecesseurs[0],node, G, G[predecesseurs[0]][node][0]['edge_type'])):
			
				#print(node+ " fusion avec "+predecesseurs[0])
				# Si le pred et noeud partagent 2 arcs différent
				#print(node+" avec "+predecesseurs[0])
				Fusion.append(node)
				Fusion.append(predecesseurs[0])
				#print(G[predecesseurs[0]][node])
				NouveauTuple=generationTuple(predecesseurs[0], node,G[predecesseurs[0]][node][0]['edge_type'],Copie)
				Dico[node]=NouveauTuple
				Dico[predecesseurs[0]]=NouveauTuple
				if(G[predecesseurs[0]][node][0]['edge_type']=="-1"):
					InversionArc.append(node)
				# Fusionner(noeud, pred, arc)
		# Mise à jour du nbre de Tuples	
		G=FusionNodes(G,Dico,InversionArc)
	
		G.remove_edges_from(G.selfloop_edges())
		nouveauNbreTuples=len(G.nodes())
	print("Reduction to "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")

	##################################
	# REDUCTION SUR LA PERFECTION ####
	##################################

	#print("reduction par perfection")
	suppression=[]
	reduction=False
	rename={}
	# Réinitialiser la liste des noeuds à compacter
	Compacte=[]
	# Pour chaque noeud
	for node in G.nodes():
		
		rename[node]=node
		# récupérer liste prédecesseurs
		ListePredecesseurs=G.predecessors(node)
		PredecesseursFusionnables=IdentificationPredecessorsFusionnables(G,ListePredecesseurs)
		
		# Si plus d'un prédécesseur fusionnable
		if(len(PredecesseursFusionnables)>1):
			# FUsion de ces noeuds
				# Créer un nom de tuple commun et mettre en dico rename
				reduction=True
				NouveauTuple=FusionTuples(PredecesseursFusionnables,node,G)
				
				G.add_edge(NouveauTuple,node,edge_type="1")
				# Stocker les autres noeud en suppression
				for sousNode in PredecesseursFusionnables:
					suppression.append(sousNode)
 
	G.remove_nodes_from(suppression)
	print("Reduction to "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")

	#########################################
	# REDUCTION SUR PREDECESSEURS ISOLES ####
	#########################################
	Copie=G.copy()
	nbreTuples=len(G.nodes())
	nbreArcs=len(G.edges())
	nouveauNbreTuples=0
	nouveauNbreArcs=0

	nbreNoeudsCycle=0
	NxnbreNoeudsReduction=nbreTuples
	listeConsistent=[]


	while(nbreNoeudsCycle!=NxnbreNoeudsReduction):
		nbreNoeudsCycle=len(G.nodes())
		suppression=[]
		rename={}
		# Réinitialiser la liste des noeuds à compacter
		Compacte=[]
		# Pour chaque noeud
		for node in G.nodes():
			rename[node]=node
		for node in G.nodes():
			successeur=G.successors(node)
			predecesseur=G.predecessors(node)
			# Si noeud sans predecesseur, 1 successeur et un seul signe entre les 2
			if(len(successeur)==1 and len(predecesseur)==0 and len(G[node][successeur[0]])==1):
				tete=successeur[0].split(",")[0]
				if(tete not in listeConsistent):
					listeConsistent.append(tete)
				suppression.append(node)
				nouveauTuple=node
				# Si arc inhibiteur => Inversion du tuple
				if(G[node][successeur[0]][0]['edge_type']=="-1"):
					nouveauTuple=InversionTuple(nouveauTuple)
		
				rename[successeur[0]]=rename[successeur[0]]+","+nouveauTuple
		G.remove_nodes_from(suppression)
		NxnbreNoeudsReduction=len(G.nodes())
		G=nx.relabel_nodes(G,rename)
		listeConsistent


	DicoNodes={}
	DicoInverse={}
	nbreNode=0
	for node in G.nodes(): 
		DicoInverse[node]="node"+str(nbreNode)
		DicoNodes[DicoInverse[node]]=node
		nbreNode=nbreNode+1
	
	print("Reduction to "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")

	#######################	
	# REDUCTION DES ARCS ##
	#######################	

	Copie=nx.MultiDiGraph()
	Copie.add_nodes_from(G.nodes())
	#print("reduction des arcs")
	for edge in G.edges():
		poidsActivation=0
		poidsInhibition=0
		source=edge[0]
		target=edge[1]

		if(len(source.split("\"")) > 1 ):
		       source=source.split("\"")[1]
		if(len(target.split("\"")) > 1 ):
		        target=target.split("\"")[1]
		for sousTuple1 in source.split(","):
			# Pour chaque sousNoeud de tuple2
		        for sousTuple2 in target.split(","):
		                node1=sousTuple1.split(" ")[0]
				signeSource=sousTuple1.split(" ")[1]
				#print(sousTuple1+ " to "+node1+" "+signeSource)
		                node2=sousTuple2.split(" ")[0]
		                if(GOrigine.has_edge(node1,node2)):
					
		                        for edgeOrigine in GOrigine[node1][node2]:
		                                arc=(GOrigine[node1][node2][edgeOrigine]['edge_type'])
					#	print(node1+" to "+node2+" "+arc)
		                                if(arc == "1"):
							if(signeSource=="+"):
								 poidsActivation=poidsActivation+1
							else:
			                                        poidsInhibition=poidsInhibition+1
		                                elif(arc=="-1"):
		                                        if(signeSource=="+"):
								 poidsInhibition=poidsInhibition+1
							else:
			                                       poidsActivation=poidsActivation+1

		poidsMin=min(poidsActivation,poidsInhibition)  
		retour=True
#		poidsMin=0 
		if(poidsActivation-poidsMin >0):
			Copie.add_edge(source,target,edge_type="1")  
		if(poidsInhibition-poidsMin >0):
			Copie.add_edge(source,target,edge_type="-1") 
		# Cas isolement d'un arc 
		if(poidsActivation==poidsInhibition and poidsActivation !=0):
			# Stocker tuple pour préciser target : consistent + imperfect
			tete=edge[1].split(",")[0]
			if(tete not in listeIsole):
				listeIsole.append(tete)

#	print(Copie.edges())
#	print(G.edges())
	G=Copie

	nouveauNbreTuples=len(G.nodes())
	nouveauNbreArcs=len(G.edges())
	NombreArcsGlobal=nouveauNbreArcs
	NombreTuplesGlobal=nouveauNbreTuples
	print("Reduction to "+str(len(G.nodes()))+" nodes and "+str(len(G.edges()))+" edges")
	#print(str(NombreTuplesGlobal)+" vs "+str(NxNombreTuplesGlobal))
	#print(str(NombreArcsGlobal)+" vs "+str(NxNombreArcsGlobal))

	# A SUPPRIMER POUR BOUCLER
	NxNombreTuplesGlobal=NombreTuplesGlobal
	NombreArcsGlobal=NxNombreArcsGlobal


# Listing des arcs
listeArcs=[]
for i in G.edges():
	#print(i)
	source=i[0]
	target=i[1]
	for arc in (G[source][target]):
		edge="\""+source+"\""+"\t"+str(G[source][target][arc]['edge_type'])+"\t"+"\""+target+"\""
		if(edge not in listeArcs):
			listeArcs.append(edge)
	if(source==target):
		print("Frappe "+source+" => "+str(G[source][target][arc]['edge_type']))


file=open(sys.argv[2],"w")
for i in listeArcs:
	file.write(i+"\n")
#	print(G[
file.close()


# Ecriture du Dictionnaire
file=open(sys.argv[3],"w")
for node in G.nodes():
	file.write("\""+node+"\" : "+DicoInverse[node]+"\n")

file.close()




fileOutput=open(sys.argv[4],"w")
# Ecriture du graphe Mis en forme
NodeUtilise=G.nodes()
for edge in G.edges():
	poidsActivation=0
	poidsInhibition=0
	source=edge[0]
	target=edge[1]
	if(len(source.split("\"")) > 1 ):
	       source=source.split("\"")[1]
	if(len(target.split("\"")) > 1 ):
	        target=target.split("\"")[1]
	for sousTuple1 in source.split(","):
		# Pour chaque sousNoeud de tuple2
	        for sousTuple2 in target.split(","):
	                node1=sousTuple1.split(" ")[0]
			signeSource=sousTuple1.split(" ")[1]
			#print(sousTuple1+ " to "+node1+" "+signeSource)
	                node2=sousTuple2.split(" ")[0]
	               # print("test "+node1+" to "+node2)
	                if(GOrigine.has_edge(node1,node2)):
	                        for edgeOrigine in GOrigine[node1][node2]:
	                                arc=(GOrigine[node1][node2][edgeOrigine]['edge_type'])
				#	print(node1+" to "+node2+" "+arc)
	                                if(arc == "1"):
						if(signeSource=="+"):
							 poidsActivation=poidsActivation+1
						else:
		                                        poidsInhibition=poidsInhibition+1
	                                elif(arc=="-1"):
	                                        if(signeSource=="+"):
							 poidsInhibition=poidsInhibition+1
						else:
		                                       poidsActivation=poidsActivation+1
	poidsMin=min(poidsActivation,poidsInhibition)
	if(poidsActivation-poidsMin!=0):
		if(edge[0] in NodeUtilise):
			NodeUtilise.remove(edge[0])
		if(edge[1] in NodeUtilise):
			NodeUtilise.remove(edge[1])


        #print("("+source+ ","+target+",1,"+str(poidsActivation)+").")
        	fileOutput.write("edge("+DicoInverse[edge[0]]+ ","+DicoInverse[edge[1]]+",1,"+str(poidsActivation-poidsMin)+").")
	if(poidsInhibition-poidsMin!=0):
		if(edge[0] in NodeUtilise):
			NodeUtilise.remove(edge[0])
		if(edge[1] in NodeUtilise):
			NodeUtilise.remove(edge[1])
		#print("("+source+ ","+target+",-1,"+str(poidsInhibition)+").")
		fileOutput.write("edge("+DicoInverse[edge[0]]+ ","+DicoInverse[edge[1]]+",-1,"+str(poidsInhibition-poidsMin)+").")

	# Checker si besoin d'afficher les composants pré-identifiés : En liste "NodeUtilise"	

	
# Recuperation des cibles imparfaites
for component in listeIsole:
	#print(component)
	for node in G.nodes():
		if(node.find(component)!=-1):
			fileOutput.write("imperfectcoloring("+DicoInverse[node]+").")
			fileOutput.write("consistentTarget("+DicoInverse[node]+").")                          




# Recuperation des cibles cohérentes
for component in listeConsistent:
	#print(component)
	for node in G.nodes():
		if(node.find(component)!=-1):	
			fileOutput.write("consistentTarget("+DicoInverse[node]+").")                          






fileOutput.close()

