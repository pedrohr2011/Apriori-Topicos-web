# Análise de Regras de Associação com Apriori em Python

Projeto em Python para gerar regras de associação a partir de dados transacionais usando o algoritmo Apriori.

A base usada neste trabalho representa atividades acadêmicas. Cada transação possui uma atividade e os alunos participantes. A análise busca encontrar alunos que aparecem juntos com frequência e transformar esses padrões em regras do tipo `A -> B`.

## Objetivo

O objetivo é entender e aplicar o Apriori na prática, passando por todo o fluxo:

- leitura das transações;
- geração de itemsets frequentes;
- cálculo de suporte, confiança e lift;
- criação de regras de associação;
- exportação dos resultados em CSV;
- comparação entre uma implementação manual e uma versão com biblioteca;
- testes unitários para validar partes importantes da lógica.

## Tecnologias utilizadas

- Python
- Pandas
- mlxtend
- unittest
- CSV

## Conceitos aplicados

### Itemsets frequentes

Conjuntos de itens que aparecem juntos com frequência nas transações.

### Suporte

Mostra a frequência de um itemset em relação ao total de transações.

### Confiança

Mostra a chance de um consequente aparecer quando o antecedente já apareceu.

### Lift

Compara a força da regra com o que seria esperado se os itens fossem independentes. Valores maiores que 1 indicam associação positiva.

### Regras de associação

Relações no formato `A -> B`. No contexto deste projeto, uma regra pode indicar que certos alunos costumam participar das mesmas atividades.

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

Execute a análise completa:

```bash
python main.py
```

Também é possível rodar as versões separadamente:

```bash
python -m src.apriori_manual
python -m src.apriori_mlxtend
```

## Como executar os testes

```bash
python -m unittest discover tests
```

## Resultados gerados

Os arquivos ficam na pasta `outputs/`:

- `itemsets_manuais.csv`: itemsets gerados pela implementação manual.
- `regras_manuais.csv`: regras geradas pela implementação manual.
- `itemsets_biblioteca.csv`: itemsets gerados com `mlxtend`.
- `regras_biblioteca.csv`: regras geradas com `mlxtend`.
- `recomendacoes_exemplo.csv`: recomendação simples baseada nas regras manuais.

Com os parâmetros atuais, o projeto usa:

- suporte mínimo: `0.10`;
- confiança mínima: `0.50`;
- tamanho máximo dos itemsets: `3`.

## Exemplo de interpretação

Uma das regras geradas é:

```txt
{Ana Silva, Bruno Costa} -> {Kleber Santos}
```

Essa regra indica que Kleber Santos aparece em parte das transações onde Ana Silva e Bruno Costa aparecem juntos. Pela confiança da regra, isso pode ser usado como base para uma recomendação simples de participante.

## Aprendizados

Neste projeto foram praticados conceitos de mineração de dados, manipulação de arquivos CSV, implementação de algoritmo, cálculo de métricas e testes unitários.

A implementação manual ajudou a entender as etapas do Apriori, enquanto a versão com `mlxtend` serviu como comparação para conferir os resultados.

## Possíveis melhorias futuras

- Criar gráficos para visualizar as regras.
- Permitir o uso de outras bases de dados.
- Criar uma interface web simples para upload do arquivo.
- Adicionar notebooks explicativos.
- Comparar o Apriori com FP-Growth.
- Aumentar a cobertura dos testes.
