# Análise de Regras de Associação com Apriori em Python

## Sobre o projeto

Este projeto aplica o algoritmo Apriori para identificar padrões de associação em dados transacionais. A proposta é gerar itemsets frequentes, regras de associação e recomendações a partir de um conjunto de dados, utilizando tanto uma implementação manual em Python quanto uma abordagem com a biblioteca `mlxtend`.

O objetivo principal é compreender o funcionamento do algoritmo na prática, comparar abordagens e transformar os resultados em informações interpretáveis.

## Objetivo

O objetivo do projeto é analisar dados transacionais e identificar relações frequentes entre itens por meio de regras de associação.

A partir dos dados de entrada, o sistema deve:

- processar as transações;
- gerar itemsets frequentes;
- calcular métricas como suporte, confiança e lift;
- gerar regras de associação;
- exportar os resultados em arquivos CSV;
- validar parte da lógica com testes unitários.

## Tecnologias utilizadas

- Python
- Pandas
- mlxtend
- unittest
- CSV
- Algoritmo Apriori
- Regras de associação

## Conceitos aplicados

### Itemsets frequentes

Conjuntos de itens que aparecem juntos com frequência dentro das transações analisadas.

### Suporte

Métrica que indica a frequência com que um itemset aparece em relação ao total de transações.

### Confiança

Métrica que indica a probabilidade de um item aparecer em uma transação dado que outro item já apareceu.

### Lift

Métrica que indica o quanto a ocorrência conjunta de dois itens é maior ou menor do que seria esperado caso eles fossem independentes.

### Regras de associação

Relações do tipo `A -> B`, indicando que a presença de um conjunto de itens pode estar associada à presença de outro.

## Estrutura do projeto

```txt
Apriori-Topicos-web/
├── data/
│   └── input/
│       └── transactions.csv
├── outputs/
│   ├── itemsets_biblioteca.csv
│   ├── itemsets_manuais.csv
│   ├── recomendacoes_exemplo.csv
│   ├── regras_biblioteca.csv
│   └── regras_manuais.csv
├── src/
│   ├── apriori_manual.py
│   ├── apriori_mlxtend.py
│   ├── data_loader.py
│   └── utils.py
├── tests/
│   └── test_apriori.py
├── DOCUMENTACAO_TRABALHO.md
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
```

## Como executar

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute o fluxo completo:

```bash
python main.py
```

Também é possível executar cada abordagem separadamente:

```bash
python -m src.apriori_manual
python -m src.apriori_mlxtend
```

## Como executar os testes

```bash
python -m unittest discover tests
```

## Resultados gerados

Os arquivos de saída ficam na pasta `outputs/`:

- `itemsets_manuais.csv`: itemsets frequentes gerados pela implementação manual.
- `regras_manuais.csv`: regras de associação geradas pela implementação manual.
- `itemsets_biblioteca.csv`: itemsets frequentes gerados com `mlxtend`.
- `regras_biblioteca.csv`: regras de associação geradas com `mlxtend`.
- `recomendacoes_exemplo.csv`: exemplo de recomendação criado a partir das regras manuais.

Com os parâmetros padrão, o projeto processa 30 transações, usando suporte mínimo de `0.10`, confiança mínima de `0.50` e itemsets com tamanho máximo igual a 3.

## Exemplo de interpretação

Uma regra real gerada pelo projeto é:

`{Ana Silva, Bruno Costa} -> {Kleber Santos}`

Com confiança de aproximadamente `0.67`, essa regra indica que, em cerca de 67% das transações em que Ana Silva e Bruno Costa aparecem juntos, Kleber Santos também aparece.

Esse tipo de análise pode ser usado para identificar padrões de comportamento, apoiar recomendações e entender relações frequentes entre itens.

## Aprendizados

Durante o desenvolvimento deste projeto, foram praticados conceitos de mineração de dados, manipulação de dados com Python, implementação de algoritmos, geração de métricas e validação de código com testes.

Também foi possível comparar uma implementação manual do algoritmo Apriori com uma abordagem utilizando biblioteca, reforçando tanto o entendimento conceitual quanto o uso prático de ferramentas do ecossistema Python.

## Possíveis melhorias futuras

- Criar visualizações gráficas para as regras de associação.
- Permitir entrada de diferentes bases de dados.
- Criar uma interface web simples para upload de arquivos.
- Adicionar notebooks explicativos.
- Comparar o Apriori com outros algoritmos, como FP-Growth.
- Melhorar a cobertura dos testes automatizados.
