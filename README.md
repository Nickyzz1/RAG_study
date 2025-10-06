# RAG_study
Repo pra podermos estudar um pouco sobre a lib RAG

## Bibliotecas Utilizadas

1. LightRAG (https://github.com/HKUDS/LightRAG)
2. MinerU (https://github.com/opendatalab/MinerU)
   1. Transforma dados de PDF em formato legível para máquina

## Conteúdos Suportados

- PDFs - Artigos de pesquisa, relatórios, apresentações
- Documentos Office - DOC, DOCX, PPT, PPTX, XLS, XLSX
- Imagens - JPG, PNG, BMP, TIFF, GIF, WebP
- Arquivos de texto - TXT, MD

## Formato da content_list

A content_list deve seguir o formato padrão, com cada item sendo um dicionário contendo:

- Text content: {"type": "text", "text": "content text", "page_idx": 0}
- Image content: {"type": "image", "img_path": "/absolute/path/to/image.jpg", "image_caption": ["caption"], "image_footnote": ["note"], "page_idx": 1}
- Table content: {"type": "table", "table_body": "markdown table", "table_caption": ["caption"], "table_footnote": ["note"], "page_idx": 2}
- Equation content: {"type": "equation", "latex": "LaTeX formula", "text": "description", "page_idx": 3}
- Generic content: {"type": "custom_type", "content": "any content", "page_idx": 4}

Usa VLM (Vision-Language Model) para relacionar imagens e texto. O objetivo é entender o contexto da imagem e do texto para melhores insights
Modulo de configuração de contexto. usa LLM, modelo de linguagem de grande porte que entender e gera texto para reconhecer o contexto da imagem e do texto e possuem  um modelo de configuração de váriaveis RAGAnythingConfig (possível configurar se ele está lendo a página inteira ou chunks (quebrando a página em contextos) )
Ex de rag-config:
Observações:
- Para melhor compreensão do contexto o modelo pega uma página ou chunk antes e uma(um) depois para entender melhor
- "Mineru" é uma ferramenta de código aberto para converter PDFs em formatos legíveis por máquina, como Markdown e JSON

# Context Extraction Configuration
 ```bash
   context_window: int = 1                       # Context window size (pages/chunks)
   context_mode: str = "page"                 # Context mode ("page" or "chunk")
   max_context_tokens: int = 2000             # Maximum context tokens
   include_headers: bool = True               # Include document headers
   include_captions: bool = True              # Include image/table captions
   context_filter_content_types: List[str] = ["text"]  # Content types to include
   content_format: str = "minerU"             # Default content format for context extraction
   ```
# Context extraction settings
      ```bash
      CONTEXT_WINDOW=2                 # janela de contexto, pega uma página/chunk antes e um depois
      CONTEXT_MODE=page                # dividindo em paginas, não chunks
      MAX_CONTEXT_TOKENS=3000          # o máximo de partições/chunks que um pag pode ter
      INCLUDE_HEADERS=true
      INCLUDE_CAPTIONS=true
      CONTEXT_FILTER_CONTENT_TYPES=text,image   # inclui análise de textos/imagens para definir o contexto
      CONTENT_FORMAT=minerU            # formato padrão do conteudo extraido

      ```

- possui uma pasta com exemplos de códigos

# Diferentes tipos de conteúdo exigem dependências opcionais específicas:
- Documentos do Office (.doc, .docx, .ppt, .pptx, .xls, .xlsx): Instalar o LibreOffice
- Formatos de imagem estendidos (.bmp, .tiff, .gif, .webp): Instalar compip install raganything[image]
- Arquivos de texto (.txt, .md): Instalar compip install raganything[text]
- 📋 Instalação rápida : use pip install raganything[all]para habilitar o suporte a todos os formatos (somente dependências do - Python - o LibreOffice ainda precisa de instalação separada)

# Formatos de documentos
- PDFs - Artigos de pesquisa, relatórios, apresentações
- Documentos do Office - DOC, DOCX, PPT, PPTX, XLS, XLSX
- Imagens - JPG, PNG, BMP, TIFF, GIF, WebP
- Arquivos de texto - TXT, MD

# Mineru:
- Reconhece e converte automaticamente fórmulas no documento para o formato LaTeX.
- Reconhece e converte automaticamente tabelas no documento para o formato HTML.
- Detecta automaticamente PDFs digitalizados e PDFs ilegíveis e ativa a funcionalidade OCR.
- O OCR suporta detecção e reconhecimento de 84 idiomas.
- Suporta vários formatos de saída, como Markdown multimodal e NLP, JSON classificado por ordem de leitura e formatos intermediários avançados.



