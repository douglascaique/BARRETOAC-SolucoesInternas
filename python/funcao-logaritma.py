import numpy as np
import matplotlib.pyplot as plt

# Coeficientes calculados
a = 567.69
c = -538.5

# Função
def f(x):
    return a * np.log10(x) + c

# Gerar x e y: começando em x=20, aumentando 10 a cada ponto
x_vals = np.arange(20, 500 + 1, 10)  # até x=150 (ajustável)
y_vals = f(x_vals)

# Plotagem
plt.figure(figsize=(12, 6))
plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue',
         label=fr'$f(x) = {a:.2f} \cdot \log_{{10}}(x) {c:+.2f}$')
plt.title('Função logarítmica: f(x) cresce 100 a cada 10 unidades em x')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
