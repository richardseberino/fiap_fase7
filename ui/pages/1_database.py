import streamlit as st
import pymysql
import pandas as pd
import yaml
import os
from datetime import datetime

def load_database_config():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'config',
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

def delete_record(table_name, pk_column, pk_value):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {pk_column} = %s", (pk_value,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao excluir: {e}")
            return False
        finally:
            conn.close()
    return False

def insert_cultura(nome, comprimento, largura, area_util, area_total):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO t_cultura (nome, comprimento, largura, area_util, area_total) VALUES (%s, %s, %s, %s, %s)",
                (nome, comprimento, largura, area_util, area_total)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
            return False
        finally:
            conn.close()
    return False

def update_cultura(cd_cultura, nome, comprimento, largura, area_util, area_total):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE t_cultura SET nome=%s, comprimento=%s, largura=%s, area_util=%s, area_total=%s WHERE cd_cultura=%s",
                (nome, comprimento, largura, area_util, area_total, cd_cultura)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
            return False


        finally:
            conn.close()
    return False

def insert_local(nm_local, cd_cultura):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO t_local (nm_local, cd_cultura) VALUES (%s, %s)", (nm_local, cd_cultura))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
            return False
        finally:
            conn.close()
    return False

def update_local(cd_local, nm_local, cd_cultura):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE t_local SET nm_local=%s, cd_cultura=%s WHERE cd_local=%s", (nm_local, cd_cultura, cd_local))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
            return False
        finally:
            conn.close()
    return False

def insert_sensor(cd_local

, nm_sensor):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO t_sensor (cd_local, nm_sensor) VALUES (%s, %s)", (cd_local, nm_sensor))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
            return False
        finally:
            conn.close()
    return False

def update_sensor(cd_sensor, cd_local, nm_sensor):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE t_sensor SET cd_local=%s, nm_sensor=%s WHERE cd_sensor=%s", (cd_local, nm_sensor, cd_sensor))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
            return False
        finally:
            conn.close()
    return False

def insert_produto(ds_produto):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO t_produto (ds_produto) VALUES (%s)", (ds_produto,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
            return False
        finally:
            conn.close()
    return False

def update_produto(cd_produto, ds_produto):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE t_produto SET ds_produto=%s WHERE cd_produto=%s", (ds_produto, cd_produto))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
            return False
        finally:
            conn.close()
    return False

def insert_aplicacao(cd_cultura, cd_produto, value, unit):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO t_aplicacao (cd_cultura, cd_produto, value, unit) VALUES (%s, %s, %s, %s)", 
                         (cd_cultura, cd_produto, value, unit))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
            return False
        finally:
            conn.close()
    return False

def update_aplicacao(cd_aplicacao, cd_cultura, cd_produto, value, unit):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE t_aplicacao SET cd_cultura=%s, cd_produto=%s, value=%s, unit=%s WHERE cd_aplicacao=%s", 
                         (cd_cultura, cd_produto, value, unit, cd_aplicacao))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")
            return False
        finally:
            conn.close()
    return False

def insert_coleta(ts_coleta, cd_sensor, vl_coleta, tp_indicador):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO t_coleta (ts_coleta, cd_sensor, vl_coleta, tp_indicador) VALUES (%s, %s, %s, %s)", 
                         (ts_coleta, cd_sensor, vl_coleta, tp_indicador))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao inserir: {e}")
            return False
        finally:
            conn.close()
    return False

def update_coleta(ts_coleta_old, cd_sensor_old, ts_coleta, cd_sensor, vl_coleta, tp_indicador):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE t_coleta SET ts_coleta=%s, cd_sensor=%s, vl_coleta=%s, tp_indicador=%s WHERE ts_coleta=%s AND cd_sensor=%s", 
                         (ts_coleta, cd_sensor, vl_coleta, tp_indicador, ts_coleta_old, cd_sensor_old))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")


            return False
        finally:
            conn.close()
    return False

def delete_coleta(ts_coleta, cd_sensor):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM t_coleta WHERE ts_coleta=%s AND cd_sensor=%s", (ts_coleta, cd_sensor))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao excluir: {e}")
            return False
        finally:
            conn.close()
    return False

st.title("Gerenciamento de Banco de Dados")

tabs = st.tabs(["Cultura", "Local", "Sensor", "Produto", "Aplicação", "Coleta"])

with tabs[0]:
    st.header("Tabela: t_cultura")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Registros")
        df_cultura = get_all_records("t_cultura")
        if not df_cultura.empty:
            st.dataframe(df_cultura, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado")


    
    with col2:
        st.subheader("Ações")
        action = st.radio("Selecione", ["Criar", "Editar", "Excluir"], key="cultura_action")
        
        if action == "Criar":
            with st.form("create_cultura"):
                nome = st.text_input("Nome")
                comprimento = st.number_input("Comprimento", min_value=1, value=100)
                largura = st.number_input("Largura", min_value=1, value=100)
                area_util = st.number_input("Área Útil", min_value=0.01, value=9000.0, format="%.2f")
                area_total = st.number_input("Área Total", min_value=0.01, value=10000.0, format="%.2f")
                
                if st.form_submit_button("Criar"):
                    if insert_cultura(nome, comprimento, largura, area_util, area_total):
                        st.success("Registro criado!")
                        st.rerun()
        
        elif action == "Editar":
            if not df_cultura.empty:
                cd_cultura = st.selectbox("cd_cultura_update", df_cultura['cd_cultura'].tolist())
                record = df_cultura[df_cultura['cd_cultura'] == cd_cultura].iloc[0]
                
                with st.form("edit_cultura"):
                    nome = st.text_input("Nome", value=record['nome'])
                    comprimento = st.number_input("Comprimento", min_value=1, value=int(record['comprimento']))
                    largura = st.number_input("Largura", min_value=1, value=int(record['largura']))
                    area_util = st.number_input("Área Útil", min_value=0.01, value=float(record['area_util']), format="%.2f")
                    area_total = st.number_input("Área Total", min_value=0.01, value=float(record['area_total']), format="%.2f")
                    
                    if st.form_submit_button("Atualizar"):
                        if update_cultura(cd_cultura, nome, comprimento, largura, area_util, area_total):
                            st.success("Registro atualizado!")
                            st.rerun()
        


        elif action == "Excluir":
            if not df_cultura.empty:
                cd_cultura = st.selectbox("cd_cultura_delete", df_cultura['cd_cultura'].tolist())
                if st.button("excluir_cultura", type="primary"):
                    if delete_record("t_cultura", "cd_cultura", cd_cultura):
                        st.success("Registro excluído!")
                        st.rerun()

with tabs[1]:
    st.header("Tabela: t_local")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Registros")
        df_local = get_all_records("t_local")
        if not df_local.empty:
            st.dataframe(df_local, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado")
    
    with col2:
        st.subheader("Ações")
        action = st.radio("Selecione", ["Criar", "Editar", "Excluir"], key="local_action")
        
        df_cultura = get_all_records("t_cultura")
        
        if action == "Criar":
            with st.form("create_local"):
                nm_local = st.text_input("Nome do Local")
                cd_cultura = st.selectbox("Cultura", df_cultura['cd_cultura'].tolist() if not df_cultura.empty else [])
                
                if st.form_submit_button("Criar"):
                    if insert_local(nm_local, cd_cultura):
                        st.success("Registro criado!")
                        st.rerun()
        
        elif action == "Editar":
            if not df_local.empty:
                cd_local = st.selectbox("cd_local_update", df_local['cd_local'].tolist())
                record = df_local[df_local['cd_local'] == cd_local].iloc[0]
                
                with st.form("edit_local"):
                    nm_local = st.text_input("Nome do Local", value=record['nm_local'])
                    cd_cultura = st.selectbox("Cultura", df_cultura['cd_cultura'].tolist() if not df_cultura.empty else [], 
                                            index=df_cultura['cd_cultura'].tolist().index(record['cd_cultura'])

 if not df_cultura.empty else 0)
                    
                    if st.form_submit_button("Atualizar"):
                        if update_local(cd_local, nm_local, cd_cultura):
                            st.success("Registro atualizado!")
                            st.rerun()
        
        elif action == "Excluir":
            if not df_local.empty:
                cd_local = st.selectbox("cd_local_delete", df_local['cd_local'].tolist())
                if st.button("excluir_local", type="primary"):
                    if delete_record("t_local", "cd_local", cd_local):
                        st.success("Registro excluído!")
                        st.rerun()

with tabs[2]:
    st.header("Tabela: t_sensor")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Registros")
        df_sensor = get_all_records("t_sensor")
        if not df_sensor.empty:
            st.dataframe(df_sensor, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado")
    


    with col2:
        st.subheader("Ações")
        action = st.radio("Selecione", ["Criar", "Editar", "Excluir"], key="sensor_action")
        
        df_local = get_all_records("t_local")
        
        if action == "Criar":
            with st.form("create_sensor"):
                cd_local = st.selectbox("Local", df_local['cd_local'].tolist() if not df_local.empty else [])
                nm_sensor = st.text_input("Nome do Sensor")
                
                if st.form_submit_button("Criar"):
                    if insert_sensor(cd_local, nm_sensor):
                        st.success("Registro criado!")
                        st.rerun()
        
        elif action == "Editar":
            if not df_sensor.empty:
                cd_sensor = st.selectbox("cd_sensor_update", df_sensor['cd_sensor'].tolist())
                record = df_sensor[df_sensor['cd_sensor'] == cd_sensor].iloc[0]
                
                with st.form("edit_sensor"):
                    cd_local = st.selectbox("Local", df_local['cd_local'].tolist() if not df_local.empty else [], 
                                          index=df_local['cd_local'].tolist().index(record['cd_local']) if not df_local.empty else 0)
                    nm_sensor = st.text_input("Nome do Sensor", value=record['nm_sensor'])
                    
                    if st.form_submit_button("Atualizar"):
                        if update_sensor(cd_sensor, cd_local, nm_sensor):
                            st.success("Registro atualizado!")
                            st.rerun()
        
        elif action == "Excluir":
            if not df_sensor.empty:
                cd_sensor = st.selectbox("cd_sensor_delete", df_sensor['cd_sensor'].tolist())
                if st.button("excluir_sensor", type="primary"):
                    if delete_record("t_sensor", "cd_sensor", cd_sensor):
                        st.success("Registro excluído!")
                        st.rerun()

with tabs[3]:
    st.header("Tabela: t_produto")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Registros")
        df_produto = get_all_records("t_produto")
        if not df_produto.empty:
            st.dataframe(df_produto, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado")
    
    with col2:
        st.subheader("Ações")
        action = st.radio("Selecione", ["Criar", "Editar", "Excluir"], key="produto_action")
        
        if action == "Criar":
            with st.form("create_produto"):
                ds_produto = st.text_input("Descrição do Produto")
                
                if st.form_submit_button("Criar"):
                    if insert_produto(ds_produto):
                        st.success("Registro criado!")
                        st.rerun()
        
        elif action == "Editar":
            if not df_produto.empty:
                cd_produto = st.selectbox("cd_produto_update", df_produto['cd_produto'].tolist())
                record = df_produto[df_produto['cd_produto'] ==

 cd_produto].iloc[0]
                
                with st.form("edit_produto"):
                    ds_produto = st.text_input("Descrição do Produto", value=record['ds_produto'])
                    
                    if st.form_submit_button("Atualizar"):
                        if update_produto(cd_produto, ds_produto):
                            st.success("Registro atualizado!")
                            st.rerun()
        
        elif action == "Excluir":
            if not df_produto.empty:
                cd_produto = st.selectbox("cd_produto_delete", df_produto['cd_produto'].tolist())
                if st.button("excluir_produto", type="primary"):
                    if delete_record("t_produto", "cd_produto", cd_produto):
                        st.success("Registro excluído!")
                        st.rerun()

with tabs[4]:
    st.header("Tabela: t_aplicacao")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Registros")
        df_aplicacao = get_all_records("t_aplicacao")
        if not df_aplicacao.empty:
            st.dataframe(df_aplicacao, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado")
    
    with col2:
        st.subheader("Ações")
        action = st.radio("Selecione", ["Criar", "Editar", "Excluir"], key="aplicacao_action")
        
        df_cultura = get_all_records("t_cultura")
        df_produto = get_all_records("t_produto")
        
        if action == "Criar":
            with st.form("create_aplicacao"):
                cd_cultura = st.selectbox("Cultura", df_cultura['cd_cultura'].tolist() if not df_cultura.empty else [])
                cd_produto = st.selectbox("Produto", df_produto['cd_produto'].tolist() if not df_produto.empty else [])
                value = st.number_input("Valor", min_value=0.0, value=100.0, format="%.2f")
                unit = st.text_input("Unidade", value="kg_m2")
                
                if st.form_submit_button("Criar"):
                    if insert_aplicacao(cd_cultura, cd_produto, value, unit):
                        st.success("Registro criado!")
                        st.rerun()
        
        elif action == "Editar":
            if not df_aplicacao.empty:
                cd_aplicacao = st.selectbox("cd_aplicacao_update", df_aplicacao['cd_aplicacao'].tolist())
                record = df_aplicacao[df_aplicacao['cd_aplicacao'] == cd_aplicacao].iloc[0]
                
                with st.form("edit_aplicacao"):
                    cd_cultura = st.selectbox("Cultura", df_cultura['cd_cultura'].tolist() if not df_cultura.empty else [], 
                                            index=df_cultura['cd_cultura'].tolist().index(record['cd_cultura']) if not df_cultura.empty else 0)
                    cd_produto = st.selectbox("Produto", df_produto['cd_produto'].tolist() if not df_produto.empty else [], 
                                            index=df_produto['cd_produto'].tolist().index(record['cd_produto']) if not df_produto.empty else

 0)
                    value = st.number_input("Valor", min_value=0.0, value=float(record['value']), format="%.2f")
                    unit = st.text_input("Unidade", value=record['unit'])
                    
                    if st.form_submit_button("Atualizar"):
                        if update_aplicacao(cd_aplicacao, cd_cultura, cd_produto, value, unit):
                            st.success("Registro atualizado!")
                            st.rerun()
        
        elif action == "Excluir":
            if not df_aplicacao.empty:
                cd_aplicacao = st.selectbox("cd_aplicacao_delete", df_aplicacao['cd_aplicacao'].tolist())
                if st.button("excluir_aplicacao", type="primary"):
                    if delete_record("t_aplicacao", "cd_aplicacao", cd_aplicacao):
                        st.success("Registro excluído!")
                        st.rerun()

with tabs[5]:
    st.header("Tabela: t_coleta")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Registros")


        df_coleta = get_all_records("t_coleta")
        if not df_coleta.empty:
            st.dataframe(df_coleta, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado")
    
    with col2:
        st.subheader("Ações")
        action = st.radio("Selecione", ["Criar", "Editar", "Excluir"], key="coleta_action")
        
        df_sensor = get_all_records("t_sensor")
        
        if action == "Criar":
            with st.form("create_coleta"):
                ts_dt_coleta = st.date_input("Data da Coleta", value=datetime.now())
                ts_tm_coleta = st.time_input("Hora da Coleta", value=datetime.now().time())

                ts_coleta = datetime.combine(ts_dt_coleta, ts_tm_coleta)
                cd_sensor = st.selectbox("Sensor", df_sensor['cd_sensor'].tolist() if not df_sensor.empty else [])
                vl_coleta = st.number_input("Valor da Coleta", value=0.0, format="%.2f")
                tp_indicador = st.text_input("Tipo de Indicador")
                
                if st.form_submit_button("Criar"):
                    if insert_coleta(ts_coleta, cd_sensor, vl_coleta,

 tp_indicador):
                        st.success("Registro criado!")
                        st.rerun()
        
        elif action == "Editar":
            if not df_coleta.empty:
                idx = st.selectbox("Selecione Registro", range(len(df_coleta)), 
                                 format_func=lambda x: f"{df_coleta.iloc[x]['ts_coleta']} - Sensor {df_coleta.iloc[x]['cd_sensor']}")
                record = df_coleta.iloc[idx]
                
                with st.form("edit_coleta"):
                    current_ts = pd.to_datetime(record['ts_coleta'])
                    
                    ts_dt_coleta = st.date_input("Data da Coleta", value=current_ts.date())
                    ts_tm_coleta = st.time_input("Hora da Coleta", value=current_ts.time())

                    ts_coleta = datetime.combine(ts_dt_coleta, ts_tm_coleta)
                    
                    cd_sensor = st.selectbox("Sensor", df_sensor['cd_sensor'].tolist() if not df_sensor.empty else [], 
                                           index=df_sensor['cd_sensor'].tolist().index(record['cd_sensor']) if not df_sensor.empty else 0)
                    vl_coleta = st.number_input("Valor da Coleta", value=float(record['vl_coleta']), format="%.2f")
                    tp_indicador = st.text_input("Tipo de Indicador", value=record['tp_indicador'])
                    
                    if st.form_submit_button("Atualizar"):
                        if update_coleta(record['ts_coleta'], record['cd_sensor'], ts_coleta, cd_sensor, vl_coleta, tp_indicador):
                            st.success("Registro atualizado!")
                            st.rerun()
        
        elif action == "Excluir":
            if not df_coleta.empty:
                idx = st.selectbox("Selecione Registro", range(len(df_coleta)), 
                                 format_func=lambda x: f"{df_coleta.iloc[x]['ts_coleta']} - Sensor {df_coleta.iloc[x]['cd_sensor']}")
                record = df_coleta.iloc[idx]
                if st.button("excluir_coleta", type="primary"):
                    if delete_coleta(record['ts_coleta'], record['cd_sensor']):
                        st.success("Registro excluído!")
                        st.rerun()