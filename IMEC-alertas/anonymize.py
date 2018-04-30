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

codigos_imec = sorted(estados_academicos['CODIGO_ESTUDIANTE'].unique())

import uuid

hasheado = {}

for estudiante in codigos_imec:
    hasheado[estudiante] = uuid.uuid4()

estados_academicos_hash = estados_academicos.replace({"CODIGO_ESTUDIANTE": hasheado})
cursos_df_hash = cursos_df.replace({"CODIGO_ESTUDIANTE": hasheado})

data_csv = os.path.join(base_dir,'grados.csv')
grados_df = pd.read_csv(data_csv, sep = ',')
grados_df_hash = grados_df.replace({"CODIGO_ESTUDIANTE": hasheado})

output_csv = os.path.join(base_dir,'estados_academicos_anon.csv')
estados_academicos_hash.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)

output_csv = os.path.join(base_dir,'cursos_anon.csv')
cursos_df_hash.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)

output_csv = os.path.join(base_dir,'grados_anon.csv')
grados_df_hash.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)
