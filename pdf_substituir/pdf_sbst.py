from pypdf import PdfReader, PdfWriter


def substituir_pagina(
    ficheiro_base: str,
    ficheiro_substituto: str,
    pagina_alvo: int,
    pagina_substituta: int,
    ficheiro_saida: str
) -> None:
    """
    Substitui uma pagina do PDF base por uma pagina de outro PDF.

    pagina_alvo e pagina_substituta sao numeros de pagina em modo "humano" (1, 2, 3, ...).
    """

    # Ler os PDFs
    base_reader = PdfReader(ficheiro_base)
    subst_reader = PdfReader(ficheiro_substituto)

    num_paginas_base = len(base_reader.pages)
    num_paginas_subst = len(subst_reader.pages)

    # Validacoes basicas
    if pagina_alvo < 1 or pagina_alvo > num_paginas_base:
        raise ValueError(
            f"pagina_alvo fora de intervalo. PDF base tem {num_paginas_base} paginas."
        )

    if pagina_substituta < 1 or pagina_substituta > num_paginas_subst:
        raise ValueError(
            f"pagina_substituta fora de intervalo. PDF substituto tem {num_paginas_subst} paginas."
        )

    # Converter para indice zero-based
    idx_alvo = pagina_alvo - 1
    idx_subst = pagina_substituta - 1

    writer = PdfWriter()

    # Copiar todas as paginas do base para o writer,
    # substituindo apenas a pagina alvo
    for i in range(num_paginas_base):
        if i == idx_alvo:
            # Usar a pagina do PDF substituto
            pagina = subst_reader.pages[idx_subst]
        else:
            # Usar a pagina original
            pagina = base_reader.pages[i]

        writer.add_page(pagina)

    # Guardar no ficheiro de saida
    with open(ficheiro_saida, "wb") as f_out:
        writer.write(f_out)


if __name__ == "__main__":
    # Exemplo de uso:
    # - ficheiro_base.pdf: PDF original
    # - ficheiro_substituto.pdf: PDF que contem a pagina para substituir
    # - substitui a pagina 3 do PDF base pela pagina 1 do PDF substituto
    # - grava resultado em saida.pdf

    ficheiro_base = "Recibos_Vencimento_Novembro_2025.pdf"
    ficheiro_substituto = "JL.pdf"
    pagina_alvo = 5          # pagina do base a substituir (1-based)
    pagina_substituta = 1    # pagina do substituto a usar (1-based)
    ficheiro_saida = "Recibos_Vencimento_Novembro_2025_1.pdf"

    substituir_pagina(
        ficheiro_base,
        ficheiro_substituto,
        pagina_alvo,
        pagina_substituta,
        ficheiro_saida
    )

    print("PDF gerado com sucesso em", ficheiro_saida)
