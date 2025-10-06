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



