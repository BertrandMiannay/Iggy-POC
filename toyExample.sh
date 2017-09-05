 graph=graphs/graphToyExample.sif



python graphCompaction.py $graph ReducedGraph DicoNodes grapheMEF.lp

clingo grapheMEF.lp tools/optimizationComponent.lp -n 0 --opt-mode=optN --enum-mode=cautious --quiet=1 | grep "correle"| sort | uniq | sed s/" "/"\n"/g | sed s/")"/")."/g > correlations.csv

python tools/componentIdentification.py  DicoNodes correlations.csv > temporyFile

python tools/componentsSort.py temporyFile | sort > components.csv
rm temporyFile
