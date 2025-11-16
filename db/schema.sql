DROP TABLE IF EXISTS culturas;

CREATE TABLE culturas (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    comprimento INTEGER NOT NULL,
    largura INTEGER NOT NULL,
    area_util DECIMAL(12, 2) NOT NULL,
    area_total DECIMAL(12, 2) NOT NULL,
    npk_kg_m2 DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (comprimento > 0),
    CHECK (largura > 0),
    CHECK (area_util > 0),
    CHECK (area_total > 0),
    CHECK (area_util <= area_total),
    CHECK (npk_kg_m2 >= 0)
);

CREATE INDEX idx_cultura ON culturas(nome);
CREATE INDEX idx_created_at ON culturas(created_at);
