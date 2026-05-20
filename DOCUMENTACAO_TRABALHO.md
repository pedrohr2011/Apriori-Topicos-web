# Documentação técnica do projeto Apriori

## Contexto

Este projeto implementa uma análise de regras de associação sobre uma base transacional de atividades acadêmicas. Cada linha do arquivo de entrada representa uma atividade, e os itens analisados são os alunos participantes.

A solução foi organizada em duas abordagens:

- implementação manual do algoritmo Apriori em `src/apriori_manual.py`;
- implementação equivalente usando `mlxtend` em `src/apriori_mlxtend.py`.

## Base de dados

O arquivo de entrada fica em:

```txt
data/input/transactions.csv
```

Cada linha segue o formato:

```txt
id, descrição da atividade, aluno 1, aluno 2, aluno 3, ...
```

Durante o carregamento, as duas primeiras colunas são ignoradas. Apenas os nomes dos alunos são usados como itens das transações.

## Parâmetros padrão

| Parâmetro | Valor |
|---|---:|
| Suporte mínimo | 0.10 |
| Confiança mínima | 0.50 |
| Tamanho máximo do itemset | 3 |

## Métricas

### Suporte

Indica a proporção de transações em que um itemset aparece.

```txt
suporte(X) = transações que contêm X / total de transações
```

### Confiança

Indica a probabilidade de o consequente aparecer quando o antecedente já aparece.

```txt
confiança(A -> B) = suporte(A união B) / suporte(A)
```

### Lift

Indica a força da associação em comparação com o cenário em que antecedente e consequente seriam independentes.

```txt
lift(A -> B) = confiança(A -> B) / suporte(B)
```

## Arquivos principais

| Caminho | Finalidade |
|---|---|
| `main.py` | Executa o fluxo completo do projeto. |
| `src/data_loader.py` | Carrega e processa as transações. |
| `src/apriori_manual.py` | Implementa o Apriori manualmente e gera regras/recomendações. |
| `src/apriori_mlxtend.py` | Executa a comparação usando `mlxtend`. |
| `src/utils.py` | Reúne funções auxiliares para CSV e formatação. |
| `tests/test_apriori.py` | Testes unitários da implementação manual. |
| `outputs/` | Arquivos CSV gerados pelo projeto. |

## Execução

```bash
python -m pip install -r requirements.txt
python main.py
```

## Testes

```bash
python -m unittest discover tests
```

Os testes validam leitura de transações, cálculo de suporte, geração de itemsets frequentes, geração de regras, comportamento com transações vazias e recomendação simples baseada nas regras.

## Interpretação de exemplo

A regra:

```txt
{Ana Silva, Bruno Costa} -> {Kleber Santos}
```

indica que Kleber Santos aparece com frequência relevante em transações onde Ana Silva e Bruno Costa aparecem juntos. Esse padrão pode apoiar uma recomendação de participantes para novas atividades.
