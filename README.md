# Iggy-POC is a graph coloring model created by Bertrand Miannay to :
- Identify subnetworks from a prior knowledge network (PKN).
- Compute the maximal similarity with each subnetwork from a set of observations.

This model need Python (... Version), the package NetworkX and Clingo (... Version : https://sourceforge.net/projects/potassco/files/clingo/4.2.1/)

# To try a toy example, the toyExample.sh file allows to use the framework on a small network :
    chmod 777 toyExample.sh
    ./toyExample.sh

# Files :
- graphCompaction.py
    - Use example : python graphCompaction.py Initialgraph.sif ReducedGraph.sif DicoNodes grapheMEF.lp
    - Generate a reduced graph based on subcomponents identification
    - Input : 
        - Initialgraph.sif : PKN file respecting sif format (A  1   B)
    - Output : 
        - ReducedGraph.sif : Reduced graph respecting sif format
        - DicoNodes :  Hash table  ("A +" : node1)
        - grapheMEF.lp : reduced graph respecting lp format (edge(node1,node2,1,2).)

- optimizationComponent.lp
    - Use example : clingo grapheMEF.lp tools/optimizationComponent.lp -n 0 --opt-mode=optN --enum-mode=cautious --quiet=1 | grep "correle"| sort | uniq | sed s/" "/"\n"/g | sed s/")"/")."/g > correlations.csv
    - Identification of correlated nodes in the graph based on the perfect colorations constraints
    - Input : 
        - grapheMEF.lp : reduced graph respecting lp format (edge(node1,node2,1,2).)
    - Output : 
        - correlations.csv : 
    
    
- componentIdentification.py 
    - Use example : python tools/componentIdentification.py  DicoNodes correlations.csv > temporyFile
    - Input   
           - DicoNodes : Hash table  
           - correlations.csv : correlation
    - Output
        - test
    
- componentsSort.py	Ajout Fichiers	6 days ago
    - test




clingo grapheMEF.lp tools/optimizationComponent.lp -n 0 --opt-mode=optN --enum-mode=cautious --quiet=1 | grep "correle"| sort | uniq | sed s/" "/"\n"/g | sed s/")"/")."/g > correlations.csv

python tools/componentIdentification.py  DicoNodes correlations.csv > temporyFile

python tools/componentsSort.py temporyFile | sort > components.csv
