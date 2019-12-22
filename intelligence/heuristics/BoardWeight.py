
# A static table
class BoardStaticWeight:
    weightTable1 = [
        [200,    -100,    100,       8,      8,      8,      8,       100,      -100,     200],
        [-100,   -200,    -10,     -50,    -50,    -50,    -50,       -10,      -200,    -100],
        [100,     -10,    -50,      50,     25,     25,     50,       -50,       -10,     100],
        [50,      -50,     50,    -100,      0,      0,   -100,        50,       -50,      50],
        [50,      -50,     25,       0,      0,      0,      0,        25,       -50,      50],
        [50,      -50,     25,       0,      0,      0,      0,        25,       -50,      50],
        [50,      -50,     50,    -100,      0,      0,   -100,        50,       -50,      50],
        [100,     -10,    -50,      50,     25,     25,     50,       -50,       -10,     100],
        [-100,   -200,    -10,     -50,    -50,    -50,    -50,       -10,      -200,    -100],
        [200,    -100,    100,      50,     50,     50,     50,       100,      -100,     200],
    ]
    weightTable4 = [
        [200,    -100,    100,       8,      8,      8,      8,       100,      -100,     200],
        [-100,   -200,    100,     -50,    -50,    -50,    -50,       100,      -200,    -100],
        [100,     100,    150,      50,     25,     25,     50,       150,       100,     100],
        [50,      -50,     50,    -100,      0,      0,   -100,        50,       -50,      50],
        [50,      -50,     25,       0,      0,      0,      0,        25,       -50,      50],
        [50,      -50,     25,       0,      0,      0,      0,        25,       -50,      50],
        [50,      -50,     50,    -100,      0,      0,   -100,        50,       -50,      50],
        [100,     100,    150,      50,     25,     25,     50,       150,       100,     100],
        [-100,   -200,    100,     -50,    -50,    -50,    -50,       100,      -200,    -100],
        [200,    -100,    100,      50,     50,     50,     50,       100,      -100,     200],
    ]
    weightTable3 = [
        [200,    -100,    100,     -50,    -25,    -25,    -50,       100,      -100,     200],
        [-100,   -200,    100,     -50,     25,     25,    -50,       100,      -200,    -100],
        [100,     100,    150,     -50,     25,     25,    -50,       150,       100,     100],
        [-50,     -50,    -50,     -50,      0,      0,    -50,       -50,       -50,     -50],
        [-25,       25,     25,       0,      0,      0,      0,        25,        25,    -25],
        [-25,       25,     25,       0,      0,      0,      0,        25,        25,    -25],
        [-50,     -50,   -50,      -50,      0,      0,    -50,       -50,       -50,     -50],
        [100,     100,    150,     -50,     25,     25,    -50,       150,       100,     100],
        [-100,   -200,    100,     -50,     25,     25,    -50,       100,      -200,    -100],
        [200,    -100,    100,     -50,    -25,    -25,    -50,       100,      -100,     200],
    ]
    weightTable5 = [
        [200,    -100,    100,     -50,    -25,    -25,    -50,       100,      -100,     200],
        [-100,   -200,    100,     -50,     25,     25,    -50,       100,      -200,    -100],
        [100,     100,    150,     -50,     25,     25,    -50,       150,       100,     100],
        [-50,     -50,    -50,     -50,      0,      0,    -50,       -50,       -50,     -50],
        [-25,       25,     25,       0,      10,      10,      0,        25,        25,    -25],
        [-25,       25,     25,       0,      10,      10,      0,        25,        25,    -25],
        [-50,     -50,   -50,      -50,      0,      0,    -50,       -50,       -50,     -50],
        [100,     100,    150,     -50,     25,     25,    -50,       150,       100,     100],
        [-100,   -200,    100,     -50,     25,     25,    -50,       100,      -200,    -100],
        [200,    -100,    100,     -50,    -25,    -25,    -50,       100,      -100,     200],
    ]


    weightTable2 = [
        [200 , -100, 100,  50,  50,  50,  50,   100,  -100,   200],
        [-100, -100, 0, 0, 0, 0, 0,   0,  -100,  -100],
        [100 ,  0, 100,  50,  25,  25,  50,   100,   0,   100],
        [50  ,  0,  50, -25,  10,  10, -25,    50,   0,    50],
        [50  ,  0,  25,  10,  25,  25,  10,    25,   0,    50],
        [50  ,  0,  25,  10,  25,  25,  10,    25,   0,    50],
        [50  ,  0,  50, -25,  10,  10, -25,    50,   0,    50],
        [100 ,  0, 100,  50,  25,  25,  50,   100,    0,   100],
        [-100, -100, 0, 0, 0, 0, 0,   0,  -100,  -100],
        [200 , -100, 100,  50,  50,  50,  50,   100,  -100,   200],
        ]


    weightTableStable = [
        [ 9,  -5, -1,  -1,  -1,  -1,  -1,  -1,   -5,   9],
        [-5, -10,  1,   1,   1,   1,   1,   1,  -10,  -5],
        [ 1,   1,  1,   1,   1,   1,   1,   1,    1,   1],
        [ 1,   1,  1,   1,   1,   1,   1,   1,    1,   1],
        [ 1,   1,  1,   1,   1,   1,   1,   1,    1,   1],
        [ 1,   1,  1,   1,   1,   1,   1,   1,    1,   1],
        [ 1,   1,  1,   1,   1,   1,   1,   1,    1,   1],
        [ 1,   1,  1,   1,   1,   1,   1,   1,    1,   1],
        [-5, -10,  1,   1,   1,   1,   1,   1,  -10,  -5],
        [ 9,  -5, -1,  -1,  -1,  -1,  -1,  -1,   -5,   9],
        ]
    
    


    weightPreventKillerMove = [
        [ 0,  -500, 0,0,0,0,0,0,   -500,   0],
        [-500, -1000,  5,   -50,   -50,   -50,   -50,   5,  -1000,  -500],
        [0,5,0,0,0,0,0,0,5,0],
        [0,-50,0,0,0,0,0,0,-50,0],
        [0,-50,0,0,0,0,0,0,-50,0],
        [0,-50,0,0,0,0,0,0,-50,0],
        [0,-50,0,0,0,0,0,0,-50,0],
        [0,5,0,0,0,0,0,0,5,0],
        [-500, -1000,  5,   -50,   -50,   -50,   -50,   5,  -1000,  -500],
        [ 0,  -500, 0,0,0,0,0,0,   -500,   0],
        ]
