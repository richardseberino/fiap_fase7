-- Drop tables in correct order (respecting foreign key constraints)
DROP TABLE IF EXISTS t_cultura;
DROP TABLE IF EXISTS t_coleta;
DROP TABLE IF EXISTS t_sensor;
DROP TABLE IF EXISTS t_aplicacao;
DROP TABLE IF EXISTS t_produto;
DROP TABLE IF EXISTS t_local;

CREATE TABLE t_cultura (
    cd_cultura INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    comprimento INTEGER NOT NULL,
    largura INTEGER NOT NULL,
    area_util DECIMAL(12, 2) NOT NULL,
    area_total DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (comprimento > 0),
    CHECK (largura > 0),
    CHECK (area_util > 0),
    CHECK (area_total > 0),
    CHECK (area_util <= area_total)
);

CREATE INDEX idx_cultura ON t_cultura(nome);
CREATE INDEX idx_created_at ON t_cultura(created_at);

CREATE TABLE t_local (
    cd_local INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    nm_local VARCHAR(50) NOT NULL,
    cd_cultura INTEGER NOT NULL,
    CONSTRAINT fk_cultura FOREIGN KEY (cd_cultura) REFERENCES t_cultura(cd_cultura)
);

CREATE TABLE t_sensor (
    cd_sensor INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cd_local INTEGER NOT NULL,
    nm_sensor VARCHAR(35) NOT NULL,
    CONSTRAINT fk_local FOREIGN KEY (cd_local) REFERENCES t_local(cd_local)
);

CREATE TABLE t_coleta (
    ts_coleta TIMESTAMP NOT NULL,
    cd_sensor INTEGER NOT NULL,
    vl_coleta DOUBLE NOT NULL,
    tp_indicador VARCHAR(20) NOT NULL,
    PRIMARY KEY (ts_coleta, cd_sensor),
    CONSTRAINT fk_sensor FOREIGN KEY (cd_sensor) REFERENCES t_sensor(cd_sensor)
);

CREATE TABLE t_produto (
    cd_produto INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ds_produto VARCHAR(50) NOT NULL
);

-- Tabela de aplicacao de produtos para culturas
CREATE TABLE t_aplicacao (
    cd_aplicacao INTEGER PRIMARY KEY AUTO_INCREMENT,
    cd_cultura INTEGER NOT NULL,
    cd_produto INTEGER NOT NULL,
    value DECIMAL(12, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_aplicacao_cultura FOREIGN KEY (cd_cultura) REFERENCES t_cultura(cd_cultura),
    CONSTRAINT fk_aplicacao_produto FOREIGN KEY (cd_produto) REFERENCES t_produto(cd_produto),
    CHECK (value >= 0)
);

CREATE INDEX idx_aplicacao_cultura_produto ON t_aplicacao(cd_cultura, cd_produto);
