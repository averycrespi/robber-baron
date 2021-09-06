% MiniZinc model for the Numbergrid problem

int: grid_size;
set of int: N = 1..grid_size;
constraint assert(grid_size >= 5, "grid is too small");

int: num_clues;
set of int: C = 1..num_clues;
set of int: V = 0..grid_size;   % Zero denotes an empty clue, which is used for padding to a constant length
array[N,C] of V: row_clues;     % The clues of row i are row_clues[i,..]
array[N,C] of V: col_clues;     % The clues of column j are col_clues[j,..]

% The line for row i, clue c starts at column row_starts[i,c] and ends at column row_ends[i,c] (inclusive)
% The line for column j, clue c starts at row col_starts[j,c] and ends at row column_ends[j,c] (inclusive)
% We use `int` instead of `N` because the empty clue starts and ends may go out-of-bounds
array[N,C] of var int: row_starts;
array[N,C] of var int: row_ends;
array[N,C] of var int: col_starts;
array[N,C] of var int: col_ends;

% For each row and column, the line starts must be sorted in strictly ascending order
constraint forall(i in N, c in C) ((c < num_clues) -> (row_starts[i,c] < row_starts[i,c+1]));
constraint forall(j in N, c in C) ((c < num_clues) -> (col_starts[j,c] < col_starts[j,c+1]));

% For each row and column, the line ends must be sorted in strictly ascending order
constraint forall(i in N, c in C) ((c < num_clues) -> (row_ends[i,c] < row_ends[i,c+1]));
constraint forall(j in N, c in C) ((c < num_clues) -> (col_ends[j,c] < col_ends[j,c+1]));

% If clue c is non-empty, its lines must lie on the grid
constraint forall(i in N, c in C) ((row_clues[i,c] != 0) -> (row_starts[i,c] in N /\ row_ends[i,c] in N));
constraint forall(j in N, c in C) ((col_clues[j,c] != 0) -> (col_starts[j,c] in N /\ col_ends[j,c] in N));

% If clue c is empty, its lines must lie off the grid
% This isn't strictly necessary, but helps to get the empty clue lines out of the way
constraint forall(i in N, c in C) ((row_clues[i,c] = 0) -> not (row_starts[i,c] in N \/ row_ends[i,c] in N));
constraint forall(j in N, c in C) ((col_clues[j,c] = 0) -> not (col_starts[j,c] in N \/ col_ends[j,c] in N));

% If clue c is non-empty, its lines must have a length equal to the distance between start and end
constraint forall(i in N, c in C) ((row_clues[i,c] != 0) -> (row_starts[i,c] + row_clues[i,c] - 1 = row_ends[i,c]));
constraint forall(j in N, c in C) ((col_clues[j,c] != 0) -> (col_starts[j,c] + col_clues[j,c] - 1 = col_ends[j,c]));

% Every consecutive pair of lines must have a gap of at least one cell between them
constraint forall(i in N, c in C) ((c < num_clues) -> (row_ends[i,c] + 1 < row_starts[i,c+1]));
constraint forall(j in N, c in C) ((c < num_clues) -> (col_ends[j,c] + 1 < col_starts[j,c+1]));

array[N,N] of var bool: grid;   % Row i, column j is black iff grid[i,j]

% Iff a cell lies within a row line and a column line, then it is black
constraint forall(i, j in N ) (
    grid[i,j] <-> (exists(ci in C, cj in C) (row_starts[i,ci] <= j /\ j <= row_ends[i,ci] /\ col_starts[j,cj] <= i /\ i <= col_ends[j,cj]))
);

% The number of black cells in each row and column must equal the sum of the given clues
constraint forall(i in N) (sum(grid[i,..]) = sum(row_clues[i,..]));
constraint forall(j in N) (sum(grid[..,j]) = sum(col_clues[j,..]));

solve satisfy;
