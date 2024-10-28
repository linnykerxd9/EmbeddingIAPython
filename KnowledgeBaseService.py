import PyPDF2
import re

# Lista de nomes dos livros da Bíblia
nomes_livros_biblia = [
    "GENESIS", "EXODO", "LEVITICO", "NUMEROS", "DEUTERONOMIO",
    "JOSUE", "JUIZES", "RUTE", "1 SAMUEL", "2 SAMUEL", "1 REIS", "2 REIS",
    "1 CRONICAS", "2 CRONICAS", "ESDRAS", "NEEMIAS", "ESTER", "JO", "SALMOS",
    "PROVERBIOS", "ECLESIASTES", "CANTICOS", "ISAIAS", "JEREMIAS", "LAMENTACOES",
    "EZEQUIEL", "DANIEL", "OSEIAS", "JOEL", "AMOS", "OBADIAS", "JONAS", "MIQUEIAS",
    "NAUM", "HABACUQUE", "SOFONIAS", "AGEU", "ZACARIAS", "MALAQUIAS",
    "MATEUS", "MARCOS", "LUCAS", "JOAO", "ATOS", "ROMANOS", "1 CORINTIOS",
    "2 CORINTIOS", "GALATAS", "EFEZIOS", "FILIPENSES", "COLOSSENSES",
    "1 TESSALONICENSES", "2 TESSALONICENSES", "1 TIMOTEO", "2 TIMOTEO",
    "TITO", "FILEMOM", "HEBREUS", "TIAGO", "1 PEDRO", "2 PEDRO", "1 JOAO",
    "2 JOAO", "3 JOAO", "JUDAS", "APOCALIPSE"
]

# Cria uma expressão regular que combina todos os nomes dos livros da Bíblia
regex_livros_biblia = re.compile(r'\b(' + '|'.join(nomes_livros_biblia) + r')\b', re.IGNORECASE)

def ler_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = ""
        
        # Itera sobre todas as páginas e extrai o texto
        for pagina in range(len(leitor_pdf.pages)):
            pagina_atual = leitor_pdf.pages[pagina]
            teste = len(leitor_pdf.pages)
            texto_pagina = pagina_atual.extract_text()
            
            # Remove quebras de linha indesejadas
            texto_pagina = re.sub(r'\n+', ' ', texto_pagina)

            # Adiciona uma quebra de linha antes de todos os números
            texto_pagina = re.sub(r'(?<!\d)(\d)', r'\n\1', texto_pagina)

            # Remove a quebra de linha antes dos números que seguem "Capítulo" com múltiplos espaços
            texto_pagina = re.sub(r'(capítulo\s*)\n(\d)', r'\1\2', texto_pagina, flags=re.IGNORECASE)


            # Adiciona uma quebra de linha antes da palavra "capitulo"
            texto_pagina = re.sub(r'\b(capítulo)\b', r'\n\1', texto_pagina, flags=re.IGNORECASE)

            # Adiciona uma quebra de linha ao final da primeira página
            if pagina == 0:
                texto_pagina += '\n'
            
            texto_completo += texto_pagina
    
    return texto_completo

def separar_livro_capitulo_versiculo(texto_biblia):
    biblia_dict = {}
    livro_atual = None
    capitulo_atual = None
    linhas = texto_biblia.split('\n')
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()

        # Se a linha tiver menos de 10 caracteres, junte com a linha anterior e continue
        if len(linha) < 10 and i > 0:
            linhas[i - 1] += ' ' + linha
            continue
        
        # Verifica se é o início de um novo capítulo
        capitulo_match = re.match(r'Capítulo  (\d+)', linha, re.IGNORECASE)
        if capitulo_match:
            capitulo_atual = int(capitulo_match.group(1))
            if capitulo_atual == 1:
                livro_possivel_anterior = linhas[i - 1].strip() if i > 0 else ""
                livro_possivel_atual = linha
                
                # Verifica se a linha anterior contém "O SANTO EVANGELHO SEGUNDO"
                    # Extrai a próxima palavra após "O SANTO EVANGELHO SEGUNDO"
                match = re.search(r'O\s+SANTO\s+EVANGELHO\s+SEGUNDO\s+(\w+)', livro_possivel_anterior, re.IGNORECASE)
                # Remove caracteres minúsculos
                if match:
                    livro_nome = match.group(1)
                    livro_nome = re.sub(r'[a-z]', '', livro_nome)
                    if livro_nome.upper() in nomes_livros_biblia:
                        livro_atual = livro_nome
                        biblia_dict[livro_atual] = {}
                
                # Extrai a próxima palavra após "O SANTO EVANGELHO SEGUNDO"
                match = re.search(r'O\s+SANTO\s+EVANGELHO\s+SEGUNDO\s+(\w+)', livro_possivel_atual, re.IGNORECASE)
                if match:
                    livro_nome = match.group(1)
                    # Remove caracteres minúsculos
                    livro_nome = re.sub(r'[a-z]', '', livro_nome)
                    if livro_nome.upper() in nomes_livros_biblia:
                        livro_atual = livro_nome
                        biblia_dict[livro_atual] = {}

        # Verifica se a linha começa com um número (versículo)
        versiculo_match = re.match(r'(\d+)', linha)
        if versiculo_match:
            versiculo_atual = int(versiculo_match.group(1))
            linha = linha[len(versiculo_match.group(1)):].strip()  # Remove o número do início da linha
        else:
            versiculo_atual = 1  # Se não começar com um número, usa 'i' como versículo
        
        # Adiciona a linha ao dicionário, mesmo que não corresponda a um capítulo ou versículo
        if livro_atual and capitulo_atual:
            if capitulo_atual not in biblia_dict[livro_atual]:
                biblia_dict[livro_atual][capitulo_atual] = {}
            if versiculo_atual not in biblia_dict[livro_atual][capitulo_atual]:
                biblia_dict[livro_atual][capitulo_atual][versiculo_atual] = []
            biblia_dict[livro_atual][capitulo_atual][versiculo_atual].append(linha)
        else:
            if 'Biblia' not in biblia_dict:
                biblia_dict['Biblia'] = {}
            if i not in biblia_dict['Biblia']:
                biblia_dict['Biblia'][i] = {}
            if versiculo_atual not in biblia_dict['Biblia'][i]:
                biblia_dict['Biblia'][i][versiculo_atual] = []
            biblia_dict['Biblia'][i][versiculo_atual].append(linha)
    
    return biblia_dict




    