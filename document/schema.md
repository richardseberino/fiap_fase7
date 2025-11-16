# Database Schema

## ERD

```mermaid
erDiagram
    t_cultura ||--o{ t_local : "has"
    t_cultura ||--o{ t_aplicacao : "uses"
    t_produto ||--o{ t_aplicacao : "used_by"
    t_local ||--o{ t_sensor : "has"
    t_sensor ||--o{ t_coleta : "collects"

    t_cultura {
        INTEGER cd_cultura PK "AUTO_INCREMENT"
        VARCHAR_100 nome "NOT NULL"
        INTEGER comprimento "NOT NULL CHECK gt 0"
        INTEGER largura "NOT NULL CHECK gt 0"
        DECIMAL_12_2 area_util "NOT NULL CHECK gt 0"
        DECIMAL_12_2 area_total "NOT NULL CHECK gt 0"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP updated_at "DEFAULT CURRENT_TIMESTAMP ON UPDATE"
    }

    t_local {
        INTEGER cd_local PK "AUTO_INCREMENT"
        VARCHAR_50 nm_local "NOT NULL"
        INTEGER cd_cultura FK "NOT NULL references t_cultura"
    }

    t_sensor {
        INTEGER cd_sensor PK "AUTO_INCREMENT"
        INTEGER cd_local FK "NOT NULL references t_local"
        VARCHAR_35 nm_sensor "NOT NULL"
    }

    t_coleta {
        TIMESTAMP ts_coleta PK "NOT NULL"
        INTEGER cd_sensor PK_FK "NOT NULL references t_sensor"
        DOUBLE vl_coleta "NOT NULL"
        VARCHAR_20 tp_indicador "NOT NULL"
    }

    t_produto {
        INTEGER cd_produto PK "AUTO_INCREMENT"
        VARCHAR_50 ds_produto "NOT NULL"
    }

    t_aplicacao {
        INTEGER cd_aplicacao PK "AUTO_INCREMENT"
        INTEGER cd_cultura FK "NOT NULL references t_cultura"
        INTEGER cd_produto FK "NOT NULL references t_produto"
        DECIMAL_12_2 value "NOT NULL CHECK gte 0"
        VARCHAR_20 unit "NOT NULL"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
        TIMESTAMP updated_at "DEFAULT CURRENT_TIMESTAMP ON UPDATE"
    }
```