# Analisador de Sequências de DNA/RNA

Programa em Python para análise básica de sequências biológicas, desenvolvido para a disciplina de Bioinformática.

## Funcionalidades

1. **Análise de Sequências**
   - Entrada manual de sequências de DNA/RNA
   - Busca de sequências via API do NCBI
   - Validação automática de sequências (DNA ou RNA)
   - Contagem de bases nitrogenadas com porcentagem
   - Cálculo do conteúdo GC (Guanina + Citosina)
   - Relatório completo da análise

2. **Transcrição**
   - Conversão de DNA para RNA
   - Opção de salvar resultado em arquivo

## Instalação

### Requisitos:
- Python 3.6 ou superior
- Biblioteca `requests`

### Instalar dependências:
```bash
pip install requests
```

## Como Usar

### Executar o programa:
```bash
python analisador_sequencias.py
```

### Opções do Menu:
1. **Analisar sequência digitada**: Permite digitar a sequência diretamente
2. **Buscar sequência no NCBI (via API)**: Busca sequências reais do banco de dados NCBI
3. **Transcrever DNA para RNA**: Converte DNA em RNA
4. **Sair**: Encerra o programa

### Buscar Sequências via API (Opção 2):
O programa pode buscar sequências reais do banco de dados NCBI usando IDs de acesso.

**Exemplos de IDs de acesso:**
- `NM_000207.3` - RNA mensageiro (INS - gene da insulina)
- `NC_000001.11` - Cromossomo 1 humano
- `M10051.1` - Sequência genômica

**Como usar:**
1. Escolha a opção 2 no menu
2. Digite o ID de acesso do NCBI
3. O programa buscará e analisará a sequência automaticamente

**Nota:** É necessária conexão com a internet para usar esta funcionalidade.

## Exemplo de Uso

### Análise de Sequência Digitada:
1. Execute o programa
2. Escolha a opção 1
3. Digite a sequência (ex: `ATGCGATCGATCGATCG`)
4. O programa validará e mostrará um relatório completo com:
   - Tipo de sequência (DNA ou RNA)
   - Tamanho em bases
   - Contagem de cada base com porcentagem
   - Conteúdo GC (para DNA)
   - Primeiros e últimos 20 caracteres

### Transcrição DNA para RNA:
1. Primeiro, carregue uma sequência (opção 1 ou 2)
2. Escolha a opção 3
3. O programa converterá T por U
4. Opcionalmente, salve o resultado em arquivo
