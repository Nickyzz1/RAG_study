from mineru.backend.pipeline.pipeline_analyze import load_images_from_pdf
from mineru.cli.common import do_parse, read_fn
from mineru.utils.enum_class import ImageType
from mineru.utils.config_reader import get_device 
from mineru.utils.model_utils import clean_memory, get_res_list_from_layout_res #trash
from mineru.backend.pipeline.pipeline_analyze import batch_image_analyze
from PIL import Image
import gc

pdf_bytes = read_fn("Data/PDF/pdflatex-image.pdf")
pdf_bytes_list = []
pdf_bytes_list.append(pdf_bytes)
# print(pdf_bytes)
print("Pegou os bytes")
# do_parse(
#     output_dir="C:/Users/SPI1CT/Documents/Estudo XPertify/RAG-Anything/repo/RAG_study",
#     pdf_file_names="y",
#     pdf_bytes_list=pdf_bytes_list,
#     p_lang_list=[''],
#     method='ocr',
#     backend='pipeline',
#     formula_enable=False,
#     table_enable=False,
#     server_url=None,
#     f_draw_layout_bbox=False,
#     f_draw_span_bbox=False,
#     f_dump_md=False,
#     f_dump_middle_json=False,
#     f_dump_model_output=False,
#     f_dump_orig_pdf=False,
#     f_dump_content_list=False
# )

all_pages_info = []
images_list, _ = load_images_from_pdf(pdf_bytes,image_type=ImageType.PIL)
print("Carregou as imagens")
_ocr_enable = False
for page_idx in range(len(images_list)):
    img_dict = images_list[page_idx]
    all_pages_info.append((
                    img_dict['img_pil'], _ocr_enable, ""
                ))
images_with_extra_info = [(info[0], info[1], info[2]) for info in all_pages_info]
batch_size = 384
batch_images = [
        images_with_extra_info[i:i + batch_size]
        for i in range(0, len(images_with_extra_info), batch_size)
    ]
results = []
for index, batch_image in enumerate(batch_images):
    batch_results = batch_image_analyze(batch_image, True, True)
    results.extend(batch_results)

print(results)
# image = imagelist[0]['img_pil']
# image.save('imagemteste.png')
# print(type(imagelist))
# clean_memory(get_device())
# # del imagelist
# # del pdf_bytes
# # del image
# # gc.collect() 