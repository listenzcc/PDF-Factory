"""
File: pdf.py
Author: Chuncheng Zhang
Date: 2025-06-16
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    PDF generator.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2025-06-16 ------------------------
# Requirements and constants
import contextlib

from io import BytesIO
from html import escape
from typing import Union
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4

from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.platypus import PageBreak, FrameBreak, NextPageTemplate
from reportlab.platypus import Table, Paragraph, Spacer, Image
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

from .svg import SVGCache
from .font import register_chinese_font
from .log import logger

# %%
svg_cache = SVGCache()


class MySVG:
    firstPageFrame = 'pdfFactory.svg.frame.path'
    waterPrint = 'pdfFactory.svg.logoWaterPrint.path'


def _prepare_svg():
    key = MySVG.firstPageFrame
    svg_cache.checkout(key)
    svg_cache.resize_drawing_by_height(key, 4)
    logger.info(f'Using svg: {key}')

    key = MySVG.waterPrint
    svg_cache.checkout(key)
    svg_cache.resize_drawing_by_height(key, 4)
    logger.info(f'Using svg: {key}')

    return


_prepare_svg()

# %% ---- 2025-06-16 ------------------------
# Function and class


def setup_styles(font_name):
    """设置样式表"""
    styles = getSampleStyleSheet()

    # 添加自定义样式
    custom_styles = {
        'cTitle': {
            'parent': styles['Heading1'],
            'fontSize': 24,
            'leading': 28,
            'alignment': TA_CENTER,
            'spaceAfter': 20,
            'textColor': colors.darkblue,
        },
        'cSubTitle': {
            'parent': styles['Heading2'],
            'fontSize': 14,
            'leading': 18,
            'alignment': TA_CENTER,
            'spaceAfter': 15,
            'textColor': colors.darkblue,
        },
        'cBodyText': {
            'parent': styles['BodyText'],
            'fontSize': 12,
            'leading': 15,
            'alignment': TA_LEFT,
            'spaceAfter': 10,
        },
        'cCenteredText': {
            'parent': styles['Normal'],
            'fontSize': 12,
            'leading': 15,
            'alignment': TA_CENTER,
            'spaceAfter': 10,
        },
        'cImageCaption': {
            'parent': styles['Italic'],
            'fontSize': 10,
            'leading': 12,
            'alignment': TA_CENTER,
            'spaceBefore': 5,
            'spaceAfter': 15,
        },
        'cStopper': {
            'parent': styles['Normal'],
            'fontSize': 14,
            'leading': 10,
            'alignment': TA_CENTER,
            'spaceBefore': 10,
            'textColor': colors.darkred,
        }
    }

    for style_name, style_params in custom_styles.items():
        if style_name in styles:
            logger.warning(
                f'Define {style_name}, but the sample style already has it, so I am ignoring it.')
        else:
            styles.add(ParagraphStyle(name=style_name, **style_params))
            logger.debug(f'Using style: {style_name} = {style_params}')

    # 修改现有样式使用中文字体
    for style_name in styles.byName:
        styles[style_name].fontName = font_name
        logger.debug(f'Update styles[{style_name}].fontName = {font_name}')

    return styles


class PDFBasic:
    page_size = A4
    font_name = register_chinese_font()
    styles = setup_styles(font_name)

    doc: BaseDocTemplate
    buff: BytesIO
    elements: list
    date: str


class PDFRender(PDFBasic):
    def __init__(self):
        self.mk_doc()

    def mk_doc(self):
        buff = BytesIO()
        doc = BaseDocTemplate(
            buff,
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        first_page_frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            id='firstPageFrame',
        )

        normal_page_frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            id='normalPageFrame',
            showBoundary=True
        )

        two_columns_page_left_frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width/2,
            doc.height,
            id='twoColumnsPageLeftFrame',
            showBoundary=True
        )

        two_columns_page_right_frame = Frame(
            doc.leftMargin+doc.width/2,
            doc.bottomMargin,
            doc.width/2,
            doc.height,
            id='twoColumnsPageRightFrame',
            showBoundary=True
        )

        doc.addPageTemplates([
            PageTemplate(
                id='FirstPage',
                frames=[first_page_frame],
                onPage=self._render_first_page,
            ),
            PageTemplate(
                id='TwoColumnsPage',
                frames=[two_columns_page_left_frame,
                        two_columns_page_right_frame],
                onPage=self._render_normal_page,
            ),
            PageTemplate(
                id='NormalPage',
                frames=[normal_page_frame],
                onPage=self._render_normal_page)
        ])

        self.doc = doc
        self.buff = buff

        return self.doc

    def _render_first_page(self, canvas: canvas.Canvas, doc: BaseDocTemplate):
        W, H = self.page_size
        w = W-doc.leftMargin-doc.rightMargin
        h = H - doc.bottomMargin - doc.topMargin
        color = colors.darkblue

        header_text = 'Left'
        header_text_r = 'Right'

        # Draw the header
        with self._safeCanvas(canvas):
            canvas.setFillColor(color)
            canvas.setStrokeColor(color)
            canvas.setFont(self.font_name, 8)
            canvas.translate(doc.leftMargin, H-doc.topMargin+0.5*inch)

            dy = 0.05*inch

            canvas.drawString(0, dy, header_text)
            canvas.drawRightString(w, dy, header_text_r)
            canvas.line(0, 0, w, 0)

        # Draw footer
        with self._safeCanvas(canvas):
            canvas.setFillColor(color)
            canvas.setStrokeColor(color)
            canvas.setFont(self.font_name, 12)
            canvas.translate(doc.leftMargin, doc.bottomMargin-0.5*inch)

            offset_y = 1.6*inch
            dy = -0.25*inch

            canvas.line(0, offset_y, w*0.3, offset_y)
            canvas.drawString(0, offset_y+2*dy,
                              'CopyRight:\tBelongs to no-one')
            canvas.drawString(0, offset_y+3*dy,
                              'Author:\tListenzcc')
            canvas.drawString(0, offset_y+4*dy,
                              'Address:\tSome building, some road')
            canvas.drawString(0, offset_y+5*dy,
                              'Location:\tSome city, some state')

        # Draw the Logo svg
        with self._safeCanvas(canvas):
            canvas.translate(doc.leftMargin, doc.bottomMargin)

            drawing = svg_cache.checkout(MySVG.firstPageFrame)

            x1, y1, x2, y2 = drawing.getBounds()
            renderPDF.draw(
                drawing, canvas,
                w*0.5 - (x2+x1)*0.5,
                h*0.5,
            )

            canvas.setFillColor(color)
            canvas.setStrokeColor(color)
            canvas.setFont(self.font_name, 36)
            canvas.drawCentredString(
                w*0.5, h*0.5+(y1+y2)*0.5-0.12*inch, 'Auto Generated PDF')
            canvas.setFont(self.font_name, 24)
            canvas.drawCentredString(w*0.5, h*0.5, 'Example Page')

        return

    def _render_normal_page(self, canvas: canvas.Canvas, doc: BaseDocTemplate):
        """Customizes the first page (adds footer at the bottom)."""
        W, H = self.page_size
        w = W - doc.leftMargin - doc.rightMargin
        h = H - doc.bottomMargin - doc.topMargin
        color = 'gray'

        # Header texts
        header_text = 'Left prompt'
        header_text_r = self.date

        # Page number
        current_page = doc.page
        page_number = f"第 {current_page} 页"

        drawing = svg_cache.checkout(MySVG.waterPrint)

        # Draw header
        with self._safeCanvas(canvas):
            canvas.setFillColor(color)
            canvas.setStrokeColor(color)
            canvas.setFont(self.font_name, 8)
            canvas.translate(doc.leftMargin, H-doc.topMargin+0.5*inch)

            dy = 0.05*inch

            canvas.drawString(0, dy, header_text)
            canvas.drawRightString(w, dy, header_text_r)
            canvas.line(0, 0, w, 0)

        # Draw footer
        with self._safeCanvas(canvas):
            canvas.setFillColor(color)
            canvas.setStrokeColor(color)
            canvas.setFont(self.font_name, 8)
            canvas.translate(doc.leftMargin, doc.bottomMargin-0.5*inch)

            dy = -0.15*inch

            canvas.drawCentredString(w / 2.0, dy, page_number)
            canvas.line(0, 0, w, 0)

        # Draw water print
        with self._safeCanvas(canvas):
            canvas.translate(doc.leftMargin, doc.bottomMargin)
            canvas.translate(w*0.5, h*0.5)
            canvas.rotate(20)
            x1, y1, x2, y2 = drawing.getBounds()
            renderPDF.draw(
                drawing, canvas,
                -(x1+x2)*0.5,
                -(y1+y2)*0.5,
            )
        return

    @contextlib.contextmanager
    def _safeCanvas(self, canvas: canvas.Canvas):
        canvas.saveState()
        try:
            yield canvas
        finally:
            canvas.restoreState()


class PDFUtil(PDFRender):
    def __init__(self):
        super().__init__()
        self.elements = []

    def build(self):
        self.date = datetime.now().isoformat()
        n = len(self.elements)
        # It will empty the self.elements
        self.doc.build(self.elements)
        logger.debug(f'Built doc with {n} elements')
        return self.buff

    def save(self, path: Union[Path, str]):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(self.buff.getvalue())
        logger.info(f'Wrote file: {path}')
        return path


class PDFGenerator(PDFUtil):
    def __init__(self):
        super().__init__()

    def insert_image_with_caption(self, path_or_bytes, caption: str = 'N.A.', width: float = 6):
        """
        This function inserts an image into the doc.

        :param image_path_or_bytes:
            The path to the image you want to insert.
            Or the bytes can be converted to Image
        """
        img = Image(path_or_bytes)
        img.drawWidth = width * inch
        img.drawHeight = img.drawWidth / img.imageWidth * img.imageHeight
        self.elements.append(img)
        self.elements.append(Paragraph(caption, self.styles['ImageCaption']))
        # 添加一些间距
        self.elements.append(Spacer(1, 0.3*inch))
        logger.debug(f'Insert img(caption): {img}({caption})')
        return

    def insert_paragraph(self, text: str, style='cBodyText'):
        """添加段落"""
        # Report Lab can't handle hebrew (unicode) <https://stackoverflow.com/questions/10958904/report-lab-cant-handle-hebrew-unicode>
        # Python Reportlab - Unable to print special characters <https://stackoverflow.com/questions/19712130/python-reportlab-unable-to-print-special-characters>
        # AttributeError: module 'cgi' has no attribute 'escape' <https://github.com/ablab/quast/issues/157>
        text = escape(text)

        try:
            self.elements.append(Paragraph(text, self.styles[style]))
        except KeyError:
            self.elements.append(Paragraph(text, self.styles['BodyText']))
            logger.warning(
                f'The {style} is not available, using BodyText instead.')
        self.elements.append(Spacer(1, 0.2*inch))
        logger.debug(f'Insert paragraph: {text[:20]}...')
        return

    def insert_table(self, *lines):
        """
        It inserts a table into the database.
        """
        col_width = 120
        style = [
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),  # 字体
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # 第一行的字体大小
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # 第二行到最后一行的字体大小
            ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),  # 设置第一行背景颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 第一行水平居中
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # 第二行到最后一行左右左对齐
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有表格上下居中对齐
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为grey色，线宽为0.5
        ]
        table = Table(lines, colWidths=col_width, style=style)
        self.elements.append(table)
        logger.debug(f'Insert table, {table}')
        return

    def insert_page_break(self):
        self.elements.append(PageBreak())
        logger.debug('Insert pageBreak')
        return

    def insert_frame_break(self):
        self.elements.append(FrameBreak())
        logger.debug('Insert pageBreak')
        return

    def switch_page_template(self, name: str):
        '''
        Insert NextPageTemplate(name) into the doc.
        It also automatically inserts the page break to make sure it works.
        '''
        self.elements.append(NextPageTemplate(name))
        logger.debug(f'Switch page template to {name}')
        self.insert_page_break()
        return

# %% ---- 2025-06-16 ------------------------
# Play ground

# %% ---- 2025-06-16 ------------------------
# Pending


# %% ---- 2025-06-16 ------------------------
# Pending
