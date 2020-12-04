from launch_loads import bucklingCheck
from materialselection import MatSelec
from mass_calculators import massTankAndProp
import numpy as np
import math

print("Hello project WP5!")

materials = ['Ti-6Al-4V','Ti-3Al-2.5V','Al 2219-T851']
yieldstrength = [880e6, 500e6, 352e6]
density = [4430, 4480, 2840]
V = [0.12/2, 0.15/2]
fo = 2
ok = 0

while fo != 0 and fo != 1:
    fo = int(input("Do you want to calculate my ass for fuel (0) or oxizidizer (1)?: "))
    if fo != 0 and fo != 1:
        print("Your input is wrong! Only accepted values are 0 (fuel) or 1 (oxidizer). Try again.")
    
maxR = (3 * V[fo] / 4 / math.pi)**(1/3)

for R in np.arange(0.001, maxR, 1e-3):
    L = 1 / (math.pi * R * R) * (V[fo] - 4/3*math.pi*R*R*R)

    at1, at2 = MatSelec(R, yieldstrength)

    MLst = []
    for i in range(len(materials)):
        totMass = massTankAndProp(i, L, R, at1[i], at2[i], fo)
        MLst.append(totMass)
    
    lowestMass = min(MLst)
    im = MLst.index(min(MLst))
    t1 = at1[im]
    t2 = at2[im]
    material = materials[im]
    
    diff_col, diff_shell = bucklingCheck(im, L, R, t1, lowestMass)

    if diff_col > 0 and diff_shell > 0 and L > 0:
        print(f"Option passes with material = {material}, L = {L:.4f}, R = {R:.4f}, t1 = {t1:.4f}, t2 = {t2:.4f}, mass = {lowestMass:.4f}")
        ok = 1
    else:
        print(f"diff_col = {diff_col}, diff_shell = {diff_shell}")
        continue

if ok == 0:
    print("No suitable value found.")
