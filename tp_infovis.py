import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

# print(plt.style.available)
plt.style.use('seaborn-dark') ##ggplot queda bien

df = pd.read_csv('data/pedidosya.csv')
df['fecha'] = [datetime.strptime(x, '%Y-%m-%d') for x in df['fecha']] # convertimos fechas string a datetime
font = {'fontname':'Microsoft Tai Le'}

fig,(ax1,ax2) = plt.subplots(nrows=2,ncols=1)


## ax1 ################################################################################################################################################
# comidas = df['comida'].unique()
# print(comidas)
# slices = []
# slices= [int(df[df['comida']==comida].describe().loc['count']['monto']) for comida in comidas]
# print(slices)

comidas = ['Green Eat','Empanadas','Cerveza','Fast food']
cant = [12, 25, 61, 10]
colores = ['#1dd1a1', '#00d2d3','#576574','#54a0ff']
ax1.pie(cant, labels = comidas, colors = colores, autopct = '%1.1f%%', startangle = -28.5)
ax1.set_title('Proporción de pedidos por tipo de comida', **font)

## ax2 ################################################################################################################################################


filtr_cerveza = df['comida'] == 'cerveza'
filtr_empanadas = df['comida'] == 'empanadas'
filtr_ensalada = (df['comida'] == 'ensalada') | (df['comida'] == 'sushi')
filtr_fast_food = (df['comida'] == 'mcdonalds') | (df['comida'] == 'burger king')

filters = [filtr_cerveza,filtr_empanadas,filtr_ensalada,filtr_fast_food]
colores = ['#576574','#00d2d3','#1dd1a1','#54a0ff']
labels = ['Cerveza','Empanadas','Green Eat','Fast Food']

for i in range(4):
    ax2.plot_date(df.loc[filters[i]]['fecha'], df.loc[filters[i]]['monto'], marker = 'o', color = colores[i], label = labels[i])

ax2.set_ylabel('Monto en pesos ($/pedido)', **font)

ax2.axvline(x = 18332, linestyle = '--', color = 'k', label = 'Inicio de ASPO')
# ax2.axhline(y=381.83, label = 'Media ($)', linestyle = ':', color = 'k') # ensucia demasiado la cronología
ax2.set_title('Cronología de pedidos', **font)
ax2.legend()
ax2.grid(True)

## ax3 ################################################################################################################################################
ax3 = fig.add_subplot(231)

comidas = ['ensalada', 'mcdonalds','empanadas', 'cerveza']
comidaslimpio = ['Green Eat','Fast food','Empanadas','Cerveza']
montos_por_comida = []
grupos_com = df.groupby('comida')
montos_por_comida = [grupos_com.get_group(x).sum()['monto'] for x in comidas]
montos_por_comida[1]+= grupos_com.get_group('burger king').sum()['monto']
# montos_por_comida[1]+= grupos_com.get_group('burger king').sum()['monto']
montos_por_comida[0] += grupos_com.get_group('sushi').sum()['monto']
montos_por_comida[0] += grupos_com.get_group('helado').sum()['monto']
montos_por_comida = [x/1000 for x in montos_por_comida]
print(montos_por_comida)
colores = ['#1dd1a1','#54a0ff', '#00d2d3','#576574']

ax3.bar(comidas,montos_por_comida, color = colores, edgecolor = 'k')

plt.xticks(ticks=comidas, labels=comidaslimpio)

ax3.set_ylabel('Pesos (miles)', **font)
ax3.set_title('Gasto anual por tipo de comida', **font)

## ax4 ################################################################################################################################################
ax4 = fig.add_subplot(233)
comidas = ['empanadas','ensalada','cerveza','mcdonalds']
comidaslimpio = ['Empanadas','Green Eat','Cerveza','Fast food']
media_por_comida = [grupos_com.get_group(x).mean()['monto'] for x in comidas]
media_por_comida[3]+= grupos_com.get_group('burger king').mean()['monto']
media_por_comida[3]/=2
media_por_comida[1] += grupos_com.get_group('sushi').mean()['monto']
media_por_comida[1] += grupos_com.get_group('helado').mean()['monto']
media_por_comida[1] /=3
colores = ['#00d2d3','#1dd1a1','#576574','#54a0ff']

ax4.bar(comidas,media_por_comida, color = colores, edgecolor = 'k')

plt.xticks(ticks=comidas, labels=comidaslimpio)

ax4.set_ylabel('Pesos', **font)
ax4.set_title('Costo promedio de pedido por tipo de comida', **font)

plt.suptitle('Uso de pedidosYa durante el año', **font,fontsize=20)
plt.tight_layout()
plt.show()
