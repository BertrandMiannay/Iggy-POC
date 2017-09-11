# Iggy-POC is a graph coloring model created by Bertrand Miannay to :
- Identify subnetworks from a prior knowledge network.
- Compute the maximal similarity with each subnetwork from a set of observations.

# To try a toy example, the toyExample.sh file allows to use the framework on a small network :
    chmod 777 toyExample.sh
    ./toyExample.sh

# Files :
- componentIdentification.py 
    - Use example : 
    python tools/componentIdentification.py  DicoNodes correlations.csv > temporyFile
    - Input 
           - DicoNodes 
           - correlations.csv
    - 
    
- componentsSort.py	Ajout Fichiers	6 days ago
    - test
- graphCompaction.py	Ajout Fichiers	6 days ago
- optimizationComponent.lp
