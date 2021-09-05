% Utilities for working with 2D grids
% Assumptions: row-major order; i denotes row; j denotes column

% Returns true iff (i,j) is cardinally adjacent to (i2,j2)
predicate cardinally_adjacent(int: i, int: j, int: i2, int: j2) = (
        (i-1 == i2 /\ j == j2)
    \/  (i+1 == i2 /\ j == j2)
    \/  (j-1 == j2 /\ i == i2)
    \/  (j+1 == j2 /\ i == i2)
);

% Returns true iff (i,j) is diagonally adjacent to (i2,j2)
predicate diagonally_adjacent(int: i, int: j, int: i2, int: j2) = (
        (i-1 == i2 /\ j-1 == j2)
    \/  (i-1 == i2 /\ j+1 == j2)
    \/  (i+1 == i2 /\ j-1 == j2)
    \/  (i+1 == i2 /\ j+1 == j2)
);

% Returns true iff (i,j) is adjacent to (i2,j2)
predicate adjacent(int: i, int: j, int: i2, int: j2) = (
    cardinally_adjacent(i, j, i2, j2) \/ diagonally_adjacent(i, j, i2, j2)
);
