import pandas as pd
from sqlalchemy import create_engine
import glob
import os

print("Script iniciado...")

engine = create_engine() #adc caminho do seu DBrowser 

print("Banco conectado...")

arquivos = glob.glob("C:/Users/User/Desktop/", recursive=True) #adc caminho do seu arquivo/pasta
arquivos = [a for a in arquivos if not os.path.basename(a).startswith("~$")]

print(f"Arquivos encontrados: {len(arquivos)}")

for caminho in arquivos:
    try:
        df = pd.read_excel(caminho, engine="openpyxl")
        
        # Converte colunas de horário pra texto
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].apply(lambda x: str(x) if hasattr(x, 'hour') else x)
        
        nome_tabela = os.path.splitext(os.path.basename(caminho))[0]
        df.to_sql(nome_tabela, engine, if_exists="fail", index=False)
        print(f"✅ {nome_tabela} ({len(df)} linhas)")
    except Exception as e:
        print(f"❌ Erro em {caminho}: {e}")