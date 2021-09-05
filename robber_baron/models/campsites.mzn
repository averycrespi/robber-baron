% MiniZinc model for the Campsites problem

include "grid.mzn";

int: num_rows;
int: num_cols;
set of int: R = 1..num_rows;
set of int: C = 1..num_cols;
constraint assert(num_rows >= 5 /\ num_cols >= 10, "board is too small");

array[R] of int: num_tents_in_row; % Row i contains num_tents_in_row[i] tents
array[C] of int: num_tents_in_col; % Column j contains num_tents_in_col[j] tents
constraint assert(sum(num_tents_in_row) == sum(num_tents_in_col), "inconsistent number of tents");

int: num_trees;
set of int: T = 1..num_trees;
array[T] of int: tree_rows;     % Row indices of trees
array[T] of int: tree_cols;     % Column indices of trees
array[R,C] of var bool: trees;  % Row i, column j contains a tree iff trees[i][j]
constraint forall(i in R, j in C) (trees[i,j] <-> exists(k in T) (tree_rows[k] = i /\ tree_cols[k] = j));

array[R,C] of var bool: tents; % Row i, column j contains a tent iff tents[i][j]

% Every tree on the board is associated with _one_ tent, which is always horizontally or vertically adjacent to it
constraint forall(i in R, j in C) (trees[i,j] -> exists(i2 in R, j2 in C) (tents[i2,j2] /\ cardinally_adjacent(i, j, i2, j2)));
constraint forall(i in R, j in C) (tents[i,j] -> exists(i2 in R, j2 in C) (trees[i2,j2] /\ cardinally_adjacent(i, j, i2, j2)));

% No tent can be horizontally, vertically or diagonally adjacent to another tent
constraint forall(i in R, j in C) (tents[i,j] -> not exists(i2 in R, j2 in C) (tents[i2,j2] /\ adjacent(i, j, i2, j2)));

% The numbers for each column/row indicate the total number of tents within that column/row
constraint forall(i in R) (sum(tents[i,..]) == num_tents_in_row[i]);
constraint forall(j in C) (sum(tents[..,j]) == num_tents_in_col[j]);

% The final solution will have `num_tents` tents
constraint sum(tents) == sum(num_tents_in_row);

solve satisfy;
