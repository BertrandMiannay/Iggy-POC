

# Graph reduction
python tools/graphCompaction.py graphs/graphToyExample.sif ReducedGraphsif DicoNodes grapheMEF.lp

# Correlation identification
clingo grapheMEF.lp tools/optimizationComponent.lp -n 0 --opt-mode=optN --enum-mode=cautious --quiet=1 | grep "correle"| sort | uniq | sed s/" "/"\n"/g | sed s/")"/")."/g > correlations.csv

# Components identification
python tools/componentIdentification.py  DicoNodes correlations.csv > temporyFile

# Components sorting
python tools/componentsSort.py temporyFile | sort > components.csv
rm temporyFile

# MS computing
python tools/MSComputing.py data/dataExample.NA components.csv >> resultat_MS.csv
