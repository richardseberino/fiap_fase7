#!/usr/bin/env python3

import os
import sys
import yaml
import pymysql
from pymysql import Error
from datetime import datetime, timedelta

# Seed data for t_cultura
SEED_DATA_CULTURAS = [
    {
        'cd_cultura': 1,
        'nome': 'Café',
        'comprimento': 200,
        'largura': 200,
        'area_util': 36000.0,
        'area_total': 40000.0
    },
    {
        'cd_cultura': 2,
        'nome': 'Milho',
        'comprimento': 600,
        'largura': 600,
        'area_util': 342000.0,
        'area_total': 360000.0
    }
]

# Seed data for t_local
SEED_DATA_LOCAL = [
    {'nm_local': 'Plantacao Cafe 01', 'cd_cultura': 1},  # References first Café cultura
    {'nm_local': 'Plantacao Soja 02', 'cd_cultura': 2}   # References first Milho cultura
]

# Seed data for t_sensor
SEED_DATA_SENSOR = [
    {'cd_local': 1, 'nm_sensor': 'Sensor Fosforo'},
    {'cd_local': 1, 'nm_sensor': 'Sensor Potassio'},
    {'cd_local': 2, 'nm_sensor': 'Sensor pH'},
    {'cd_local': 2, 'nm_sensor': 'Sensor Umidade'}
]

# Seed data for t_produto
SEED_DATA_PRODUTO = [
    {'ds_produto': 'Adubo NPK 10-10-10'},
    {'ds_produto': 'Irrigacao'}
]

# Seed data for t_aplicacao
SEED_DATA_APLICACAO = [
    {'cd_aplicacao': 1, 'cd_cultura': 1, 'cd_produto': 1, 'value': 540.0, 'unit': 'kg_m2'},
    {'cd_aplicacao': 2, 'cd_cultura': 1, 'cd_produto': 2, 'value': 100.0, 'unit': 'litro_m2'},
    {'cd_aplicacao': 3, 'cd_cultura': 2, 'cd_produto': 1, 'value': 13680.0, 'unit': 'kg_m2'},
    {'cd_aplicacao': 4, 'cd_cultura': 2, 'cd_produto': 2, 'value': 150.0, 'unit': 'litro_m2'}
]

# Seed data for t_coleta (sensor readings)
# Generate sample sensor data for a 7-day period with realistic variations
# Sensor 1: Fosforo (typical range: 30-60 mg/dm³)
# Sensor 2: Potassio (typical range: 35-65 mg/dm³)
# Sensor 3: pH (typical range: 5.5-7.5)
# Sensor 4: Umidade (typical range: 40-80%)
def generate_coleta_data():
    """Generate sample sensor readings for a 7-day period"""
    base_date = datetime(2024, 1, 1, 8, 0, 0)
    coleta_data = []

    # Initial values
    fosforo = 45.0
    potassio = 50.0
    ph = 6.5
    umidade = 65.0

    for day in range(7):
        ts = base_date + timedelta(days=day)

        # Simulate daily variations
        fosforo += (hash(f'f{day}') % 100 - 50) / 100.0  # Small variations
        potassio += (hash(f'p{day}') % 100 - 50) / 100.0
        ph += (hash(f'h{day}') % 100 - 50) / 1000.0
        umidade += (hash(f'u{day}') % 200 - 100) / 10.0

        # Keep values within realistic ranges
        fosforo = max(30.0, min(fosforo, 60.0))
        potassio = max(35.0, min(potassio, 65.0))
        ph = max(5.5, min(ph, 7.5))
        umidade = max(40.0, min(umidade, 80.0))

        # Add readings for each sensor
        coleta_data.append({
            'ts_coleta': ts,
            'cd_sensor': 1,
            'vl_coleta': round(fosforo, 2),
            'tp_indicador': 'Fosforo'
        })
        coleta_data.append({
            'ts_coleta': ts,
            'cd_sensor': 2,
            'vl_coleta': round(potassio, 2),
            'tp_indicador': 'Potassio'
        })
        coleta_data.append({
            'ts_coleta': ts,
            'cd_sensor': 3,
            'vl_coleta': round(ph, 2),
            'tp_indicador': 'pH'
        })
        coleta_data.append({
            'ts_coleta': ts,
            'cd_sensor': 4,
            'vl_coleta': round(umidade, 2),
            'tp_indicador': 'Umidade'
        })

    return coleta_data

SEED_DATA_COLETA = generate_coleta_data()


def load_database_config():
    """Load database configuration from config/database.yml"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'config',
        'database.yml'
    )

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            # Use development environment by default
            env = os.getenv('ENV', 'development')
            return config[env]
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def get_database_connection(config):
    """Create and return a database connection"""
    try:
        # Handle empty/None password from YAML
        password = config.get('password') or ''

        connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=password,
            charset=config.get('charset', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )

        if connection.open:
            print(f"Successfully connected to MySQL database: {config['database']}")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        sys.exit(1)


def clear_existing_data(cursor):
    """Clear existing data from all tables"""
    try:
        # Clear in reverse order due to foreign key constraints
        cursor.execute("DELETE FROM t_coleta")
        cursor.execute("DELETE FROM t_sensor")
        cursor.execute("DELETE FROM t_aplicacao")
        cursor.execute("DELETE FROM t_produto")
        cursor.execute("DELETE FROM t_local")
        cursor.execute("DELETE FROM t_cultura")
        print("Cleared existing data from all tables")
    except Error as e:
        print(f"Error clearing existing data: {e}")
        raise


def seed_local(cursor):
    """Insert seed data into t_local table"""
    insert_query = """
        INSERT INTO t_local (nm_local, cd_cultura)
        VALUES (%(nm_local)s, %(cd_cultura)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA_LOCAL:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into t_local table")
    except Error as e:
        print(f"Error inserting seed data into t_local: {e}")
        raise


def seed_sensor(cursor):
    """Insert seed data into t_sensor table"""
    insert_query = """
        INSERT INTO t_sensor (cd_local, nm_sensor)
        VALUES (%(cd_local)s, %(nm_sensor)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA_SENSOR:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into t_sensor table")
    except Error as e:
        print(f"Error inserting seed data into t_sensor: {e}")
        raise


def seed_produto(cursor):
    """Insert seed data into t_produto table"""
    insert_query = """
        INSERT INTO t_produto (ds_produto)
        VALUES (%(ds_produto)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA_PRODUTO:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into t_produto table")
    except Error as e:
        print(f"Error inserting seed data into t_produto: {e}")
        raise


def seed_aplicacao(cursor):
    """Insert seed data into t_aplicacao table"""
    insert_query = """
        INSERT INTO t_aplicacao (cd_cultura, cd_produto, value, unit)
        VALUES (%(cd_cultura)s, %(cd_produto)s, %(value)s, %(unit)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA_APLICACAO:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into t_aplicacao table")
    except Error as e:
        print(f"Error inserting seed data into t_aplicacao: {e}")
        raise


def seed_coleta(cursor):
    """Insert seed data into t_coleta table"""
    insert_query = """
        INSERT INTO t_coleta (ts_coleta, cd_sensor, vl_coleta, tp_indicador)
        VALUES (%(ts_coleta)s, %(cd_sensor)s, %(vl_coleta)s, %(tp_indicador)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA_COLETA:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into t_coleta table")
    except Error as e:
        print(f"Error inserting seed data into t_coleta: {e}")
        raise


def seed_culturas(cursor):
    """Insert seed data into t_cultura table"""
    insert_query = """
        INSERT INTO t_cultura (nome, comprimento, largura, area_util, area_total)
        VALUES (%(nome)s, %(comprimento)s, %(largura)s, %(area_util)s, %(area_total)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA_CULTURAS:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into culturas table")
    except Error as e:
        print(f"Error inserting seed data into culturas: {e}")
        raise


def main():
    """Main seeding function"""
    print("="*60)
    print("Database Seeding Script")
    print("="*60)

    # Load database configuration
    print("\n[1/4] Loading database configuration...")
    config = load_database_config()

    # Connect to database
    print("[2/4] Connecting to database...")
    connection = get_database_connection(config)

    try:
        cursor = connection.cursor()

        # Clear existing data
        print("[3/4] Clearing existing data...")
        clear_existing_data(cursor)

        # Insert seed data
        print("[4/4] Inserting seed data...")
        print("  - Seeding t_cultura...")
        seed_culturas(cursor)
        print("  - Seeding t_produto...")
        seed_produto(cursor)
        print("  - Seeding t_aplicacao...")
        seed_aplicacao(cursor)
        print("  - Seeding t_local...")
        seed_local(cursor)
        print("  - Seeding t_sensor...")
        seed_sensor(cursor)
        print("  - Seeding t_coleta...")
        seed_coleta(cursor)

        # Commit changes
        connection.commit()

        print("\n" + "="*60)
        print("Seeding completed successfully!")
        print("="*60)

    except Error as e:
        print(f"\nSeeding failed: {e}")
        connection.rollback()
        sys.exit(1)
    finally:
        if connection and connection.open:
            cursor.close()
            connection.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()