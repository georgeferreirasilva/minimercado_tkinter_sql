CREATE DATABASE IF NOT EXISTS testemercado;

USE testemercado;

CREATE TABLE IF NOT EXISTS usuarios (
    usuario VARCHAR(50) PRIMARY KEY,
    senha VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
    codigo VARCHAR(20) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco_custo DECIMAL(10, 2) NOT NULL,
    preco_venda DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL,
    unidade VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATETIME NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS itens_venda (
    venda_id INT,
    produto_codigo VARCHAR(20),
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (produto_codigo) REFERENCES produtos(codigo),
    PRIMARY KEY (venda_id, produto_codigo)
);



