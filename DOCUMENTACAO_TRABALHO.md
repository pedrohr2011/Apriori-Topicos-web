# Documentação do trabalho

## Resumo

O trabalho implementa o algoritmo Apriori para encontrar padrões de associação entre alunos que participam de atividades acadêmicas.

Foram feitas duas versões:

- uma implementação manual em Python;
- uma implementação usando a biblioteca `mlxtend`, para comparação.

## Base de dados

O arquivo usado como entrada está em:

```txt
data/input/transactions.csv
```

Cada linha tem este formato:

```txt
id, descrição da atividade, aluno 1, aluno 2, aluno 3, ...
```

No processamento, o id e a descrição são ignorados. A análise usa apenas os nomes dos alunos.

## Parâmetros usados

| Parâmetro | Valor |
|---|---:|
| Suporte mínimo | 0.10 |
| Confiança mínima | 0.50 |
| Tamanho máximo do itemset | 3 |

## Métricas

### Suporte

Proporção de transações em que um itemset aparece.

```txt
suporte(X) = transações que contêm X / total de transações
```

### Confiança

Probabilidade de o consequente aparecer quando o antecedente aparece.

```txt
confiança(A -> B) = suporte(A união B) / suporte(A)
```

### Lift

Mede a força da associação em relação ao cenário em que os itens seriam independentes.

```txt
lift(A -> B) = confiança(A -> B) / suporte(B)
```

## Arquivos principais

| Caminho | Finalidade |
|---|---|
| `main.py` | Executa a análise completa. |
| `src/data_loader.py` | Lê o arquivo de transações. |
| `src/apriori_manual.py` | Contém a implementação manual do Apriori. |
| `src/apriori_mlxtend.py` | Contém a versão feita com `mlxtend`. |
| `src/utils.py` | Funções auxiliares para CSV e formatação. |
| `tests/test_apriori.py` | Testes unitários. |
| `outputs/` | Arquivos CSV gerados pela execução. |

## Execução

```bash
python -m pip install -r requirements.txt
python main.py
```

## Testes

```bash
python -m unittest discover tests
```

Os testes cobrem leitura das transações, cálculo de suporte, geração de itemsets, geração de regras, transações vazias e recomendação simples.

## Exemplo de regra

```txt
{Ana Silva, Bruno Costa} -> {Kleber Santos}
```

Essa regra mostra uma associação entre os três alunos. Quando Ana Silva e Bruno Costa aparecem juntos, Kleber Santos também aparece em parte dessas transações.
