install.packages("dplyr")
library(dplyr)

install.packages("rstudioapi")
library(rstudioapi)

# Verificar o diretório atual
absolute_path <- dirname(getActiveDocumentContext()$path)

# Carregar os dados de um arquivo CSV
csv_path = paste0(absolute_path, "/bd.csv")
print(csv_path)
dados <- read.csv(csv_path, sep=";", header=TRUE)

# Verificar os Dados
print("Dados carregados:")
print(dados)

# Separando as culturas
cafe <- dados[dados$cultura == "Café", ]
milho <- dados[dados$cultura == "Milho", ]

# Exibir dados filtrados
print("Dados filtrados - Café:")
print(cafe)
print("Dados filtrados - Milho:")
print(milho)

# Inicializar variáveis para evitar erros caso não haja dados
cafe_media_area_util <- NA
cafe_desvio_area_util <- NA
cafe_media_npk <- NA
cafe_desvio_npk <- NA

milho_media_area_util <- NA
milho_desvio_area_util <- NA
milho_media_npk <- NA
milho_desvio_npk <- NA

# Calcular estatísticas se houver dados disponíveis
if (nrow(cafe) > 0) {
    cafe_media_area_util <- mean(cafe$area_util)
    cafe_desvio_area_util <- sd(cafe$area_util)
    cafe_media_npk <- mean(cafe$npk_kg_m2)
    cafe_desvio_npk <- sd(cafe$npk_kg_m2)

    print("Média e Desvio Padrão - Café")
    print(paste("Média da área útil (Café):", cafe_media_area_util))
    print(paste("Desvio Padrão da área útil (Café):", cafe_desvio_area_util))
    print(paste("Média do NPK (Café):", cafe_media_npk))
    print(paste("Desvio Padrão do NPK (Café):", cafe_desvio_npk))
} else {
    print("Nenhum dado encontrado para Café!")
}

if (nrow(milho) > 0) {
    milho_media_area_util <- mean(milho$area_util)
    milho_desvio_area_util <- sd(milho$area_util)
    milho_media_npk <- mean(milho$npk_kg_m2)
    milho_desvio_npk <- sd(milho$npk_kg_m2)

    print("Média e Desvio Padrão - Milho")
    print(paste("Média da área útil (Milho):", milho_media_area_util))
    print(paste("Desvio Padrão da área útil (Milho):", milho_desvio_area_util))
    print(paste("Média do NPK (Milho):", milho_media_npk))
    print(paste("Desvio Padrão do NPK (Milho):", milho_desvio_npk))
} else {
    print("Nenhum dado encontrado para Milho!")
}

# Criar um data frame com os resultados
resultados_totais <- data.frame(
  Cultura = c("Café", "Milho"),
  Media_Area_Util = c(cafe_media_area_util, milho_media_area_util),
  Desvio_Area_Util = c(cafe_desvio_area_util, milho_desvio_area_util),
  Media_NPK = c(cafe_media_npk, milho_media_npk),
  Desvio_NPK = c(cafe_desvio_npk, milho_desvio_npk)
)

# Imprimir no console
print(resultados_totais)
