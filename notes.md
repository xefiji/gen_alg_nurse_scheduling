# Notes:
Encoding: binary with constraints
Crossover: singlepoint. prob: 0.5 (medium)
Selection: proportionate
Mutation: point. prob: 0.8 (high)

- https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3
- https://towardsdatascience.com/using-genetic-algorithms-to-schedule-timetables-27f132c9e280
- https://towardsdatascience.com/how-to-define-a-fitness-function-in-a-genetic-algorithm-be572b9ea3b4

lgorithmes d'approximation. L'aléa le rend non déterministe. Tant dans sa solution que dans son temps d'exécution. Compromis acceptable.

Ajouter des contraintes supplémentaires afin de structurer l algorithme ! Exemple du quadrillage du plan dans le pbm du voyageur de commerce.

Quand stopper ?
Après n itération
Après n temps
Si le max score a pas  augmenté depuis n itération  


"the fitness represent the sum of all penalties caused by the violations of constraints"
"the solution will be found when the fitness of the solutions reaches the value 0"
Différentes pénalités pour les contraintes
Les contraintes comme des distances par rapport à une cible

Faire un tableau:

| constraint | penalities or majoration |
| --- | --- |
| contrainte 1 | value ++ |
| contrainte 2 | value -- |


https://www.patatconference.org/patat2008/proceedings/Dean-WA3c.pdf

Penser aux priorConsecutiveDays

comparer genome 1D vs 2D
