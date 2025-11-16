# Database Schema

This document provides a visual representation of the database schema using Mermaid ER diagrams.

## Entity Relationship Diagram

```mermaid
erDiagram
    t_cultura ||--o{ t_local : "has"
    t_cultura ||--o{ t_aplicacao : "uses"
    t_produto ||--o{ t_aplicacao : "used_by"
    t_local ||--o{ t_sensor : "has"
    t_sensor ||--o{ t_coleta : "collects"

    t_cultura {
        INTEGER cd_cultura PK "AUTO_INCREMENT"
        VARCHAR(100) nome "NOT NULL"
        INTEGER comprimento "NOT NULL, CHECK > 0"
        INTEGER largura "NOT NULL, CHECK > 0"
        DECIMAL(12,2) area_util "NOT NULL, CHECK > 0"
        DECIMAL(12,2) area_total "NOT NULL, CHECK > 0"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP updated_at "DEFAULT CURRENT_TIMESTAMP ON UPDATE"
    }

    t_local {
        INTEGER cd_local PK "AUTO_INCREMENT"
        VARCHAR(50) nm_local "NOT NULL"
        INTEGER cd_cultura FK "NOT NULL, references t_cultura(cd_cultura)"
    }

    t_sensor {
        INTEGER cd_sensor PK "AUTO_INCREMENT"
        INTEGER cd_local FK "NOT NULL, references t_local(cd_local)"
        VARCHAR(35) nm_sensor "NOT NULL"
    }

    t_coleta {
        TIMESTAMP ts_coleta PK "NOT NULL"
        INTEGER cd_sensor PK_FK "NOT NULL, references t_sensor(cd_sensor)"
        DOUBLE vl_coleta "NOT NULL"
        VARCHAR(20) tp_indicador "NOT NULL"
    }

    t_produto {
        INTEGER cd_produto PK "AUTO_INCREMENT"
        VARCHAR(50) ds_produto "NOT NULL"
    }

    t_aplicacao {
        INTEGER cd_aplicacao PK "AUTO_INCREMENT"
        INTEGER cd_cultura FK "NOT NULL, references t_cultura(cd_cultura)"
        INTEGER cd_produto FK "NOT NULL, references t_produto(cd_produto)"
        DECIMAL(12,2) value "NOT NULL, CHECK >= 0"
        VARCHAR(20) unit "NOT NULL"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP updated_at "DEFAULT CURRENT_TIMESTAMP ON UPDATE"
    }
```

## Table Descriptions

### Core Tables

#### `t_cultura` (Crop/Culture Types)
Stores information about different crop types and their dimensional characteristics.
- Primary Key: `cd_cultura` (AUTO_INCREMENT)
- Indexes: `idx_cultura(nome)`, `idx_created_at(created_at)`
- Constraints: Area and dimension validations
- Fields:
  - `nome`: Crop name (e.g., "Café", "Milho")
  - `comprimento`: Length in meters
  - `largura`: Width in meters
  - `area_util`: Usable area in m²
  - `area_total`: Total area in m²

#### `t_local` (Plantation Locations)
Represents physical plantation locations, each associated with a specific crop type.
- Primary Key: `cd_local` (AUTO_INCREMENT)
- Foreign Keys: `cd_cultura` → `t_cultura(cd_cultura)`
- Fields:
  - `nm_local`: Location name (e.g., "Plantacao Cafe 01")

#### `t_sensor` (Sensors)
IoT sensors installed at plantation locations for monitoring.
- Primary Key: `cd_sensor` (AUTO_INCREMENT)
- Foreign Keys: `cd_local` → `t_local(cd_local)`
- Fields:
  - `nm_sensor`: Sensor name/type (e.g., "Sensor Fosforo", "Sensor pH")

#### `t_produto` (Products)
Agricultural products (fertilizers, irrigation, etc.) that can be applied.
- Primary Key: `cd_produto` (AUTO_INCREMENT)
- Fields:
  - `ds_produto`: Product description (e.g., "Adubo NPK 10-10-10", "Irrigacao")

### Relationship Tables

#### `t_aplicacao` (Product Application Recommendations)
Defines recommended product applications for specific crop types, including dosage and units.
- Primary Key: `cd_aplicacao` (AUTO_INCREMENT)
- Foreign Keys:
  - `cd_cultura` → `t_cultura(cd_cultura)`
  - `cd_produto` → `t_produto(cd_produto)`
- Index: `idx_aplicacao_cultura_produto(cd_cultura, cd_produto)`
- Fields:
  - `value`: Recommended dosage amount
  - `unit`: Measurement unit (e.g., "kg_m2", "litro_m2")
  - `created_at`: Record creation timestamp
  - `updated_at`: Record update timestamp

### Transaction/Event Tables

#### `t_coleta` (Sensor Data Collection)
Time-series data collected by sensors.
- Composite Primary Key: `(ts_coleta, cd_sensor)`
- Foreign Keys: `cd_sensor` → `t_sensor(cd_sensor)`
- Fields:
  - `ts_coleta`: Collection timestamp
  - `vl_coleta`: Measured value
  - `tp_indicador`: Indicator type (e.g., "Fosforo", "Potassio", "pH", "Umidade")

## Relationships Summary

1. **Cultura → Local (1:N)**: Each plantation location grows one crop type
2. **Cultura → Aplicacao (1:N)**: Each crop has recommended product applications
3. **Produto → Aplicacao (1:N)**: Each product can be recommended for multiple crops
4. **Local → Sensor (1:N)**: Each location can have multiple sensors
5. **Sensor → Coleta (1:N)**: Each sensor generates multiple data collection records

## Data Flow

```
IoT Monitoring Flow:
t_cultura → t_local → t_sensor → t_coleta (continuous data collection)

Product Management Flow:
t_cultura + t_produto → t_aplicacao (product recommendations for crops)
```

## Use Cases

1. **Crop Management**: Define crops with their physical dimensions and calculate areas
2. **Location Tracking**: Associate plantation locations with specific crop types
3. **Sensor Monitoring**: Track IoT sensors installed at each location
4. **Data Collection**: Store time-series sensor readings (pH, humidity, nutrient levels)
5. **Product Recommendations**: Define recommended product applications and dosages per crop type
