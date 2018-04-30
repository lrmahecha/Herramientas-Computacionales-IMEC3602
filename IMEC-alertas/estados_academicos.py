import os
import pandas as pd
from numpy import nan

base_dir = os.path.join( '.','datos')

data_csv = os.path.join(base_dir,'cursos.csv')
cursos_df = pd.read_csv(data_csv, sep = ',',decimal=b'.')
data_csv = os.path.join(base_dir,'grados.csv')
grados_df = pd.read_csv(data_csv, sep = ',', index_col = "CODIGO_ESTUDIANTE")
data_csv = os.path.join(base_dir,'poblacion_imec.csv')
poblacion_imec_df = pd.read_csv(data_csv, sep = ',',decimal=b'.')
data_csv = os.path.join(base_dir,'puntaje_examen.csv')
puntaje_examen_df = pd.read_csv(data_csv, sep = ',', index_col = "CODIGO_ESTUDIANTE")

estados_academicos_df = poblacion_imec_df.copy()

estados_academicos_df["ACTIVIDAD_IMEC"] = ""
estados_academicos_df["DESERTOR"] = ""
estados_academicos_df["GRADO"] = ""
estados_academicos_df["PUNTAJE_EXAMEN"] = ""
estados_academicos_df["NOMBRE_EXAMEN"] = ""
estados_academicos_df["ACTIVO"] = ""
estados_academicos_df["COHORTE"] = ""

codigos_imec = sorted(poblacion_imec_df['CÓDIGO ESTUDIANTE'].unique())

oblig_imec = ["IMEC1000","IMEC1001","IMEC1330","IMEC1410","IMEC1503",
              "IMEC1541","IMEC2210","IMEC2320","IMEC2411",
              "IMEC2520","IMEC2540","IMEC2543","IMEC2700","IMEC3345",
              "IMEC3460","IMEC3530","IMEC3700","IMEC3701","IMEC3702",
              "IMEC3991"]

oblig_otros = ["MATE1203","QUIM1103","MATE1214","FISI1018","FISI1019",
               "ISIS1204","LENG1501","LITE1611","MATE1105",
               "FISI1028","FISI1029","DERE1300","MATE1207","IELE1002",
               "MATE2301","IIND2106","IELE2300","IIND2401"]

semestres = [201110,201120,201210,201220,201310,201320,201410,201420,201510,201520,
             201610,201620,201710,201720,201810]

# Último en que se puede haber desertado, debe ser actualizado cada semestre

ult_sem_des = semestres[-3]
conteo = 0

# Para efectos de debugging
#estudiante = codigos_imec[10]

for estudiante in codigos_imec:

    conteo = conteo + 1

    if conteo%100 == 0:
        print("Voy en el "+str(conteo)+"...")

    semestres_est = sorted(
        poblacion_imec_df[poblacion_imec_df["CÓDIGO ESTUDIANTE"] == estudiante]
        ['PERIODO'].unique())

    info_est = cursos_df[cursos_df['CODIGO_ESTUDIANTE'] == estudiante]

    desertor = "FALSE"
    cont_desertor = 0
    grado = "FALSE"
    grado_flag = "FALSE"
    puntaje_examen_est = nan
    nombre_examen_est = None

    sem0 = semestres_est[0]
    if (estados_academicos_df[
        (estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante) &
        (estados_academicos_df["PERIODO"] == sem0)]["SOBREPASO ACADÉMICO"] ==
        "PRIMIPARO").any():
        if sem0%10 == 0:
            cohorte_est = sem0
        else:
            cohorte_est = sem0 - sem0%100 + 20
    else:
        cohorte_est = nan

    try:
        sem_grado_est = int(semestres[semestres.index(
                            grados_df.get_value(estudiante, "PERIODO"))-1])
        grado_flag = "TRUE"
    except:
        sem_grado_est = "XXXXXXXXX"

    try:
        puntaje_examen_est = puntaje_examen_df.loc[estudiante]['Avg. RESULTADO_CUANTITATIVO']
        nombre_examen_est = puntaje_examen_df.loc[estudiante]['NOMBRE_EXAMEN']
        try:
            puntaje_examen_est = puntaje_examen_est.iloc[0]
            nombre_examen_est = nombre_examen_est.iloc[0]
        except:
            pass
    except:
        pass

    if (semestres_est[0]%10 == 0):
        sem_index_ant = semestres.index(semestres_est[0])
    else:
        sem_index_ant = semestres.index(semestres_est[0]-semestres_est[0]%10)

    for sem in semestres_est:
        if sem in semestres: #todo me falta resolver como hago para no tener dersertor
                            # repetido para un solo estudiante. Aca puede pasar en caso
                            #de que el estudiante se ausente muchos semestres.
            sem_index = semestres.index(sem)
            for i in range(sem_index_ant, sem_index-1):
                result = estados_academicos_df[
                    (estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante) &
                    (estados_academicos_df["PERIODO"] == semestres[sem_index_ant])]
                indice = result.iloc[0].name
                indice_add = estados_academicos_df.index[-1]+1
                line_dict = estados_academicos_df.iloc[[indice]].to_dict()
                cont_desertor = cont_desertor + 1
                if cont_desertor == 3 and grado != "TRUE":
                    desertor = "TRUE"
                line = pd.DataFrame({
                    'ACTIVIDAD_IMEC': "FALSE",
                    "CÓDIGO ESTUDIANTE": estudiante,
                    "PERIODO": semestres[i+1],
                    "Year of FECHA NACIMIENTO":line_dict["Year of FECHA NACIMIENTO"][indice],
                    "CIUDAD RESIDENCIA": line_dict["CIUDAD RESIDENCIA"][indice],
                    'CREDITOS PGA': line_dict['CREDITOS PGA'][indice],
                    'CRÉDITOS APROBADOS': line_dict['CRÉDITOS APROBADOS'][indice],
                    'CRÉDITOS TOMADOS': line_dict['CRÉDITOS TOMADOS'][indice],
                    'CRÉDITOS TRANSFERIDOS': line_dict['CRÉDITOS TRANSFERIDOS'][indice],
                    'GRADO': line_dict['GRADO'][indice],
                    'PRIORIDAD PROGRAMA': line_dict['PRIORIDAD PROGRAMA'][indice],
                    'Avg. PROMEDIO ACUMULADO': line_dict['Avg. PROMEDIO ACUMULADO'][indice],
                    'PUNTAJE_EXAMEN': line_dict['PUNTAJE_EXAMEN'][indice],
                    'NOMBRE_EXAMEN': line_dict['NOMBRE_EXAMEN'][indice],
                    'SEMESTRE SEGÚN CRÉDITOS': line_dict['SEMESTRE SEGÚN CRÉDITOS'][indice],
                    'DESERTOR': desertor,
                    "GÉNERO": line_dict['GÉNERO'][indice],
                    "ACTIVO": "FALSE",
                    "COHORTE": cohorte_est}, index=[indice_add])
                estados_academicos_df = estados_academicos_df.append(line)
        else:
            pass

        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
                    & (estados_academicos_df["PERIODO"] == sem),"COHORTE"] = cohorte_est
        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
                    & (estados_academicos_df["PERIODO"] == sem),"ACTIVO"] = "TRUE"

        info_sem = info_est[(info_est['PERIODO'] == sem)].drop_duplicates(subset=['CRN'])

        sem_imec = "FALSE"
        for index, row in info_sem.iterrows():
            if ((row["CODIGO_CURSO"] in oblig_imec) or
                (row["CODIGO_CURSO"] in oblig_otros)):
                sem_imec = "TRUE"
                desertor = "FALSE"
                cont_desertor = 0
                estados_academicos_df.at[
                    (estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante),
                    "DESERTOR"] = "FALSE"

        if sem == sem_grado_est:
            grado = "TRUE"

        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
            & (estados_academicos_df["PERIODO"] == sem),"ACTIVIDAD_IMEC"] = sem_imec

        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
            & (estados_academicos_df["PERIODO"] == sem),"GRADO"] = grado

        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
            & (estados_academicos_df["PERIODO"] == sem),"PUNTAJE_EXAMEN"] = puntaje_examen_est

        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
            & (estados_academicos_df["PERIODO"] == sem),"NOMBRE_EXAMEN"] = nombre_examen_est

        if (sem%10 == 0):
            if sem_imec == "FALSE":
                cont_desertor = cont_desertor + 1
            else:
                cont_desertor = 0

            if cont_desertor == 3 and grado != "TRUE":
                desertor = "TRUE"

        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
                & (estados_academicos_df["PERIODO"] == sem),"DESERTOR"] = desertor

        sem_index_ant = sem_index

    if ((grado == "FALSE") and (grado_flag == "TRUE")):
        grado = "TRUE"
        estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
                & (estados_academicos_df["PERIODO"] == sem),"GRADO"] = grado
    # if ((sem < ult_sem_des) and ((grado == "FALSE") and (desertor == "FALSE"))):
    #     desertor = "TRUE"
    #     estados_academicos_df.at[(estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante)
    #             & (estados_academicos_df["PERIODO"] == sem),"DESERTOR"] = desertor

    if ((sem < semestres[-1]) and ((grado == "FALSE") and (desertor == "FALSE"))):
        if (sem%10 == 0):
            ult_sem = semestres.index(sem)
        else:
            ult_sem = semestres.index(sem-sem%10)

        break_flag = 0
        for sem_add in semestres[ult_sem+1:]:
            cont_desertor = cont_desertor + 1
            if cont_desertor == 3 and grado != "TRUE":
                desertor = "TRUE"
                break_flag = 1
            result = estados_academicos_df[
                (estados_academicos_df["CÓDIGO ESTUDIANTE"] == estudiante) &
                (estados_academicos_df["PERIODO"] == sem)]
            indice = result.iloc[0].name
            indice_add = estados_academicos_df.index[-1]+1
            line_dict = estados_academicos_df.iloc[[indice]].to_dict()
            line = pd.DataFrame({
                    'ACTIVIDAD_IMEC': "FALSE",
                    "CÓDIGO ESTUDIANTE": estudiante,
                    "PERIODO": sem_add,
                    "Year of FECHA NACIMIENTO":line_dict["Year of FECHA NACIMIENTO"][indice],
                    "CIUDAD RESIDENCIA": line_dict["CIUDAD RESIDENCIA"][indice],
                    'CREDITOS PGA': line_dict['CREDITOS PGA'][indice],
                    'CRÉDITOS APROBADOS': line_dict['CRÉDITOS APROBADOS'][indice],
                    'CRÉDITOS TOMADOS': line_dict['CRÉDITOS TOMADOS'][indice],
                    'CRÉDITOS TRANSFERIDOS': line_dict['CRÉDITOS TRANSFERIDOS'][indice],
                    'DESERTOR': desertor,
                    'GRADO': line_dict['GRADO'][indice],
                    'PRIORIDAD PROGRAMA': line_dict['PRIORIDAD PROGRAMA'][indice],
                    'Avg. PROMEDIO ACUMULADO': line_dict['Avg. PROMEDIO ACUMULADO'][indice],
                    'PUNTAJE_EXAMEN': line_dict['PUNTAJE_EXAMEN'][indice],
                    'NOMBRE_EXAMEN': line_dict['NOMBRE_EXAMEN'][indice],
                    'SEMESTRE SEGÚN CRÉDITOS': line_dict['SEMESTRE SEGÚN CRÉDITOS'][indice],
                    "GÉNERO": line_dict['GÉNERO'][indice],
                    "ACTIVO": "FALSE",
                    "COHORTE": cohorte_est}, index=[indice_add])
            estados_academicos_df = estados_academicos_df.append(line)
            if break_flag == 1: break

estados_academicos_df = estados_academicos_df[[
 'CÓDIGO ESTUDIANTE',
 'PERIODO',
 'GRADO',
 'DESERTOR',
 'ACTIVIDAD_IMEC',
 'ACTIVO',
 'Year of FECHA NACIMIENTO',
 'COHORTE',
 'CREDITOS PGA',
 'CRÉDITOS APROBADOS',
 'CRÉDITOS SEMESTRE APROBADOS',
 'CRÉDITOS SEMESTRE TOMADOS',
 'CRÉDITOS TOMADOS',
 'CRÉDITOS TRANSFERIDOS',
 'CRÉDTIOS SEMESTRE PGA',
 'GÉNERO',
 'PRIORIDAD PROGRAMA',
 'Avg. PROMEDIO ACUMULADO',
 'Avg. PROMEDIO SEMESTRE',
 'PUNTAJE_EXAMEN',
 'NOMBRE_EXAMEN',
 'SEMESTRE SEGÚN CRÉDITOS',
 'SITUACIÓN ACADÉMICA',
 'SOBREPASO ACADÉMICO',
 'CIUDAD RESIDENCIA']]

estados_academicos_df.columns = [
 'CODIGO_ESTUDIANTE',
 'PERIODO',
 'GRADO',
 'DESERTOR',
 'ACTIVIDAD_IMEC',
 'ACTIVO',
 'FECHA_NACIMIENTO',
 'COHORTE',
 'CREDITOS_PGA',
 'CREDITOS_APROBADOS',
 'CREDITOS_SEMESTRE_APROBADOS',
 'CREDITOS_SEMESTRE_TOMADOS',
 'CREDITOS_TOMADOS',
 'CREDITOS_TRANSFERIDOS',
 'CREDITOS_SEMESTRE_PGA',
 'GENERO',
 'PRIORIDAD_PROGRAMA',
 'PROMEDIO_ACUMULADO',
 'PROMEDIO_SEMESTRE',
 'PUNTAJE_EXAMEN',
 'NOMBRE_EXAMEN',
 'SEMESTRE_SEGUN_CREDITOS',
 'SITUACION_ACADEMICA',
 'SOBREPASO_ACADEMICO',
 'CIUDAD_RESIDENCIA']

estados_academicos_df = estados_academicos_df.sort_values(by=['CODIGO_ESTUDIANTE','PERIODO'])
estados_academicos_df = estados_academicos_df.reset_index(drop=True)

output_csv = os.path.join(base_dir,'estados_academicos.csv')
estados_academicos_df.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)
# Las lineas a continuación se necesitan si el archivo de origen viene separado por
# punto y coma ; y se quiere producir uno separado por coma ,
# output_csv = os.path.join(base_dir,'cursos_coma.csv')
# cursos_df.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)

codigos_df = pd.DataFrame({'CODIGO_ESTUDIANTE':codigos_imec})
output_csv = os.path.join(base_dir,'codigos.csv')
codigos_df.to_csv(output_csv,encoding="utf-8",index=False,index_label=False)
