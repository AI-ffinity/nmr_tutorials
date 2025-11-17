# 13C-edited 3D NOESY

Execute the following steps in the specified order:

1. `kr` for restricted peak picking using 13C-HSQC to pick peaks in 13C 3D NOESY. Assuming that the 13C-HSQC contains 
grid lattice created with `Ng` plugin, use all its peaks and set the following tolerances:
w1 (1H): 20, w2 (13C): 0.075, w3 (1H): 0.0075
Then click "Pick peaks".
2. Do a second round of restricted peak picking, this time using all 13C-HSQC peaks but setting the following tolerances:
w1 (1H): 0.0075, w2 (13C): 100, w3 (1H): 20
Then click "Select peaks".
3. Got to the 13C 3D NOESY, hit `nt` and name these peaks "aliphatic H".
4. Now go to the restricted peak picking window and set the "Using peaks in" to the 15N-HSQC. Set the following tolerances:
w1 (1H): 0.005, w2 (13C): 100, w3 (1H): 20
Then click "Select peaks".
5. Got to the 13C 3D NOESY, hit `nt` and name these peaks "amidic H".
6. Still in the 13C 3D NOESY hit `lt`, sort by "Note" and select all the peaks that have an empty "Note" field. Then 
switch to the 13C 3D NOESY window and click the keyboard's "Delete" button.


# 15N-edited 3D NOESY

Execute the following steps in the specified order:

1. `kr` for restricted peak picking using 15N-HSQC to pick peaks in 15N 3D NOESY. Assuming that the 15N-HSQC contains 
grid lattice created with `Ng` plugin, use all its peaks and set the following tolerances:
w1 (1H): 20, w2 (15N): 0.05, w3 (1H): 0.005
Then click "Pick peaks".
2. Do a second round of restricted peak picking, this time using all 15N-HSQC peaks but setting the following tolerances:
w1 (1H): 0.005, w2 (15N): 100, w3 (1H): 20
Then click "Select peaks".
3. Got to the 15N 3D NOESY, hit `nt` and name these peaks "amidic H".
4. Now go to the restricted peak picking window and set the "Using peaks in" to the 13C-HSQC. Set the following tolerances:
w1 (1H): 0.0075, w2 (15N): 100, w3 (1H): 20
Then click "Select peaks".
5. Got to the 15N 3D NOESY, hit `nt` and name these peaks "aliphatic H".
6. Still in the 13C 3D NOESY hit `lt`, sort by "Note" and select all the peaks that have an empty "Note" field. Then 
switch to the 13C 3D NOESY window and click the keyboard's "Delete" button.