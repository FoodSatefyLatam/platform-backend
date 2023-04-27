import pandas as pd

#para nutrientes_ajustados
col_entrevistado_na = [
    "macrozona",
    "id", #id
    "sex", #sexo
    "ht", #altura
    "wgt", #peso
    "ageyrs", #años
]

#falta le comuna y region 

#para alimentos ajustados
col_entrevistado_aa = [
    "folio",
    "region",
    "g_comuna"
]

df_najustado = pd.read_csv("ENCA_Er24h_Nutrientes_AJUSTADO.csv", sep=',', header=0, usecols = col_entrevistado_na)

df_anajustado = pd.read_csv("ENCA_ETCC_ALIMENTOS_AGRUPADOS.csv", sep=',', header=0, usecols= col_entrevistado_aa)
df_anajustado.rename(columns={'folio': 'id'}, inplace=True)

print(df_anajustado.shape)

print(df_najustado.shape)

df_entrevistado = pd.merge(df_anajustado, df_najustado, on = "id", how="inner")
df_entrevistado.drop_duplicates(subset=['id'], keep= "first", inplace=True)

print(df_entrevistado.shape)

print(df_entrevistado.head())

df_entrevistado.to_csv("entrevistados.csv", index=False)
