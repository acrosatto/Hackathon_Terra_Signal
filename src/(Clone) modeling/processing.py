from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from category_encoders import TargetEncoder
import pandas as pd

#%%
def preprocessing(xnum: list, xcat:list):
    # constroi pipeline de processamento de variaveis independentes

    pipe_num = Pipeline(steps=[('imputer_num', SimpleImputer(strategy='mean'))])

    pipe_cat = Pipeline(steps=[('imputer_cat', SimpleImputer(strategy='constant', fill_value='missing')),
                               ('mean_encoder', TargetEncoder(smoothing=20))])
    
    pipilene = ColumnTransformer(transformers=[('transformer_cat', pipe_cat, xcat),
                                                 ('transformer_num', pipe_num, xnum)])
    
    return pipilene

def padronizar(dados):    
    # padrinuza e limpa os dados 
    dados["PhoneService"] = dados["PhoneService"].replace({"no": "No", "yes": "Yes"})
    
    # transformando os unknows em nulos pra imputação posterior
    dados["tenure"] = pd.to_numeric(
        dados["tenure"], errors='coerce'
    )

    dados["tenure"] = dados["tenure"].astype('float64')

    colunas_binarias = [
        "Partner", 
        "Dependents", 
        "PhoneService", 
        "PaperlessBilling", 
        "Churn"
    ]

    mapeamento = {
        'Yes': 1, 'No': 0,
        'Sim': 1, 'Não': 0, 'Nao': 0,
        True: 1, False: 0
    }

    for col in colunas_binarias:
        if col in dados.columns:
            dados[col] = dados[col].map(mapeamento)

    return dados        


