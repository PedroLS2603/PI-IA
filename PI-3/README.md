# Treinamento de agente por Q-Learning para MsPacman 

### Instalação de dependências
```pip install -r requirements.txt```

### Executando arquivo

#### args

arg | descrição | tipo | padrão
:-: | :-: | :-: | :-:
eps | Número de ciclos para treinamento | int | 10
load | Nome do arquivo que contém a QTable a ser utilizada | string | ultima q_table salva
dict | Modo de treinamento: arquivo pré-existente ou criar novo | string | ram 

##### dict
 * ram: cria novas tabelas e salva na pasta "q_tables"
 * disk: carrega arquivo especificado da pasta "q_tables"


#### Exemplo

```python main.py --eps 1000 --load q_table3```


