# Implementação do algoritmo Apriori para regras de associação

**Universidade:** UFRRJ

**Curso:** Sistemas de Informação

**Disciplina:** Tópicos Especiais em Desenvolvimento Web

**Professor(a):** Tiago Cruz de Franca

**Aluno(a):** Pedro Henrique Rainha de Souza

**Data:** 08/05/2026

## Resumo

Este trabalho apresenta a implementação do algoritmo Apriori para descoberta de padrões de participação em atividades extracurriculares de uma universidade fictícia chamada Campus Nova Aurora. O objetivo foi identificar combinações frequentes de alunos e gerar regras de associação que possam apoiar um sistema simples de recomendação. A solução foi desenvolvida em Python de duas formas: uma implementação própria, construída do zero, e uma segunda implementação utilizando a biblioteca `mlxtend`. A partir das transações fornecidas no arquivo `3.transactionsParaRegrasAssociacao.txt`, foram calculadas as métricas de suporte, confiança e alavancagem para regras envolvendo pares de alunos e pares associados a um terceiro aluno.

## 1. Introdução

Regras de associação são técnicas utilizadas em mineração de dados para identificar relações frequentes entre itens de um conjunto de transações. Um exemplo clássico é a análise de cesta de compras, na qual se busca descobrir quais produtos costumam ser comprados juntos. Neste trabalho, a mesma ideia foi aplicada ao contexto acadêmico.

Cada transação representa uma atividade extracurricular, como esportes, grupos de estudo, monitorias, projetos de pesquisa e eventos culturais. Os itens de cada transação são os alunos que participaram daquela atividade. Dessa forma, ao identificar que determinados alunos aparecem frequentemente juntos, torna-se possível gerar recomendações. Por exemplo, se uma regra indica que `{Ana Silva, Bruno Costa} -> {Kleber Santos}`, então, quando Ana e Bruno estiverem inscritos em uma nova atividade, Kleber pode ser recomendado como participante potencial.

## 2. Objetivos

O objetivo geral do trabalho é aplicar o algoritmo Apriori para descobrir padrões de associação entre alunos participantes de atividades extracurriculares.

Os objetivos específicos são:

- Ler e processar o arquivo de transações fornecido.
- Ignorar o identificador e a descrição da atividade.
- Utilizar apenas os nomes dos alunos como itens das transações.
- Implementar o Apriori do zero em Python.
- Calcular suporte, confiança e alavancagem das regras.
- Gerar regras entre pares de alunos e regras do tipo par com terceiro aluno.
- Implementar uma versão equivalente utilizando uma biblioteca pronta.
- Comparar os resultados obtidos pelas duas abordagens.
- Demonstrar um exemplo simples de recomendação.

## 3. Base de dados

O arquivo utilizado foi:

```text
3.transactionsParaRegrasAssociacao.txt
```

Cada linha do arquivo possui a seguinte estrutura:

```text
id, descrição da atividade, aluno 1, aluno 2, aluno 3, ...
```

Exemplo:

```text
id-1, Jogo de tênis nas sextas, Ana Silva, Bruno Costa, Carlos Souza, Daniela Rocha
```

No processamento, as duas primeiras colunas são descartadas. A transação final considerada pelo algoritmo é:

```text
{Ana Silva, Bruno Costa, Carlos Souza, Daniela Rocha}
```

A base contém 30 transações no total.

## 4. Metodologia

A solução foi dividida em duas abordagens.

Na primeira abordagem, o Apriori foi implementado manualmente no arquivo `apriori_associacao.py`. Essa implementação realiza a leitura das transações, gera candidatos, filtra itemsets frequentes de acordo com o suporte mínimo e, em seguida, cria regras de associação a partir dos itemsets encontrados.

Na segunda abordagem, o arquivo `apriori_biblioteca.py` utiliza a biblioteca `mlxtend`, que já possui funções prontas para geração de itemsets frequentes e regras de associação.

Os parâmetros adotados foram:

| Parâmetro | Valor utilizado | Justificativa |
|---|---:|---|
| Suporte mínimo | 0.10 | Representa pelo menos 3 ocorrências em 30 transações. |
| Confiança mínima | 0.50 | Mantém regras em que a consequência ocorre em pelo menos metade dos casos do antecedente. |
| Tamanho máximo do itemset | 3 | Atende ao enunciado, que solicita pares e pares com um terceiro item. |

## 5. Métricas utilizadas

### 5.1 Suporte

O suporte mede a frequência com que um itemset aparece no conjunto total de transações.

```text
suporte(X) = quantidade de transações que contêm X / total de transações
```

Exemplo: se `{Ana Silva, Bruno Costa}` aparece em 5 de 30 atividades, então:

```text
suporte({Ana Silva, Bruno Costa}) = 5 / 30 = 0.166667
```

### 5.2 Confiança

A confiança mede a probabilidade de o consequente aparecer quando o antecedente já aparece.

```text
confiança(A -> B) = suporte(A união B) / suporte(A)
```

Uma confiança igual a `0.80` significa que, em 80% das transações que contêm o antecedente, o consequente também aparece.

### 5.3 Alavancagem

A alavancagem mede o quanto a ocorrência conjunta de dois conjuntos é maior ou menor do que seria esperado caso fossem independentes.

```text
alavancagem(A -> B) = suporte(A união B) - suporte(A) * suporte(B)
```

Valores positivos indicam associação acima do esperado. Valores próximos de zero indicam pouca diferença em relação à independência.

## 6. Descrição dos arquivos do projeto

| Arquivo | Finalidade |
|---|---|
| `3.transactionsParaRegrasAssociacao.txt` | Arquivo de entrada com as atividades e os alunos participantes. |
| `apriori_associacao.py` | Implementação manual do Apriori, cálculo das métricas e geração de recomendações. |
| `apriori_biblioteca.py` | Implementação com a biblioteca `mlxtend`. |
| `test_apriori_associacao.py` | Testes automatizados da implementação manual. |
| `requirements.txt` | Lista de dependências da versão com biblioteca. |
| `README.md` | Instruções rápidas de execução. |
| `resultados/itemsets_manuais.csv` | Itemsets frequentes gerados pela implementação própria. |
| `resultados/regras_manuais.csv` | Regras de associação geradas pela implementação própria. |
| `resultados/itemsets_biblioteca.csv` | Itemsets frequentes gerados com `mlxtend`. |
| `resultados/regras_biblioteca.csv` | Regras de associação geradas com `mlxtend`. |
| `resultados/recomendacoes_exemplo.csv` | Exemplo de recomendação gerado a partir das regras. |

## 7. Funcionamento da implementação manual

### 7.1 Leitura das transações

A função `load_transactions` abre o arquivo de dados, interpreta cada linha como CSV e ignora as duas primeiras colunas. Os nomes dos alunos são armazenados em conjuntos imutáveis (`frozenset`), o que facilita a comparação entre itemsets.

```python
def load_transactions(path: str | Path) -> list[frozenset[str]]:
```

Essa função retorna uma lista de transações, onde cada transação contém somente os alunos participantes.

### 7.2 Cálculo de suporte

A função `support` recebe a lista de transações e um itemset. Ela conta quantas transações contêm todos os itens do itemset e divide esse valor pelo total de transações.

```python
def support(transactions: Iterable[frozenset[str]], itemset: frozenset[str]) -> float:
```

### 7.3 Geração de itemsets frequentes

A função `apriori` implementa o processo central do algoritmo. Primeiro são avaliados os itemsets de tamanho 1. Em seguida, novos candidatos são gerados a partir dos itemsets frequentes da etapa anterior.

```python
def apriori(
    transactions: list[frozenset[str]],
    min_support: float,
    max_size: int = DEFAULT_MAX_SIZE,
) -> dict[frozenset[str], float]:
```

O princípio do Apriori é utilizado na função `_next_candidates`: um itemset candidato só é considerado se todos os seus subconjuntos imediatos também forem frequentes. Isso reduz o número de combinações analisadas.

### 7.4 Geração das regras de associação

A função `generate_association_rules` percorre os itemsets frequentes e separa cada itemset em antecedente e consequente. Para cada regra possível, são calculadas as métricas de suporte, confiança e alavancagem.

```python
def generate_association_rules(
    frequent_itemsets: dict[frozenset[str], float],
    min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    max_union_size: int = DEFAULT_MAX_SIZE,
    antecedent_sizes: set[int] | None = None,
    consequent_sizes: set[int] | None = None,
) -> list[Rule]:
```

Neste trabalho, foram aceitos antecedentes de tamanho 1 ou 2 e consequentes de tamanho 1. Assim, são geradas regras como:

```text
{Ana Silva} -> {Bruno Costa}
{Ana Silva, Bruno Costa} -> {Kleber Santos}
```

### 7.5 Sistema simples de recomendação

A função `recommend_participants` recebe um conjunto de alunos já inscritos em uma atividade e consulta as regras de associação. Quando o antecedente de uma regra está contido no conjunto de inscritos, o consequente pode ser recomendado.

```python
def recommend_participants(
    enrolled: set[str],
    rules: list[Rule],
    top_n: int = 5,
) -> list[dict[str, float | str]]:
```

O resultado é ordenado por confiança, alavancagem e suporte.

## 8. Funcionamento da implementação com biblioteca

O arquivo `apriori_biblioteca.py` utiliza a biblioteca `mlxtend`. Primeiro, as transações são convertidas para uma matriz booleana por meio do `TransactionEncoder`. Cada coluna representa um aluno, e cada linha representa uma atividade.

Depois disso, são utilizadas duas funções principais:

```python
from mlxtend.frequent_patterns import apriori, association_rules
```

A função `apriori` gera os itemsets frequentes, e a função `association_rules` calcula as regras de associação. Por fim, o código aplica os mesmos filtros da implementação manual: tamanho máximo de itemset igual a 3, antecedente de tamanho 1 ou 2 e consequente de tamanho 1.

## 9. Resultados obtidos

Com os parâmetros definidos, foram encontrados:

| Resultado | Quantidade |
|---|---:|
| Itemsets frequentes | 45 |
| Regras de pares | 27 |
| Regras de pares com terceiro aluno | 3 |

As três regras do tipo par com terceiro aluno foram:

| Antecedente | Consequente | Suporte | Confiança | Alavancagem |
|---|---|---:|---:|---:|
| `{Ana Silva, Kleber Santos}` | `{Bruno Costa}` | 0.133333 | 0.800000 | 0.083333 |
| `{Bruno Costa, Kleber Santos}` | `{Ana Silva}` | 0.133333 | 0.800000 | 0.077778 |
| `{Ana Silva, Bruno Costa}` | `{Kleber Santos}` | 0.133333 | 0.666667 | 0.073333 |

Um exemplo de recomendação gerada pelo sistema foi:

```text
Alunos inscritos: {Ana Silva, Bruno Costa}
Aluno recomendado: Kleber Santos
Regra utilizada: {Ana Silva, Bruno Costa} -> {Kleber Santos}
Confiança: 0.666667
```

Isso indica que, quando Ana Silva e Bruno Costa aparecem juntos, Kleber Santos também aparece em parte relevante dessas situações.

## 10. Comparação entre as abordagens

Os arquivos gerados pela implementação manual e pela biblioteca foram comparados. Os resultados foram equivalentes:

- `itemsets_manuais.csv` possui o mesmo conteúdo de `itemsets_biblioteca.csv`.
- `regras_manuais.csv` possui o mesmo conteúdo de `regras_biblioteca.csv`.

Essa equivalência indica que a implementação manual seguiu corretamente a lógica esperada para o algoritmo Apriori e para o cálculo das regras de associação.

## 11. Como executar o projeto

Para instalar as dependências:

```bash
python -m pip install -r requirements.txt
```

Para executar a implementação manual:

```bash
python apriori_associacao.py
```

Para executar a implementação com biblioteca:

```bash
python apriori_biblioteca.py
```

Para executar os testes:

```bash
python -m unittest test_apriori_associacao.py
```

## 12. Testes realizados

O arquivo `test_apriori_associacao.py` contém testes automatizados para verificar os principais comportamentos da implementação própria:

- Leitura correta do arquivo, ignorando id e descrição.
- Cálculo correto do suporte.
- Geração de itemsets frequentes.
- Geração de regras com suporte, confiança e alavancagem.
- Funcionamento do mecanismo simples de recomendação.

Os testes foram executados com o módulo `unittest`, nativo do Python.

## 13. Conclusão

O trabalho demonstrou a aplicação do algoritmo Apriori para identificar padrões de associação entre alunos participantes de atividades extracurriculares. A implementação manual permitiu compreender as etapas internas do algoritmo, como geração de candidatos, filtragem por suporte mínimo e criação de regras. A versão com a biblioteca `mlxtend` serviu como validação dos resultados, já que produziu os mesmos itemsets e regras.

Os resultados mostram que há grupos de alunos com participação recorrente em conjunto, especialmente envolvendo Ana Silva, Bruno Costa e Kleber Santos. Essas regras podem ser utilizadas como base para um sistema simples de recomendação de participantes em novas atividades.

## 14. Referências

AGRAWAL, Rakesh; IMIELINSKI, Tomasz; SWAMI, Arun. Mining association rules between sets of items in large databases. In: Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data. 1993.

MLXTEND. Apriori: frequent itemsets via the Apriori algorithm. Disponível em: <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/>. Acesso em: 08 maio 2026.

MLXTEND. Association Rules. Disponível em: <https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/>. Acesso em: 08 maio 2026.

PYTHON SOFTWARE FOUNDATION. Python 3 Documentation. Disponível em: <https://docs.python.org/3/>. Acesso em: 08 maio 2026.
