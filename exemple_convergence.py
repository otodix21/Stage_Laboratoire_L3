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


# Estimation simple du nombre de ddl en 1D sur une longueur L
def estimer_ddl(L, l_ele, ordre):
    nb_elements = max(1, round(L / l_ele))
    return nb_elements * ordre + 1


#Géométrie et fréquences
L_tube = 0.2
geometry = [[0, L_tube, 5e-3, 5e-3, 'linear' ]]
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

ordres = [1, 2, 3, 4, 5, 6]
l_ele_ordre = 0.01


imp_par_ordre = [
    ImpedanceComputation(freq, geometry, l_ele=l_ele_ordre, order=ord_val, interp=True).impedance
    for ord_val in ordres
]


errs_ordre = []
paires_ordres = []


for i in range(len(ordres) - 1):
    errs_ordre.append(norm_l2(imp_par_ordre[i + 1], imp_par_ordre[i]))
    paires_ordres.append(f"{ordres[i]}->{ordres[i + 1]}")


plt.figure()

plt.semilogy(paires_ordres, errs_ordre, 'o-')
plt.axhline(1e-16, color='red', linestyle='--', label='Erreur limite ($10^{-16}$)')
plt.ylim(bottom=1e-17)

plt.xlabel("Transition d'ordre d'interpolation")
plt.ylabel(r"$\frac{\|Z_{n+1} - Z_n\|}{\|Z_{n+1}\|}$")
plt.title("Convergence en ordre")
plt.grid(True, which="both", ls="--")
plt.legend()


#%% Erreur en fonction de la taille de maille

print("\nCalcul de la convergence en fonction de la taille de maille")


# On réduit à 4 tailles de mailles clés pour que ça aille très vite
liste_l_ele = [0.05, 0.02, 0.01, 0.005]
ordres_a_tester = [2, 4]  # On teste l'ordre 2 et l'ordre 4

resultats_ddl = {}


plt.figure()

for ord_val in ordres_a_tester:
    ref_maille = ImpedanceComputation(freq, geometry, l_ele=0.002, order=ord_val, interp=True)
    Z_ref_maille = ref_maille.impedance
    
    errs = []
    liste_ddl = []
    
    for l in liste_l_ele:
        res = ImpedanceComputation(freq, geometry, l_ele=l, order=ord_val, interp=True)
        errs.append(norm_l2(Z_ref_maille, res.impedance))
        liste_ddl.append(estimer_ddl(L_tube, l, ord_val))
    
    resultats_ddl[ord_val] = (liste_ddl, errs)
    plt.loglog(liste_l_ele, errs, 'o-', label=f'order {ord_val}')
    

# Affichage de l'erreur limite machine (10^-16)
plt.axhline(1e-16, color='red', linestyle='--', label='Erreur limite ($10^{-16}$)')
plt.ylim(bottom=1e-17)


plt.xlabel("Target Element Size (TES)")
plt.ylabel(r"$\frac{\|Z_{FEM} - Z_{ref}\|}{\|Z_{ref}\|}$")
plt.title("Convergence en fonction de la taille de maille")
plt.grid(True, which="both", ls="--")
plt.legend()



#%% Suivi de l'erreur en fonction des degrés de liberté (ddl)

print("\nTracé de l'erreur en fonction des ddl")

plt.figure()

for ord_val, (liste_ddl, errs_ddl) in resultats_ddl.items():
    plt.loglog(liste_ddl, errs_ddl, 'o-', label=f'order {ord_val}')

plt.axhline(1e-16, color='red', linestyle='--', label='Erreur limite ($10^{-16}$)')
plt.ylim(bottom=1e-17)

plt.xlabel("Nombre estimé de degrés de liberté (ddl)")
plt.ylabel(r"$\frac{\|Z_{FEM} - Z_{ref}\|}{\|Z_{ref}\|}$")
plt.title("Précision en fonction du coût (ddl)")
plt.grid(True, which="both", ls="--")
plt.legend()



#%% Raffinement du maillage

print("\nPremier essai de raffinement du maillage")

ordre_raff = 3
z_ref_raff = ImpedanceComputation(freq, geometry, l_ele=0.002, order=ordre_raff, interp=True).impedance


# Comparaison avec un maillage de départ
z_base_raff = ImpedanceComputation(freq, geometry, l_ele=0.02, order=ordre_raff, interp=True).impedance
err_base_raff = norm_l2(z_ref_raff, z_base_raff)


# Découpage en deux tronçons avec une taille d'élément réduite
geom_cible = [
    [0, 0.1, 5e-3, 5e-3, 'linear'],
    [0.1, L_tube, 5e-3, 5e-3, 'linear']
]

z_cible = ImpedanceComputation(freq, geom_cible, l_ele=0.005, order=ordre_raff, interp=True).impedance
err_cible = norm_l2(z_ref_raff, z_cible)


plt.figure()

plt.bar(['Maillage initial (l_ele=0.02)', 'Essai raffiné (l_ele=0.005)'], [err_base_raff, err_cible])
plt.yscale('log')
plt.axhline(1e-16, color='red', linestyle='--', label='Erreur limite ($10^{-16}$)')
plt.ylim(bottom=1e-17)

plt.ylabel(r"$\frac{\|Z_{FEM} - Z_{ref}\|}{\|Z_{ref}\|}$")
plt.title("Premier essai de raffinement du maillage")
plt.grid(True, which="both", ls="--", axis='y')
plt.legend()







