# Iggy-POC 
**Iggy-Poc is a graph coloring model created by Bertrand Miannay to :**
- Identify subnetworks from a prior knowledge network (PKN).
- Compute the maximal similarity with each subnetwork from a set of observations.

This model need Python 2.7.6, the package NetworkX and Clingo 4.5.4 ( https://sourceforge.net/projects/potassco/files/clingo/4.2.1/)

 **To try a toy example, the toyExample.sh file allows to use the framework on a small network :**   
    chmod 777 toyExample.sh    
    ./toyExample.sh

**Files : **

-  graphCompaction.py
    - Example : python tools/graphCompaction.py graphToyExample.sif ReducedGraph DicoNodes grapheMEF.lp

    - Generate a reduced graph based on subcomponents identification
    - Input : 
        - graphToyExample.sif : PKN file respecting sif format (A  1   B)
    - Output : 
        - ReducedGraph.sif : Reduced graph respecting sif format
        - DicoNodes :  Hash table  ("A +" : node1)
        - grapheMEF.lp : reduced graph respecting lp format (edge(node1,node2,1,2).)

- optimizationComponent.lp
    - Example : clingo grapheMEF.lp tools/optimizationComponent.lp -n 0 --opt-mode=optN --enum-mode=cautious --quiet=1 | grep "correle"| sort | uniq | sed s/" "/"\n"/g | sed s/")"/")."/g > correlations.csv
    - Identification of correlated nodes in the graph based on the perfect colorations constraints
    - Input : 
        - grapheMEF.lp : reduced graph respecting lp format (edge(node1,node2,1,2).)
    - Output : 
        - correlations.csv : correlation between nodes (correlePositif(node2,node1).)
    
    
- componentIdentification.py 
    - Example : python tools/componentIdentification.py  DicoNodes correlations.csv > temporyFile
    - Input   
           - DicoNodes : Hash table  ("A +" : node1)
           - correlations.csv : correlation between nodes (correlePositif(node2,node1).)
    - Output
        - temporyFile : Unsorted components ("B +, C -, A +")
    
- componentsSort.py
    - Example : python tools/componentsSort.py temporyFile | sort > components.csv
    - Input   
           - temporyFile : Unsorted components ("B +, C -, A -")
    - Output
        - components.csv : Sorted components ("A +, B -, C +")

- MSComputing.py
    - Example : python tools/MSComputing.py dataExample.NA components.csv >> resultat_MS.csv
    - Input   
           - dataExample.NA : Observations (A = 0)
           - components.csv : Sorted components ("A +, B -, C +")
    - Output
        - resultat_MS.csv : Sorted components ("A +, B -, C +")

