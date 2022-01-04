# ProyectoDeGradoFisica - PhysicsGradeProject

Minimum Entropy code compilation: g++ MinimaEntropia.cpp -o MinimaEntropia

Minimum Entropy Usage example: ./MinimaEntropia OGLE-LMC-RRLYR-01981.dat 0.15 1.2 7 6 100000 4 1.2 1.02

Where:

0.15 1.2 are the range of periods in days in which the algorithm will search

7 6 dimensions of the Grid (7 columns, 6 rows)

100000 number of periods to search, in equally spaced frequencies. 

4 The greater this number, the greater the values of f and g of every individual period. 

1.2 max value of g allowed. All periods with g above this value will be ignored (will have high fixed entropy, so it will be ignored)

1.02 max value of f allowed. All periods with f above this value will be ignored (will have high fixed entropy, so it will be ignored)

Aliased periods of 0.5, 1, 1.5, 2... days have big values of g and f, so this values "filter" bad periods. 
