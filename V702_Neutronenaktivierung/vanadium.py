import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
from scipy.optimize import curve_fit

# leer los datos y preparar variables adecuadas
tv, Nv = np.genfromtxt('Vanadium.dat', unpack=True)
Nu = np.array([129.0, 143.0, 144.0, 136.0, 126.0, 158.0])

Nu_temp = Nu/10
Nu_cor = unp.uarray(Nu_temp, np.sqrt(Nu_temp))  # con temporiz corrigida
Nu_mean = np.mean(Nu_cor)
Nv_cor = unp.uarray(Nv, np.sqrt(Nv))
Nv_diff = Nv_cor - Nu_mean
Nv_diff_log = unp.log(Nv_diff)

def lnn(x, lamb, const):
    return - lamb * x + const

# realizar el curve fit
params1, cov1 = curve_fit(lnn, tv, unp.nominal_values(Nv_diff_log), sigma=unp.std_devs(Nv_diff_log))
errors1 = np.sqrt(np.diag(cov1))
lamb1 = unp.uarray(params1[0], errors1[0])
const1 = unp.uarray(params1[1], errors1[1])

# encontrar al tiempo de medio
Tv1 = np.log(2)/lamb1

# realizar otra vez el curve fit pero sin algunos datos
params2, cov2 = curve_fit(lnn, tv[:17], unp.nominal_values(Nv_diff_log[:17]), sigma=unp.std_devs(Nv_diff_log[:17]))
errors2 = np.sqrt(np.diag(cov2))
lamb2 = unp.uarray(params2[0], errors2[0])
const2 = unp.uarray(params2[1], errors2[1])

# tiempo de medio con mas mas
Tv2 = np.log(2)/lamb2

# muestrame los valores
print(f'lambda = {lamb1}, lambda(2) = {lamb2}')
print(f'const = {const1}, const(2) = {const2}')
print(f'Halbwertszeit = {Tv1}, Halbwertszeit(2) = {Tv2}')

# hacer el grafico
x = np.linspace(0, 1230)
x2 = np.linspace(0, 440)

plt.plot(x, lnn(x, *params1), 'b-', label="Lineare Regression")
plt.plot(x2, lnn(x2, *params2), 'r-', label="Eingeschränkter Wertebereich")
plt.errorbar(tv, unp.nominal_values(Nv_diff_log), yerr = unp.std_devs(Nv_diff_log), fmt='g.', label="Messwerte mit Fehlern")
plt.yscale('log')
plt.xlabel('t [s]')
plt.ylabel('ln(N)')
plt.legend()
plt.tight_layout()
plt.savefig('vanadium.pdf')

# hacer mierdos
np.savetxt(
    'build/tab/Vanadium_mess.txt',
    np.column_stack([tv, unp.nominal_values(Nv_cor), unp.std_devs(Nv_cor)]),
    fmt='%-20s',
    delimiter=' & ',
    header='t, Nv, Nverr',
)

np.savetxt(
    'build/tab/Vanadium_diff.txt',
    np.column_stack([tv, unp.nominal_values(Nv_diff), unp.std_devs(Nv_diff)]),
    fmt='%-20s',
    delimiter=' & ',
    header='t, Nv_diff, Nv_differr',
)

# datos teoreticos y diferencias procentuales

T_theo = 224
abw1 = (T_theo - Tv1)/100
abw2 = (T_theo - Tv2)/100

print(f'Abweichung von T1: {abw1}')
print(f'Abweichung von T2: {abw2}')