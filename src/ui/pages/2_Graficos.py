import streamlit as st
import pymysql
import pandas as pd
import yaml
import os

def load_database_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        '../config',
        'database.yml'
    )
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            env = os.getenv('ENV', 'development')
            return config[env]
    return None

def get_connection():
    config = load_database_config()
    if config:
        password = config.get('password') or ''
        return pymysql.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=password,
            charset=config.get('charset', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )
    return None

def get_all_records(table_name):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            return pd.DataFrame(records) if records else pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()

st.title("Visualização de Coletas")

df_coleta = get_all_records("t_coleta")
df_sensor = get_all_records("t_sensor")
df_local = get_all_records("t_local")
df_cultura = get_all_records("t_cultura")

if not df_coleta.empty and not df_sensor.empty and not df_local.empty and not df_cultura.empty:
    st.subheader("Gráfico de Coletas por Cultura")

    # Merge all dataframes
    df_merged = pd.merge(df_coleta, df_sensor, on='cd_sensor')
    df_merged = pd.merge(df_merged, df_local, on='cd_local')
    df_merged = pd.merge(df_merged, df_cultura, on='cd_cultura')

    df_merged['ts_coleta'] = pd.to_datetime(df_merged['ts_coleta'])

    # 1. Select Culture
    cultura_names = sorted(df_merged['nome'].unique())
    selected_cultura = st.selectbox("Selecione a Cultura", cultura_names)

    if selected_cultura:
        df_cultura_filtered = df_merged[df_merged['nome'] == selected_cultura]
        
        # 2. Select Sensor (or all)
        sensor_options = ["Exibir Todos"] + sorted(df_cultura_filtered['nm_sensor'].unique())
        selected_sensor = st.selectbox("Selecione o Sensor", sensor_options)

        if selected_sensor == "Exibir Todos":
            # Pivot data to plot all sensors
            df_pivot = df_cultura_filtered.pivot_table(index='ts_coleta', 
                                                       columns='nm_sensor', 
                                                       values='vl_coleta')
            if not df_pivot.empty:
                st.write(f"Exibindo todos os sensores para a cultura **{selected_cultura}**")
                st.line_chart(df_pivot)
            else:
                st.info("Nenhum dado de coleta para os sensores desta cultura.")

        else:
            # Filter for the specific sensor
            df_sensor_filtered = df_cultura_filtered[df_cultura_filtered['nm_sensor'] == selected_sensor]
            
            if not df_sensor_filtered.empty:
                local_nome = df_sensor_filtered['nm_local'].iloc[0]
                st.write(f"**Cultura:** {selected_cultura}")
                st.write(f"**Local:** {local_nome}")

                df_display = df_sensor_filtered.set_index('ts_coleta')[['vl_coleta']]
                st.line_chart(df_display)
            else:
                st.info("Nenhum registro encontrado para o sensor selecionado.")

else:
    st.info("Dados insuficientes para exibir o gráfico. Verifique se há registros nas tabelas de coleta, sensor, local e cultura.")
