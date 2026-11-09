#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage en Laboratoire

@author: Alexandre
"""
#%% Banque d'outils
import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation


#%% Code

def norm_l2(Z1, Z2):
    norm_Z1 = np.sum(Z1**2)
    err = np.sum((Z1-Z2)**2)/norm_Z1
    return err

# geometry = [[0, .2, 5e-3, 7e-3, 'linear'],
#             [.2, .3, 9e-3, 9e-3, 'linear'],
#             [.3,.45,9e-3,90e-3, 'bessel', .75]]


#Tuyau conique (géométrie et fréquences)
geometry = [[0, 0.2, 5e-3, 5e-3, 'linear' ]]
freq = np.arange(200,2001,1)


#Code de référence
result = ImpedanceComputation(freq, geometry, l_ele=.05, order=6, interp=True)

result.plot_instrument_geometry()
result.plot_impedance()
result.plot_ac_field(var='pressure')

Z = result.impedance
result.discretization_infos()

# l_ele_dict = {'bore0':0.1, 'bore1':0.1, 'bore2':0.02}
# # order_dict = {'bore0':4, 'bore1':8, 'bore2':6}

# l_ele_dict = {'bore0':0.1, 'bore1':0.1, 'bore2':[.05,.05,.02,.02,.01]}
# order_dict = {'bore0':4, 'bore1':8, 'bore2':[4,4,6,6,8]}


#Etude de convergence
print("\n--- Calcul de l'étude de convergence ---")
ref_result = ImpedanceComputation(freq, geometry, l_ele=0.002, order=8, interp=True)
Z_ref = ref_result.impedance


#Différentes tailles de mailles
liste_l_ele = [0.05, 0.02, 0.01, 0.005]
erreurs_ordre_2 = []
erreurs_ordre_4 = []


for l in liste_l_ele:
    #Test avec l'ordre 2
    res2 = ImpedanceComputation(freq, geometry, l_ele=l, order=2, interp=True)
    erreurs_ordre_2.append(norm_l2(Z_ref, res2.impedance))
    
    #Test avec l'odre 4
    res4 = ImpedanceComputation(freq, geometry, l_ele=l, order=4, interp=True)
    erreurs_ordre_4.append(norm_l2(Z_ref, res4.impedance))
    

#Figure de convergence
plt.figure()
plt.loglog(liste_l_ele, erreurs_ordre_2, 'o-', label='Ordre 2')
plt.loglog(liste_l_ele, erreurs_ordre_4, 's-', label='Ordre 4')
plt.xlabel("Taille de la maille (l_ele)")
plt.ylabel("Erreur L2 par rapport à la référence")
plt.title("Courbe de convergence")
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()


