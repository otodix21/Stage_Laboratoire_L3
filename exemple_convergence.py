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
    return np.linalg.norm(Z1 - Z2) / np.linalg.norm(Z1)


#Géométrie et fréquences
geometry = [[0, 0.2, 5e-3, 5e-3, 'linear' ]]
freq = np.arange(200,2001,1)


#Code de référence
result = ImpedanceComputation(freq, geometry, l_ele=.05, order=6, interp=True)

result.plot_instrument_geometry()
result.plot_impedance()
result.plot_ac_field(var='pressure')
result.discretization_infos()

Z = result.impedance


#%% Erreur en fonction de l'ordre

print("\nCalcul de l'étude de convergence")

ref_ordre = ImpedanceComputation(freq, geometry, l_ele=0.005, order=8, interp=True)
Z_ref_ordre = ref_ordre.impedance

ordres = [1, 2, 3, 4, 5, 6]  # On restreint aux ordres principaux
erreurs_ordres = []

for ord_val in ordres:
    res = ImpedanceComputation(freq, geometry, l_ele=0.02, order=ord_val, interp=True)
    erreurs_ordres.append(norm_l2(Z_ref_ordre, res.impedance))
    
plt.figure()
plt.semilogy(ordres, erreurs_ordres, 'o-', color='black')
plt.xlabel("Finite elements order")
plt.ylabel(r"$\frac{\|Z_{FEM} - Z_{TMM}\|}{\|Z_{TMM}\|}$")
plt.title("Convergence en fonction de l'ordre")
plt.grid(True, which="both", ls="--")

#%% Erreur en fonction de la taille de maille

print("\nCalcul de la convergence en fonction de la taille de maille...")

ref_maille = ImpedanceComputation(freq, geometry, l_ele=0.002, order=6, interp=True)
Z_ref_maille = ref_maille.impedance

# On réduit à 4 tailles de mailles clés pour que ça aille très vite
liste_l_ele = [0.05, 0.02, 0.01, 0.005]
ordres_a_tester = [2, 4]  # On teste l'ordre 2 et l'ordre 4

plt.figure()
for ord_val in ordres_a_tester:
    errs = []
    for l in liste_l_ele:
        res = ImpedanceComputation(freq, geometry, l_ele=l, order=ord_val, interp=True)
        errs.append(norm_l2(Z_ref_maille, res.impedance))
    plt.loglog(liste_l_ele, errs, 'o-', label=f'order {ord_val}')
    

plt.xlabel("Target Element Size (TES)")
plt.ylabel(r"$\frac{\|Z_{FEM} - Z_{TMM}\|}{\|Z_{TMM}\|}$")
plt.title("Convergence en fonction de la taille de maille")
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()
