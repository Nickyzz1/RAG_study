from mineru.backend.pipeline.pipeline_analyze import load_images_from_pdf,doc_analyze as pipeline_doc_analyze
from mineru.cli.common import do_parse, read_fn
from mineru.utils.enum_class import ImageType
import copy
from mineru.data.data_reader_writer import FileBasedDataWriter
from mineru.utils.hash_utils import bytes_md5
from mineru.backend.pipeline.pipeline_magic_model import MagicModel
from mineru.utils.enum_class import ContentType
from mineru.utils.span_pre_proc import remove_outside_spans, remove_overlaps_low_confidence_spans, \
    remove_overlaps_min_spans
from mineru.utils.cut_image import cut_image_and_table
from mineru.utils.block_pre_proc import prepare_block_bboxes, process_groups
from mineru.utils.span_block_fix import fill_spans_in_blocks, fix_discarded_block, fix_block_spans
from PIL import Image
from tqdm import tqdm
from raganything.parser import MineruParser
import time

def socorro(model_list, images_list, pdf_doc, image_writer, lang=None, ocr_enable=False, formula_enabled=True):

    for page_index, page_model_info in tqdm(enumerate(model_list), total=len(model_list), desc="Processing pages"):
        # print("==================================Page index=============================================")
        # print(page_index)
        # print("==================================Page model info=============================================")
        # print(page_model_info)
        page = pdf_doc[page_index]
        # print("==================================Page=============================================")
        # print(page)
        image_dict = images_list[page_index]
        # print("==================================Image_dict=============================================")
        # print(image_dict)
        scale = image_dict["scale"]
        # print("==================================Scale=============================================")
        # print(scale)
        # print("Model_list:",model_list)
        page_pil_img = image_dict["img_pil"]
        # print("==================================page_pil_img=============================================")
        # print(page_pil_img)
        # page_img_md5 = str_md5(image_dict["img_base64"])
        page_img_md5 = bytes_md5(page_pil_img.tobytes())
        # print("==================================page_img_md5=============================================")
        # print(page_pil_img)
        page_w, page_h = map(int, page.get_size())
        magic_model = MagicModel(page_model_info, scale)
        # print("==================================magic_model=============================================")
        # print(magic_model)

        discarded_blocks = magic_model.get_discarded()
        text_blocks = magic_model.get_text_blocks()
        title_blocks = magic_model.get_title_blocks()
        inline_equations, interline_equations, interline_equation_blocks = magic_model.get_equations()

        img_groups = magic_model.get_imgs()
        # print("==================================img_groups=============================================")
        # print(img_groups)
        table_groups = magic_model.get_tables()
        # print("==================================table_groups=============================================")
        # print(table_groups)

        img_body_blocks, img_caption_blocks, img_footnote_blocks, maybe_text_image_blocks = process_groups(
            img_groups, 'image_body', 'image_caption_list', 'image_footnote_list'
        )

        table_body_blocks, table_caption_blocks, table_footnote_blocks, _ = process_groups(
            table_groups, 'table_body', 'table_caption_list', 'table_footnote_list'
        )

        spans = magic_model.get_all_spans()



        if len(maybe_text_image_blocks) > 0:
            for block in maybe_text_image_blocks:
                should_add_to_text_blocks = False

                img_body_blocks.append(block)


        """将所有区块的bbox整理到一起"""
        if formula_enabled:
            interline_equation_blocks = []

        if len(interline_equation_blocks) > 0:

            for block in interline_equation_blocks:
                spans.append({
                    "type": ContentType.INTERLINE_EQUATION,
                    'score': block['score'],
                    "bbox": block['bbox'],
                    "content": "",
                })

            all_bboxes, all_discarded_blocks, footnote_blocks = prepare_block_bboxes(
                img_body_blocks, img_caption_blocks, img_footnote_blocks,
                table_body_blocks, table_caption_blocks, table_footnote_blocks,
                discarded_blocks,
                text_blocks,
                title_blocks,
                interline_equation_blocks,
                page_w,
                page_h,
            )
        else:
            all_bboxes, all_discarded_blocks, footnote_blocks = prepare_block_bboxes(
                img_body_blocks, img_caption_blocks, img_footnote_blocks,
                table_body_blocks, table_caption_blocks, table_footnote_blocks,
                discarded_blocks,
                text_blocks,
                title_blocks,
                interline_equations,
                page_w,
                page_h,
            )

        """在删除重复span之前，应该通过image_body和table_body的block过滤一下image和table的span"""
        """顺便删除大水印并保留abandon的span"""
        spans = remove_outside_spans(spans, all_bboxes, all_discarded_blocks)

        """删除重叠spans中置信度较低的那些"""
        spans, dropped_spans_by_confidence = remove_overlaps_low_confidence_spans(spans)
        """删除重叠spans中较小的那些"""
        spans, dropped_spans_by_span_overlap = remove_overlaps_min_spans(spans)


        spans = remove_outside_spans(spans, all_bboxes, all_discarded_blocks)

        """删除重叠spans中置信度较低的那些"""
        spans, dropped_spans_by_confidence = remove_overlaps_low_confidence_spans(spans)
        """删除重叠spans中较小的那些"""
        spans, dropped_spans_by_span_overlap = remove_overlaps_min_spans(spans)

        discarded_block_with_spans, spans = fill_spans_in_blocks(
            all_discarded_blocks, spans, 0.4
        )
        fix_discarded_blocks = fix_discarded_block(discarded_block_with_spans)

        """对image/table/interline_equation截图"""
        for span in spans:
            print("SPAN TYPE:",span['type'])
            if span['type'] in [ContentType.IMAGE, ContentType.TABLE, ContentType.INTERLINE_EQUATION]:
                span = cut_image_and_table(
                    span, page_pil_img, page_img_md5, page_index, image_writer, scale=scale
                )


start_time = time.perf_counter()
path = "Data/PDF/3-page-images.pdf"
# MineruParser().parse_document(path)
pdf_bytes = read_fn(path)
pdf_bytes_list = []
pdf_bytes_list.append(pdf_bytes)
# print(pdf_bytes)
print("Pegou os bytes")
pdf_file_names = ['nome1']
infer_results, all_image_lists, all_pdf_docs, lang_list, ocr_enabled_list = (
        pipeline_doc_analyze(
            pdf_bytes_list, lang_list=['en'], parse_method='auto',
            formula_enable=True, table_enable=True
        )
    )
formula_enabled = True
print("=======================Infer_results============================")
print(infer_results)
print("=======================Enumerate(infer_results)============================")
print(enumerate(infer_results))
print("=======================all_image_lists============================")
print(all_image_lists)
print("========================IDX=========================")
for idx, model_list in enumerate(infer_results):
    print(idx)
    model_json = copy.deepcopy(model_list)
    pdf_file_name = pdf_file_names[idx]
    local_image_dir = "./diretorioFim"
    image_writer = FileBasedDataWriter(local_image_dir)
    images_list = all_image_lists[idx]
    pdf_doc = all_pdf_docs[idx]
    _lang = lang_list[idx]
    _ocr_enable = ocr_enabled_list[idx]

    socorro(model_list=model_list,images_list=images_list,pdf_doc=pdf_doc,image_writer=image_writer,lang=_lang,
            ocr_enable=False,formula_enabled=True)
end_time = time.perf_counter()
print(end_time - start_time)

    