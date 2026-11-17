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


ordres = [1, 2, 3, 4, 5, 6]  # On restreint aux ordres principaux
mailles_a_tester = [0.05, 0.02, 0.01]

plt.figure()

for l_fixe in mailles_a_tester:
    erreurs_ordres = []
    
    for ord_val in ordres:
        res = ImpedanceComputation(freq, geometry, l_ele=l_fixe, order=ord_val, interp=True)
        res_suivant = ImpedanceComputation(freq, geometry, l_ele=l_fixe, order=ord_val + 1, interp=True)
        erreurs_ordres.append(norm_l2(res_suivant.impedance, res.impedance))
    plt.semilogy(ordres, erreurs_ordres, 'o-', label=f'l_ele = {l_fixe} m')


# Affichage de l'erreur limite machine (10^-16)
plt.axhline(1e-16, color='red', linestyle='--', label='Erreur limite ($10^{-16}$)')
plt.ylim(bottom=1e-17)

    
plt.xlabel("Finite elements order (p)")
plt.ylabel(r"$\frac{\|Z_{p+1} - Z_{p}\|}{\|Z_{p+1}\|}$")
plt.title("Convergence en fonction de l'ordre")
plt.grid(True, which="both", ls="--")
plt.legend()


#%% Erreur en fonction de la taille de maille

print("\nCalcul de la convergence en fonction de la taille de maille...")


# On réduit à 4 tailles de mailles clés pour que ça aille très vite
liste_l_ele = [0.05, 0.02, 0.01, 0.005]
ordres_a_tester = [2, 4]  # On teste l'ordre 2 et l'ordre 4

plt.figure()

for ord_val in ordres_a_tester:
    ref_maille = ImpedanceComputation(freq, geometry, l_ele=0.002, order=ord_val, interp=True)
    Z_ref_maille = ref_maille.impedance
    
    errs = []
    
    for l in liste_l_ele:
        res = ImpedanceComputation(freq, geometry, l_ele=l, order=ord_val, interp=True)
        errs.append(norm_l2(Z_ref_maille, res.impedance))
    plt.loglog(liste_l_ele, errs, 'o-', label=f'order {ord_val}')
    

# Affichage de l'erreur limite machine (10^-16)
plt.axhline(1e-16, color='red', linestyle='--', label='Erreur limite ($10^{-16}$)')
plt.ylim(bottom=1e-17)


plt.xlabel("Target Element Size (TES)")
plt.ylabel(r"$\frac{\|Z_{FEM} - Z_{ref}\|}{\|Z_{ref}\|}$")
plt.title("Convergence en fonction de la taille de maille")
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()

