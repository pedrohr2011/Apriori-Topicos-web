# Apriori - regras de associacao

Trabalho da disciplina de Topicos Especiais em Desenvolvimento Web.

> A documentacao em formato de trabalho universitario esta em `DOCUMENTACAO_TRABALHO.md`.

Este projeto resolve a atividade com duas abordagens:

1. `apriori_associacao.py`: implementacao do Apriori do zero em Python.
2. `apriori_biblioteca.py`: execucao equivalente usando a biblioteca `mlxtend`.

## Criterios usados

- Arquivo de entrada: `3.transactionsParaRegrasAssociacao.txt`
- Cada linha e uma transacao/atividade.
- As duas primeiras colunas sao ignoradas: id e descricao.
- Os demais campos da linha sao tratados como alunos participantes.
- Suporte minimo: `0.10`, ou seja, pelo menos 3 das 30 transacoes.
- Confianca minima para exportar regras: `0.50`.
- Tamanho maximo dos itemsets: 3, cobrindo pares e pares com um terceiro aluno.

Metricas:

- Suporte: proporcao de atividades em que o itemset aparece.
- Confianca: `suporte(A uniao B) / suporte(A)`.
- Alavancagem: `suporte(A uniao B) - suporte(A) * suporte(B)`.

## Como executar

Instale as dependencias da versao com biblioteca:

```bash
python -m pip install -r requirements.txt
```

Rode a implementacao manual:

```bash
python apriori_associacao.py
```

Rode a versao com biblioteca:

```bash
python apriori_biblioteca.py
```

Rode os testes da implementacao manual:

```bash
python -m unittest test_apriori_associacao.py
```

## Arquivos gerados

Os resultados ficam na pasta `resultados/`:

- `itemsets_manuais.csv`
- `regras_manuais.csv`
- `itemsets_biblioteca.csv`
- `regras_biblioteca.csv`
- `recomendacoes_exemplo.csv`

Com os parametros padrao, foram encontrados:

- 45 itemsets frequentes.
- 27 regras de pares.
- 3 regras de pares com um terceiro aluno.

Exemplo de regra de recomendacao encontrada:

```text
{Ana Silva, Bruno Costa} -> {Kleber Santos}
suporte = 0.133333, confianca = 0.666667, alavancagem = 0.073333
```

Nesse exemplo, se Ana Silva e Bruno Costa estiverem inscritos em uma nova atividade, Kleber Santos pode ser recomendado como participante potencial.
