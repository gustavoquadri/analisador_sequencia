import requests
from requests.exceptions import RequestException


def buscar_sequencia_ncbi(accession_id):
    """
    busca uma sequência real no banco de dados do NCBI usando o ID de acesso.
    """
    try:
        print(f"\nBuscando sequência {accession_id} no NCBI...")

        # endereço da API do banco de dados NCBI
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db': 'nucleotide',  # banco de nucleotídeos
            'id': accession_id,  # o ID fornecido
            'rettype': 'fasta',  # formato FASTA
            'retmode': 'text'    # texto simples
        }

        # faz a requisição para o NCBI e espera até 10 segundos
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # se der erro, para aqui

        # formato FASTA, retorna com um cabeçalho (linha com >) e depois as linhas com a sequência. 
        # o necessario é somente a sequência, então o uso do .split(quebra de linha)
        linhas = response.text.strip().split('\n')
        # ignora as linhas que começam com '>' (cabeçalho) e junta o resto
        sequencia = ''.join([linha for linha in linhas if not linha.startswith('>')])
        sequencia = sequencia.upper().replace(' ', '').replace('\n', '')

        if sequencia:
            print(f"Sequência encontrada! ({len(sequencia)} bases)")
            return sequencia
        else:
            print("Erro: Sequência não encontrada ou vazia.")
            return None

    except RequestException as e:
        print(f"Erro ao buscar sequência: {e}")
        print("   Verifique sua conexão com a internet e o ID de acesso.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None


def validar_dna(sequencia):
    """
    verifica se a sequencia é DNA (só pode ter as bases A, T, C e G. se tiver qualquer outra coisa, não é DNA válido).
    """
    bases_validas = {'A', 'T', 'C', 'G'}
    for base in sequencia:
        if base not in bases_validas:
            return False  # nao é DNA
    return True  # é DNA


def validar_rna(sequencia):
    """
    verifica se a sequência é realmente RNA (só pode ter A, U, C e G).
    """
    bases_validas = {'A', 'U', 'C', 'G'}
    for base in sequencia:
        if base not in bases_validas:
            return False  # nao é RNA
    return True  # é RNA


def contar_bases(sequencia):
    """
    conta quantas vezes cada base aparece na sequência.
    """
    contagem = {}
    for base in sequencia:
        if base in contagem:
            contagem[base] += 1  # se ja apareceu conta +1
        else:
            contagem[base] = 1  # se é a primeira vez valor == 1
    return contagem


def calcular_conteudo_gc(sequencia):
    """
    calcula percentual da sequencia que é formado por G e C juntos.
    GC é importante porque diz muito sobre a estabilidade da sequência.
    """
    if len(sequencia) == 0:
        return 0  # se a sequencia for vazia retorna 0

    # conta quantas vezes G e C aparecem
    g = sequencia.count('G')
    c = sequencia.count('C')
    total = len(sequencia)

    # calcula a porcentagem
    porcentagem_gc = ((g + c) / total) * 100
    return round(porcentagem_gc, 2)  # arredonda para 2 casas decimais


def transcrever_dna_para_rna(sequencia_dna):
    """
    Converte DNA para RNA, troca todas as T (timina) por U (uracila).
    """
    rna = sequencia_dna.replace('T', 'U')
    return rna


def calcular_tamanho_sequencia(sequencia):
    """
    apenas conta quantas bases a sequencia tem
    """
    return len(sequencia)


def exibir_relatorio(sequencia, tipo='DNA'):
    """
    mostra um relatorio de informações sobre a sequencia
    """
    print("\n" + "="*60)
    print("RELATÓRIO DE ANÁLISE DE SEQUÊNCIA")
    print("="*60)

    # mostra o tipo da sequencia
    print(f"\nTipo de sequência: {tipo}")

    # quantas bases tem no total
    tamanho = calcular_tamanho_sequencia(sequencia)
    print(f"Tamanho da sequência: {tamanho} bases")

    # conta cada tipo de base e mostra o percentual
    print("\n--- Contagem de Bases ---")
    contagem = contar_bases(sequencia)
    for base in sorted(contagem.keys()):
        porcentagem = (contagem[base] / tamanho) * 100
        print(f"  {base}: {contagem[base]} ({porcentagem:.2f}%)")

    # só calcula GC para DNA (RNA não tem esse conceito da mesma forma)
    if tipo == 'DNA':
        gc = calcular_conteudo_gc(sequencia)
        print(f"\nConteúdo GC: {gc}%")

    # mostra os primeiros 20 caracteres e os ultimas 20 caso seja maior
    print(f"\nPrimeiros 20 caracteres: {sequencia[:20]}")
    if len(sequencia) > 20:
        print(f"Últimos 20 caracteres: {sequencia[-20:]}")


def salvar_resultado(arquivo_saida, conteudo):
    """
    salva o resultado em um arquivo de texto.
    """
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"\nResultado salvo em: {arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


def menu_principal():
    """
    menu com as opções
    """
    print("\n" + "="*60)
    print("ANALISADOR DE SEQUÊNCIAS DE DNA/RNA")
    print("="*60)
    print("\nOpções disponíveis:")
    print("1. Analisar sequência digitada")
    print("2. Buscar sequência no NCBI (via API)")
    print("3. Transcrever DNA para RNA")
    print("4. Sair")

    opcao = input("\nEscolha uma opção (1-4): ").strip()
    return opcao


def main():
    """
    loop principal para o menu principal
    """
    sequencia_atual = None  # guarda a sequencia atual sendo usada
    tipo_atual = None       # guarda o tipo (RNA ou DNA)

    while True:
        opcao = menu_principal()

        if opcao == '1':
            # sequencia digitada manualmente
            sequencia = input("\nDigite a sequência: ").strip().upper()  # .strip() remove os espaços em branco no inicio e no fim, e o .upper() deixa tudo maiusculo
            sequencia = sequencia.replace(' ', '').replace('\n', '')  # limpa outros espaços em branco e quebras de texto

            if sequencia:
                if validar_dna(sequencia):
                    tipo_atual = 'DNA'
                    sequencia_atual = sequencia
                    print("\nSequência de DNA válida!")
                    exibir_relatorio(sequencia_atual, tipo_atual)
                elif validar_rna(sequencia):
                    tipo_atual = 'RNA'
                    sequencia_atual = sequencia
                    print("\nSequência de RNA válida!")
                    exibir_relatorio(sequencia_atual, tipo_atual)
                else:
                    print("\nAviso: Sequência contém caracteres inválidos!")
                    sequencia_atual = sequencia
                    tipo_atual = 'Desconhecido'
            else:
                print("\nErro: Sequência vazia!")

        elif opcao == '2':
            # sequencia real no banco de dados do NCBI
            print("\n--- Buscar Sequência no NCBI ---")
            print("\nNCBI = National Center for Biotechnology Information")
            print("Banco de dados público de sequências biológicas")
            print("\nExemplos de IDs de acesso:")
            print("  - NM_000207.3 (RNA mensageiro - gene da insulina humana)")
            print("  - NC_000001.11 (Cromossomo 1 humano)")
            print("  - NC_000913.3 (Genoma completo de E. coli)")
            print("\nTipos comuns:")
            print("  NM_ = RNA mensageiro (mRNA)")
            print("  NC_ = Cromossomo completo")
            print("  NG_ = Gene ou região genômica")
            print("  NR_ = RNA não codificante")

            accession_id = input("\nDigite o ID de acesso do NCBI: ").strip()

            if accession_id:
                sequencia = buscar_sequencia_ncbi(accession_id)
                if sequencia:
                    if validar_dna(sequencia):
                        tipo_atual = 'DNA'
                        sequencia_atual = sequencia
                        exibir_relatorio(sequencia_atual, tipo_atual)
                    elif validar_rna(sequencia):
                        tipo_atual = 'RNA'
                        sequencia_atual = sequencia
                        exibir_relatorio(sequencia_atual, tipo_atual)
                    else:
                        print("\nAviso: Sequência contém caracteres não padrão.")
                        sequencia_atual = sequencia
                        tipo_atual = 'Desconhecido'
            else:
                print("\nErro: ID de acesso vazio!")

        elif opcao == '3':
            # converter DNA para RNA
            if sequencia_atual is None:
                print("\nErro: Nenhuma sequência carregada!")
                print("   Primeiro carregue uma sequência (opção 1 ou 2)")
                continue

            if tipo_atual != 'DNA':
                print("\nAviso: Esta função é para sequências de DNA!")
                print("\nCarregue uma sequência DNA válida para utilizar essa função.")
            else:
                rna = transcrever_dna_para_rna(sequencia_atual)
                print("\n--- Transcrição DNA → RNA ---")
                # mostra só os primeiros 50 caracteres se a sequência for muito longa
                print(f"DNA: {sequencia_atual[:50]}..." if len(sequencia_atual) > 50 else f"DNA: {sequencia_atual}")
                print(f"RNA: {rna[:50]}..." if len(rna) > 50 else f"RNA: {rna}")

                salvar = input("\nDeseja salvar o RNA em um arquivo? (s/n): ").strip().lower()
                if salvar == 's':
                    arquivo = input("Nome do arquivo de saída: ").strip()
                    salvar_resultado(arquivo, rna)

        elif opcao == '4':
            # sair do programa
            print("\nEncerrando programa...")
            break

        else:
            # Opção inválida - foi digitado uma opção que não existe
            print("\nOpção inválida! Escolha um número de 1 a 4.")


# executar o programa
if __name__ == "__main__":
    main()
