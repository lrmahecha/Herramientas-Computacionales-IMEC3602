import os
import numpy as np
import pandas as pd
import math

base_dir = os.path.join( '.','datos')
output_dir = os.path.join('.','output')

data_csv = os.path.join(base_dir,'cursos.csv')
cursos_df = pd.read_csv(data_csv)
data_csv = os.path.join(base_dir,'estados_academicos.csv')
estados_academicos = pd.read_csv(data_csv)

semestres = ['Tranferencia',201110,201120,201210,201220,201310,201320,201410,201420,
                201510,201520,201610,201620,201710,201720,201810]

cohorte = np.zeros(len(semestres))

grado = np.zeros(len(semestres))

desercion = np.zeros(len(semestres))

activo = np.zeros(len(semestres))

inactivo =np.zeros(len(semestres))

columnas = ['Semestre', 'Cohorte', 'Grado', 'Deserción', 'Activo', 'Inactivo']

ult_sem = semestres[-1]
ult_sem_des = semestres[-3]

codigos_imec = sorted(estados_academicos['CÓDIGO ESTUDIANTE'].unique())

conteo = 0

for estudiante in codigos_imec:

    conteo = conteo + 1

    semestres_est = sorted(
        estados_academicos[estados_academicos["CÓDIGO ESTUDIANTE"] == estudiante]
        ['PERIODO'].unique())

    num_sem = sum(p%10 == 0 for p in semestres_est)

    cohorte_est = estados_academicos[
                    estados_academicos["CÓDIGO ESTUDIANTE"] == estudiante]['COHORTE'].iloc[0]

    if math.isnan(cohorte_est):
        cohorte[0] += 1
    else:
        cohorte[semestres.index(cohorte_est)] += 1

    indice = (estados_academicos.index[
                (estados_academicos["CÓDIGO ESTUDIANTE"] == estudiante)
                & (estados_academicos["PERIODO"] == semestres_est[-1])][0])

    if(estados_academicos.get_value(indice, "GRADO")):
        if math.isnan(cohorte_est):
            grado[0] += 1
        else:
            grado[semestres.index(cohorte_est)] += 1
    if(estados_academicos.get_value(indice, "DESERTOR")):
        if math.isnan(cohorte_est):
            desercion[0] += 1
        else:
            desercion[semestres.index(cohorte_est)] += 1
    if(estados_academicos.get_value(indice, 'ACTIVO') and
       (estados_academicos.get_value(indice, 'DESERTOR') == False) and
       semestres_est[-1] == ult_sem):
       if math.isnan(cohorte_est):
           activo[0] += 1
       else:
           activo[semestres.index(cohorte_est)] += 1
        # print(estudiante)
    if((estados_academicos.get_value(indice, 'ACTIVO')  == False) and
        (estados_academicos.get_value(indice, 'DESERTOR') == False) and
        semestres_est[-1] == ult_sem):
        if math.isnan(cohorte_est):
            inactivo[0] += 1
        else:
            inactivo[semestres.index(cohorte_est)] += 1

informacion = [cohorte, grado, desercion, activo, inactivo]
info_pd = pd.DataFrame(columns=columnas)
info_pd['Semestre'] = semestres
info_pd['Cohorte'] = cohorte
info_pd['Grado'] = grado
info_pd['Deserción'] = desercion
info_pd['Activo'] = activo
info_pd['Inactivo'] = inactivo

output_csv = os.path.join(output_dir,'resumen.csv')
info_pd.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)

%pylab inline

# No fui capaz de poner correctamente los Periodos en el eje x
# plt.figure()
# info_pd[columnas[2:]].plot.area(stacked=True,alpha=0.6,x_compat=True)
# plt.xticks([str(i) for i in semestres])

codigos_deser = sorted(
    estados_academicos[
    estados_academicos['DESERTOR'] == True]['CÓDIGO ESTUDIANTE'].unique())
codigos_grad = sorted(
    estados_academicos[
    estados_academicos['GRADO'] == True]['CÓDIGO ESTUDIANTE'].unique())

num_sem_des = []
for deser in codigos_deser:
    semestres_est = sorted(
        estados_academicos[estados_academicos["CÓDIGO ESTUDIANTE"] == deser]
        ['PERIODO'].unique())
    index_des = estados_academicos[
            estados_academicos["CÓDIGO ESTUDIANTE"] == deser].DESERTOR.ne(False).idxmax()
    sem_des_regis = estados_academicos.loc[[index_des]].PERIODO.iloc[0]
    sem_des_regis_index = semestres.index(sem_des_regis)
    sem_des = semestres[sem_des_regis_index-3]
    num_sem_des.append(sum((p%10 == 0 and p <=sem_des) for p in semestres_est))

plt.hist(num_sem_des)
plt.title("Distribución Semestre Deserción")
plt.xlabel("Semestre")
plt.ylabel("# Desertores")
plt.savefig(os.path.join(output_dir,'distribucion_sem.jpg'), dpi=600)

desertores_df = estados_academicos[
                    estados_academicos['CÓDIGO ESTUDIANTE'].isin(codigos_deser)]
grados_df = estados_academicos[
                    estados_academicos['CÓDIGO ESTUDIANTE'].isin(codigos_grad)]

desertores_sem1 = desertores_df[desertores_df["PERIODO"] == desertores_df["COHORTE"]]
grados_sem1 = grados_df[grados_df["PERIODO"] == grados_df["COHORTE"]]
imec_sem1 = estados_academicos[
                    estados_academicos["PERIODO"] == estados_academicos["COHORTE"]]

# # Este código me permite extraer los estudiantes 'raros' para revisar
#
# raros_sem = estados_academicos[
#                     (estados_academicos["PERIODO"] == estados_academicos["COHORTE"]) &
#                     (estados_academicos["CRÉDITOS APROBADOS"] > 30)]
#
# output_csv = os.path.join(output_dir,'raros_sem.csv')
# raros_sem.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)
#
# ########

desertores_sem1["Avg. PROMEDIO SEMESTRE"].mean()
imec_sem1["Avg. PROMEDIO SEMESTRE"].mean()
grados_sem1["Avg. PROMEDIO SEMESTRE"].mean()

desertores_sem1["Avg. PROMEDIO SEMESTRE"].hist(alpha=0.95,normed=1, label="Desertores")
imec_sem1["Avg. PROMEDIO SEMESTRE"].hist(alpha=0.25,normed=1,label="IMEC")
grados_sem1["Avg. PROMEDIO SEMESTRE"].hist(alpha=0.4,normed=1,label="Graduados")
plt.title("Distribución Semestre Deserción")
plt.legend()
plt.xlabel("Avg. PROMEDIO Semestre 1")
plt.ylabel("Distribución")
plt.savefig(os.path.join(output_dir,'distribucion_gpa1.jpg'), dpi=600)
list(desertores_sem1)
desertores_sem1["GÉNERO"].hist(alpha=0.95,normed=1, label="Desertores")
grados_sem1["GÉNERO"].hist(alpha=0.5,normed=1,label="Graduados")
plt.legend()
plt.xlabel("Género")
plt.ylabel("Distribución")
plt.savefig(os.path.join(output_dir,'distribucion_genero.jpg'), dpi=600)

desertores_sem1[desertores_sem1["PRIORIDAD PROGRAMA"] == 1]["CRÉDITOS APROBADOS"].hist(alpha=0.95,normed=1, label="Desertores")
imec_sem1[imec_sem1["PRIORIDAD PROGRAMA"] == 1]["CRÉDITOS APROBADOS"].hist(alpha=0.5,normed=1,label="IMEC")
grados_sem1[grados_sem1["PRIORIDAD PROGRAMA"] == 1]["CRÉDITOS APROBADOS"].hist(alpha=0.5,normed=1,label="Graduados")
plt.title("Distribución Créditos Aprobados")
plt.legend()
plt.xlabel("Créditos Aprobados")
plt.ylabel("Distribución")
plt.savefig(os.path.join(output_dir,'distribucion_creditos_aprobados.jpg'), dpi=600)

estudiante = 201110358
semestre = 201210
curso = 'IMEC1410'

imec1401des = []

for est in codigos_deser:
    cursos_est = cursos_df[cursos_df['CODIGO_ESTUDIANTE'] == est]
    try:
        imec1401des.append(
            cursos_est[cursos_est["CODIGO_CURSO"] == curso]["NOTA_NUMERICA"].iloc[0])
    except:
        imec1401des.append(np.nan)

imec1401grad = []

for est in codigos_grad:
    cursos_est = cursos_df[cursos_df['CODIGO_ESTUDIANTE'] == est]
    try:
        imec1401grad.append(
            cursos_est[cursos_est["CODIGO_CURSO"] == curso]["NOTA_NUMERICA"].iloc[0])
    except:
        imec1401grad.append(np.nan)

len(imec1401des)
imec1401des.count(np.NAN)
len(imec1401grad)
imec1401grad.count(np.NAN)


plt.hist(imec1401des)
plt.title("Distribución Créditos Aprobados")
plt.legend()
plt.xlabel("Créditos Aprobados")
plt.ylabel("Distribución")
plt.savefig(os.path.join(output_dir,'distribucion_creditos_aprobados.jpg'), dpi=600)

curso = 'QUIM1103'

QUIM1103des = []

for est in codigos_deser:
    cursos_est = cursos_df[cursos_df['CODIGO_ESTUDIANTE'] == est]
    try:
        QUIM1103des.append(
            cursos_est[cursos_est["CODIGO_CURSO"] == curso]["NOTA_NUMERICA"].iloc[0])
    except:
        QUIM1103des.append(np.nan)

QUIM1103grad = []

for est in codigos_grad:
    cursos_est = cursos_df[cursos_df['CODIGO_ESTUDIANTE'] == est]
    try:
        QUIM1103grad.append(
            cursos_est[cursos_est["CODIGO_CURSO"] == curso]["NOTA_NUMERICA"].iloc[0])
    except:
        QUIM1103grad.append(np.nan)

len(QUIM1103des)
QUIM1103des.count(np.NAN)
len(QUIM1103grad)
QUIM1103grad.count(np.NAN)


plt.hist(imec1401des)
plt.title("Distribución Créditos Aprobados")
plt.legend()
plt.xlabel("Créditos Aprobados")
plt.ylabel("Distribución")
plt.savefig(os.path.join(output_dir,'distribucion_creditos_aprobados.jpg'), dpi=600)
