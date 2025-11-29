
try:
    import requests
    REQUESTS_DISPONIVEL = True
except ImportError:
    REQUESTS_DISPONIVEL = False
    print("⚠ Aviso: Biblioteca 'requests' não instalada.")
    print("   Para usar busca via API, instale com: pip install requests")

def ler_sequencia(arquivo):
    """
    Lê uma sequência de DNA/RNA de um arquivo de texto.
    Limpa a sequência removendo espaços e quebras de linha, e deixa tudo em maiúsculas.
    """
    try:
        with open(arquivo, 'r') as f:
            sequencia = f.read().strip().upper()
            # Tira qualquer quebra de linha ou espaço que possa ter no meio da sequência
            sequencia = sequencia.replace('\n', '').replace(' ', '')
        return sequencia
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado!")
        return None
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None


def buscar_sequencia_ncbi(accession_id):
    """
    Busca uma sequência real no banco de dados do NCBI usando o ID de acesso.
    Por exemplo, se você passar 'NM_000207.3', vai buscar essa sequência específica.
    """
    if not REQUESTS_DISPONIVEL:
        print("\n⚠ Erro: Biblioteca 'requests' não está instalada!")
        print("   Instale com: pip install requests")
        return None
    
    try:
        print(f"\nBuscando sequência {accession_id} no NCBI...")
        
        # Endereço da API do NCBI que fornece as sequências
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db': 'nucleotide',  # Queremos buscar no banco de nucleotídeos
            'id': accession_id,  # O ID que o usuário forneceu
            'rettype': 'fasta',  # Queremos o formato FASTA
            'retmode': 'text'    # Em formato texto simples
        }
        
        # Faz a requisição para o NCBI e espera até 10 segundos
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Se der erro, para aqui
        
        # O NCBI retorna no formato FASTA, que tem um cabeçalho (linha com >)
        # e depois as linhas com a sequência. Vamos pegar só a sequência.
        linhas = response.text.strip().split('\n')
        # Ignora as linhas que começam com '>' (cabeçalho) e junta o resto
        sequencia = ''.join([linha for linha in linhas if not linha.startswith('>')])
        sequencia = sequencia.upper().replace(' ', '').replace('\n', '')
        
        if sequencia:
            print(f"✓ Sequência encontrada! ({len(sequencia)} bases)")
            return sequencia
        else:
            print("⚠ Erro: Sequência não encontrada ou vazia.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"⚠ Erro ao buscar sequência: {e}")
        print("   Verifique sua conexão com a internet e o ID de acesso.")
        return None
    except Exception as e:
        print(f"⚠ Erro inesperado: {e}")
        return None


def buscar_sequencia_exemplo():
    """
    Retorna uma sequência de exemplo para quando você quer testar
    mas não tem acesso à internet ou não quer buscar no NCBI.
    """
    # Uma sequência fictícia só para demonstração
    sequencia_exemplo = (
        "ATGCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"
        "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"
        "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"
    )
    print("\n✓ Usando sequência de exemplo para demonstração.")
    return sequencia_exemplo


def validar_dna(sequencia):
    """
    Verifica se a sequência é realmente DNA.
    DNA só pode ter as bases A, T, C e G. Se tiver qualquer outra coisa, não é DNA válido.
    """
    bases_validas = {'A', 'T', 'C', 'G'}
    for base in sequencia:
        if base not in bases_validas:
            return False  # Encontrou uma base inválida, então não é DNA
    return True  # Todas as bases são válidas, é DNA!


def validar_rna(sequencia):
    """
    Verifica se a sequência é realmente RNA.
    RNA tem A, U, C e G (note que é U, não T como no DNA).
    """
    bases_validas = {'A', 'U', 'C', 'G'}
    for base in sequencia:
        if base not in bases_validas:
            return False  # Encontrou uma base inválida
    return True  # É RNA válido!


def contar_bases(sequencia):
    """
    Conta quantas vezes cada base aparece na sequência.
    Por exemplo, se tiver "AATCG", vai retornar: {'A': 2, 'T': 1, 'C': 1, 'G': 1}
    """
    contagem = {}
    for base in sequencia:
        if base in contagem:
            contagem[base] += 1  # Já vi essa base antes, soma mais um
        else:
            contagem[base] = 1  # Primeira vez que vejo essa base
    return contagem


def calcular_conteudo_gc(sequencia):
    """
    Calcula quanto por cento da sequência é formado por G e C juntos.
    O conteúdo GC é importante porque diz muito sobre a estabilidade da sequência.
    """
    if len(sequencia) == 0:
        return 0  # Sequência vazia não tem conteúdo GC
    
    # Conta quantas G e quantas C tem na sequência
    g = sequencia.count('G')
    c = sequencia.count('C')
    total = len(sequencia)
    
    # Calcula a porcentagem: (G + C) / total * 100
    porcentagem_gc = ((g + c) / total) * 100
    return round(porcentagem_gc, 2)  # Arredonda para 2 casas decimais


def transcrever_dna_para_rna(sequencia_dna):
    """
    Converte DNA para RNA. É simples: só troca todas as T (timina) por U (uracila).
    É assim que funciona na célula também - quando o DNA é transcrito para RNA!
    """
    rna = sequencia_dna.replace('T', 'U')
    return rna


def gerar_complemento_reverso(sequencia):
    """
    Cria a fita complementar reversa do DNA.
    Primeiro faz o complemento (A vira T, T vira A, C vira G, G vira C),
    depois inverte tudo de trás pra frente.
    """
    # Dicionário que diz qual base é complemento de qual
    complemento = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    complemento_reverso = ''
    
    # Para cada base, pega o complemento e coloca na frente (isso inverte)
    for base in sequencia:
        if base in complemento:
            complemento_reverso = complemento[base] + complemento_reverso
    
    return complemento_reverso


def encontrar_motivos(sequencia, motivo):
    """
    Procura um padrão específico (motivo) dentro da sequência.
    Por exemplo, se você procurar "ATC" em "GATCGATC", vai achar nas posições 2 e 6.
    Retorna uma lista com todas as posições onde o motivo aparece (começando do 1, não do 0).
    """
    posicoes = []
    motivo = motivo.upper()  # Deixa tudo maiúsculo para não ter problema
    sequencia_upper = sequencia.upper()
    
    # Vai deslizando pela sequência, comparando pedaços do tamanho do motivo
    for i in range(len(sequencia_upper) - len(motivo) + 1):
        if sequencia_upper[i:i+len(motivo)] == motivo:
            posicoes.append(i + 1)  # +1 porque queremos começar contando do 1, não do 0
    
    return posicoes


def calcular_tamanho_sequencia(sequencia):
    """
    Simplesmente conta quantas bases tem na sequência.
    """
    return len(sequencia)


def exibir_relatorio(sequencia, tipo='DNA'):
    """
    Mostra um relatório bonito com todas as informações importantes sobre a sequência.
    """
    print("\n" + "="*60)
    print("RELATÓRIO DE ANÁLISE DE SEQUÊNCIA")
    print("="*60)
    
    # Mostra se é DNA ou RNA
    print(f"\nTipo de sequência: {tipo}")
    
    # Quantas bases tem no total
    tamanho = calcular_tamanho_sequencia(sequencia)
    print(f"Tamanho da sequência: {tamanho} bases")
    
    # Conta cada tipo de base e mostra a porcentagem
    print("\n--- Contagem de Bases ---")
    contagem = contar_bases(sequencia)
    for base in sorted(contagem.keys()):
        porcentagem = (contagem[base] / tamanho) * 100
        print(f"  {base}: {contagem[base]} ({porcentagem:.2f}%)")
    
    # Só calcula GC para DNA (RNA não tem esse conceito da mesma forma)
    if tipo == 'DNA':
        gc = calcular_conteudo_gc(sequencia)
        print(f"\nConteúdo GC: {gc}%")
    
    # Mostra um pedaço do começo e do fim para você ter uma ideia da sequência
    print(f"\nPrimeiros 20 caracteres: {sequencia[:20]}")
    if len(sequencia) > 20:
        print(f"Últimos 20 caracteres: {sequencia[-20:]}")


def salvar_resultado(arquivo_saida, conteudo):
    """
    Salva o resultado (por exemplo, uma sequência de RNA transcrita) em um arquivo de texto.
    """
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"\nResultado salvo em: {arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


def menu_principal():
    """
    Mostra o menu principal com todas as opções disponíveis e pede para o usuário escolher.
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
    Função principal - é aqui que tudo acontece!
    Fica em loop mostrando o menu e processando as escolhas do usuário.
    """
    sequencia_atual = None  # Guarda a sequência que está sendo trabalhada agora
    tipo_atual = None       # Guarda se é DNA, RNA ou desconhecido
    
    while True:
        opcao = menu_principal()
        
        if opcao == '1':
            # Usuário quer digitar uma sequência manualmente
            sequencia = input("\nDigite a sequência: ").strip().upper()
            sequencia = sequencia.replace(' ', '').replace('\n', '')  # Limpa espaços e quebras
            
            if sequencia:
                if validar_dna(sequencia):
                    tipo_atual = 'DNA'
                    sequencia_atual = sequencia
                    print(f"\n✓ Sequência de DNA válida!")
                    exibir_relatorio(sequencia_atual, tipo_atual)
                elif validar_rna(sequencia):
                    tipo_atual = 'RNA'
                    sequencia_atual = sequencia
                    print(f"\n✓ Sequência de RNA válida!")
                    exibir_relatorio(sequencia_atual, tipo_atual)
                else:
                    print("\n⚠ Aviso: Sequência contém caracteres inválidos!")
                    sequencia_atual = sequencia
                    tipo_atual = 'Desconhecido'
            else:
                print("\nErro: Sequência vazia!")
        
        elif opcao == '2':
            # Usuário quer buscar uma sequência real no banco de dados do NCBI
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
                        print("\n⚠ Aviso: Sequência contém caracteres não padrão.")
                        sequencia_atual = sequencia
                        tipo_atual = 'Desconhecido'
            else:
                print("\nErro: ID de acesso vazio!")
        
        elif opcao == '3':
            # Usuário quer converter DNA para RNA
            if sequencia_atual is None:
                print("\n⚠ Erro: Nenhuma sequência carregada!")
                print("   Primeiro carregue uma sequência (opção 1 ou 2)")
                continue
            
            if tipo_atual != 'DNA':
                print("\n⚠ Aviso: Esta função é para sequências de DNA!")
            
            rna = transcrever_dna_para_rna(sequencia_atual)
            print("\n--- Transcrição DNA → RNA ---")
            # Mostra só os primeiros 50 caracteres se a sequência for muito longa
            print(f"DNA: {sequencia_atual[:50]}..." if len(sequencia_atual) > 50 else f"DNA: {sequencia_atual}")
            print(f"RNA: {rna[:50]}..." if len(rna) > 50 else f"RNA: {rna}")
            
            salvar = input("\nDeseja salvar o RNA em um arquivo? (s/n): ").strip().lower()
            if salvar == 's':
                arquivo = input("Nome do arquivo de saída: ").strip()
                salvar_resultado(arquivo, rna)
        
        elif opcao == '4':
            # Usuário quer sair do programa
            print("\nEncerrando programa...")
            break
        
        else:
            # Opção inválida - o usuário digitou algo que não existe
            print("\n⚠ Opção inválida! Escolha um número de 1 a 4.")


# Executar o programa
if __name__ == "__main__":
    main()

