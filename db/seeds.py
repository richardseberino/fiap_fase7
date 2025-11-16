#!/usr/bin/env python3

import os
import sys
import yaml
import pymysql
from pymysql import Error

# Hardcoded seed data from bd.csv
SEED_DATA = [
    {
        'nome': 'Café',
        'comprimento': 200,
        'largura': 200,
        'area_util': 36000.0,
        'area_total': 40000.0,
        'npk_kg_m2': 540.0
    },
    {
        'nome': 'Café',
        'comprimento': 400,
        'largura': 400,
        'area_util': 144000.0,
        'area_total': 160000.0,
        'npk_kg_m2': 2160.0
    },
    {
        'nome': 'Milho',
        'comprimento': 600,
        'largura': 600,
        'area_util': 342000.0,
        'area_total': 360000.0,
        'npk_kg_m2': 13680.0
    },
    {
        'nome': 'Milho',
        'comprimento': 400,
        'largura': 400,
        'area_util': 152000.0,
        'area_total': 160000.0,
        'npk_kg_m2': 6080.0
    },
    {
        'nome': 'Café',
        'comprimento': 500,
        'largura': 500,
        'area_util': 225000.0,
        'area_total': 250000.0,
        'npk_kg_m2': 3375.0
    },
    {
        'nome': 'Milho',
        'comprimento': 600,
        'largura': 600,
        'area_util': 342000.0,
        'area_total': 360000.0,
        'npk_kg_m2': 1234.0
    },
    {
        'nome': 'Café',
        'comprimento': 400,
        'largura': 400,
        'area_util': 144000.0,
        'area_total': 160000.0,
        'npk_kg_m2': 2160.0
    },
    {
        'nome': 'Café',
        'comprimento': 420,
        'largura': 420,
        'area_util': 158760.0,
        'area_total': 176400.0,
        'npk_kg_m2': 2381.4
    },
    {
        'nome': 'Milho',
        'comprimento': 420,
        'largura': 420,
        'area_util': 167580.0,
        'area_total': 176400.0,
        'npk_kg_m2': 6703.2
    }
]

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
    """Clear existing data from culturas table"""
    try:
        cursor.execute("DELETE FROM culturas")
        print("Cleared existing data from culturas table")
    except Error as e:
        print(f"Error clearing existing data: {e}")
        raise


def seed_culturas(cursor):
    """Insert seed data into culturas table"""
    insert_query = """
        INSERT INTO culturas (nome, comprimento, largura, area_util, area_total, npk_kg_m2)
        VALUES (%(nome)s, %(comprimento)s, %(largura)s, %(area_util)s, %(area_total)s, %(npk_kg_m2)s)
    """

    try:
        inserted_count = 0
        for data in SEED_DATA:
            cursor.execute(insert_query, data)
            inserted_count += 1

        print(f"Successfully inserted {inserted_count} records into culturas table")
    except Error as e:
        print(f"Error inserting seed data: {e}")
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
        seed_culturas(cursor)

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