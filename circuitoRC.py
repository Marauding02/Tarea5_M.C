import matplotlib.pyplot as plt
import pylab
import numpy as np 

#Carga datos y guarda los valores 
daticos = np.loadtxt("CircuitoRC.txt")
t_obs = daticos[:,0]
q_obs = daticos[:,1]

    #Scatter inicial, ver la forma de los datos
#plt.scatter(t_obs,q_obs)


#Definición función likelyhood
def verosimilitud(y_obs, y_model):
    chi_cuadrado = (1.0/2.0)*sum((y_obs-y_model)/1000)**2
    return np.exp(-chi_cuadrado)


#TAU = 1 / R*C
#Q_MAX = VS * C

def modelo(t, Q_MAX , TAU):
    return Q_MAX * ( 1 - np.exp((-t * TAU )))

#Inicializa listas para las caminatas
TAU_walk = np.empty((0)) 
Q_MAX_walk = np.empty((0))
l_walk = np.empty((0))

#Tras rezalizar un sinnúmero de intentos, se encontró que el valor aproximado de Q Y Tau , estaba dentro de 98 y 0.01 aproximadamente .

guessTAU = 0.01
guessQ = 98

TAU_walk = np.append(TAU_walk, guessTAU)
Q_MAX_walk = np.append(Q_MAX_walk,guessQ)

Q_ini = modelo(t_obs, Q_MAX_walk[0], TAU_walk[0])
l_walk = np.append(l_walk, verosimilitud(q_obs, Q_ini))

itera = 8000 
for i in range(itera):
    
    sigma = 0.01
    TAU_prima = np.random.normal(TAU_walk[i], sigma) 
    Q_MAX_prima= np.random.normal(Q_MAX_walk[i], sigma)

    Q_ini = modelo(t_obs,  Q_MAX_walk[i], TAU_walk[i])
    Q_prima = modelo(t_obs, Q_MAX_prima, TAU_prima)
    
    l_prima = verosimilitud(q_obs, Q_prima)
    l_ini = verosimilitud(q_obs, Q_ini)

    alpha = l_prima/l_ini
    
    if(alpha>=1.0):
        TAU_walk  = np.append(TAU_walk,TAU_prima)
        Q_MAX_walk  = np.append(Q_MAX_walk,Q_MAX_prima)
        l_walk = np.append(l_walk, l_prima)
    else:
        beta = np.random.random()
        if(beta<=alpha):
            TAU_walk  = np.append(TAU_walk,TAU_prima)
            Q_MAX_walk  = np.append(Q_MAX_walk,Q_MAX_prima)
            l_walk = np.append(l_walk, l_prima)
        else:
            TAU_walk = np.append(TAU_walk,TAU_walk[i])
            Q_MAX_walk = np.append(Q_MAX_walk,Q_MAX_walk[i])
            l_walk = np.append(l_walk, l_ini)

            #MOSH DE DATOS
#plt.scatter(Q_MAX_walk,TAU_walk)
#plt.show()


#Calculo los mejores valores de TAU Y Q , según la caminata
max_verosimilitud = np.argmax(l_walk)
best_TAU = TAU_walk[max_verosimilitud]
best_Q_MAX = Q_MAX_walk[max_verosimilitud]

#Función de RC , con los datos obtenidos
best_Q = modelo(t_obs, best_Q_MAX, best_TAU)


#TAU = 1 / R*C
#Q_MAX = VS * C
Vs = 10

#Calcula el valor de R y C con los valores obtenidos 
C= best_Q_MAX / Vs
print("Best value for C = " , C , "F")

R = 1 / (best_TAU * C ) 
print("Best value for R = " , R , "Ohm")


#Histogramas de R y C 
R_hist = np.empty((0))
R_hist = 1 / (TAU_walk * C )  

C_hist = np.empty((0))
C_hist = (Q_MAX_walk / Vs)

hist1 = plt.figure()
plt.hist(C_hist, bins='auto', edgecolor='black', linewidth=1.2 ,normed=True)  
plt.title("Histogram Valores de C ")
plt.ylabel(r'',fontsize=16)
plt.xlabel(r'C (F)',fontsize=16,  color='Black')
hist1.savefig('Hist_C.png')

hist2 = plt.figure()
plt.hist(R_hist, bins='auto', edgecolor='black', linewidth=1.2, normed=True)  
plt.title("Histograma Valores de R")
plt.ylabel(r'',fontsize=16)
plt.xlabel(r'R ( Ohm)',fontsize=16,  color='Black')
hist2.savefig('Hist_R.png')

#Figura Best fit
fig1 = plt.figure()
plt.rc('font', family='serif')
fig1.suptitle(r'Best fit de los datos , Circuito RC ', fontsize=16,color='Black')
#Rotulación de ejes de la gráfica y rejilla
plt.text(200, 60 , r'$ C \approx 9.75$ F', fontsize=12)
plt.text(200, 50, r'$R \approx 5.46 $ Ohm ',fontsize=12)
plt.rc('font', family='serif')
plt.xlabel(r'Tiempo',fontsize=16,  color='Black')
plt.rc('font', family='serif')
plt.ylabel(r'Carga (Q)',fontsize=16)
plt.grid(True)
#Plot de los datos
s=121
EL_UNO=plt.scatter(t_obs,q_obs,color='b', s=s/2, alpha=.4,label='Datos iniciales')
EL_DOS=plt.plot(t_obs, best_Q, color='r',label='Mejor Fit segun R y C ')
pylab.legend(loc='upper left')
#Almacena la gráfica en un pdf dentro del directorio
fig1.savefig('best_fit.png')