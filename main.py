from reportlab.lib import colors
import math
from enum import Enum
# from reportlab.lib.pagesizes import letter as
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import csv
from io import BytesIO
import pandas as pd
from document_end import document_end_text
from top_area_style import (
    customer_name_style,
    address_style,
    kontoauszug_style,
    account_heading_style,
    about_number_style,
    about_number_style_bold,
    invoice_detail_style,
    invoice_detail_style_bold,
    account_number_style
)

PdfPagesize = (8.5*72, 11.7*72)


mm = 0.75
number_font_path = "./fonts/Numeric.ttf"
pdfmetrics.registerFont(TTFont("NumericFont", number_font_path))
textgrey_font_path = "./fonts/TeXGyreHeros.ttf"
pdfmetrics.registerFont(TTFont("TeXGyreHeros", textgrey_font_path))

educlid_regular = "./fonts/Euclid/Regular.ttf"
pdfmetrics.registerFont(TTFont("Euclid", educlid_regular))

educlid_medium = "./fonts/Euclid/Medium.ttf"
pdfmetrics.registerFont(TTFont("EuclidMedium", educlid_medium))

educlid_semibold = "./fonts/Euclid/SemiBold.ttf"
pdfmetrics.registerFont(TTFont("EuclidSemiBold", educlid_semibold))

educlid_bold = "./fonts/Euclid/Bold.ttf"
pdfmetrics.registerFont(TTFont("EuclidBold", educlid_bold))

class TableColumns(Enum):
    date = "Vervollständigt"
    account = "Beschreibung"
    amount = "Einnahmen / Ausgaben"

def parse_csv(data_csv):
    input_df = pd.read_csv(data_csv)
    input_dict = input_df.to_dict(orient='records')

    all_data = []

    for record in input_dict:
        date = record[TableColumns.date.value]

        if str(date) == 'nan':
            all_data[-1][TableColumns.account.value].append(record[TableColumns.account.value])
            continue

        all_data.append({
            TableColumns.date.value: date,
            TableColumns.account.value: [record[TableColumns.account.value]],
            TableColumns.amount.value: record[TableColumns.amount.value],
        })
    return all_data


def generate_pdf(
    data,
    customer_name,
    customer_address,
    customer_account_name,
    customer_account_iban,
    customer_account_bic,
    issue_date,
    from_date,
    to_date,
    account_opening_balance,
    account_closing_balance,
    ):
    pdf_buffer = BytesIO()

    # Create the PDF document
    doc = SimpleDocTemplate(pdf_buffer, pagesize=PdfPagesize, leftMargin=10, rightMargin=10, topMargin=40, bottomMargin=80*mm)

    # Set up styles for the PDF document
    styles = getSampleStyleSheet()
    style = styles['Normal']
    bold_style = styles['Heading1']

    # Create story to hold content
    story = []






    customer_name_paragraph = Paragraph(f"{customer_name}<br /><br />", customer_name_style)
    address_paragraph = Paragraph(f"{customer_address}", address_style)
    kontoauszug_paragraph = Paragraph("KONTOAUSZUG", kontoauszug_style)


    info_table_data = [
        [customer_name_paragraph, kontoauszug_paragraph],
        [address_paragraph,]
    ]

    info_table_style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (1, 0), bold_style.fontName),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
        ('TOPPADDING', (0, 0), (1, 0), 6),
        ('LEFTPADDING', (0, 0), (1, 0), 5),
        ('RIGHTPADDING', (0, 0), (1, 0), 5),
        ('TEXTCOLOR', (0, 0), (1, 0), '#222B55'),
    ])
    info_table_col_widths = [325, 230]
    # info_table_col_widths = [350, 232]
    info_table = Table(info_table_data, colWidths=info_table_col_widths)
    info_table.setStyle(info_table_style)

    story.append(info_table)










    customer_account_name_paragraph = Paragraph(f"{customer_account_name}", account_heading_style)
    iban_paragraph = Paragraph(f"IBAN: {customer_account_iban}", account_number_style)
    bin_paragraph = Paragraph(f"BIC: {customer_account_bic}", account_number_style)

    account_info_table_data_left = [
        [customer_account_name_paragraph],
        [iban_paragraph,],
        [bin_paragraph,]
    ]


    account_info_table_data_right = [
        [
            Paragraph("", ParagraphStyle('unknown', fontSize=1,))
        ],
        [
            Paragraph("Ausstellungsdatum:", invoice_detail_style),
            Paragraph(f"{issue_date}", invoice_detail_style),
        ],
        [
            Paragraph("Von:", invoice_detail_style),
            Paragraph(f"{from_date}", invoice_detail_style),
        ],
        [
            Paragraph("Bis:", invoice_detail_style),
            Paragraph(f"{to_date}", invoice_detail_style),
        ],
        [
            Paragraph("Eröffnungssaldo:", invoice_detail_style),
            Paragraph(f"{account_opening_balance} €", invoice_detail_style_bold),
        ],
        [
            Paragraph("Abschlusssaldo:", invoice_detail_style),
            Paragraph(f"{account_closing_balance} €", invoice_detail_style_bold),
        ]
    ]


    left_table = Table(account_info_table_data_left)
    right_table = Table(account_info_table_data_right)
    right_table.setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (1, 1), (1, -1), 5),
        ('RIGHTPADDING', (1, 1), (1, -1), 5),
        ('VALIGN', (0, 0), (0, -1), 'TOP'),
        ]
    ))

    account_info_table_data = [
        [
            left_table,
            right_table,
        ]
    ]

    account_info_table_style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (1, 0), bold_style.fontName),
        ('VALIGN', (0, 0), (1, 0), 'TOP'),
        ('TOPPADDING', (0, 0), (1, 0), 38),
        ('BOTTOMPADDING', (0, 0), (1, 0), 0),
        ('TEXTCOLOR', (0, 0), (1, 0), '#222B55'),
    ])


    account_info_table_col_widths = [375, 190]
    account_info_table = Table(account_info_table_data, colWidths=account_info_table_col_widths)
    account_info_table.setStyle(account_info_table_style)

    story.append(account_info_table)



    document_top = Paragraph("", style)
    story.append(document_top)










    # Add a table to the PDF
    table_data = [['Vervollständigt', 'Beschreibung', 'Einnahmen / Ausgaben']]
    account_descriptive_table_para_style = ParagraphStyle(
        'account_descriptive_table_para_style',
        textColor='#212B54',
        spaceAfter=3,
    )
    account_descriptive_table_para_style_bold = ParagraphStyle(
        'account_descriptive_table_para_style_bold',
        fontName=bold_style.fontName,
        textColor='#212B54',
        spaceAfter=3,
    )

    for entry in data:
        account_descriptive_table_data = [[]]
        account_descriptive_values = list(entry[TableColumns.account.value])
        for index, account_description in enumerate(account_descriptive_values):
            if index == 0:
                account_descriptive_table_data[0].append(
                    Paragraph(f"{account_description}", account_descriptive_table_para_style_bold)
                )
            else:
                account_descriptive_table_data[0].append(
                    Paragraph(f"{account_description}", account_descriptive_table_para_style,)
                )

        table_data.append([entry[TableColumns.date.value], account_descriptive_table_data, entry[TableColumns.amount.value]])


    # Create the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#EBECF0'),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1, 1)),
        ('FONTNAME', (0, 0), (-1, 0), bold_style.fontName),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, 0), 12),
        ('RIGHTPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (2, 0), (2, -1), "EuclidMedium"),  # Apply bold font to the "Amount" column
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 1), (-1, -1), 10), # Cells
        ('TOPPADDING', (0, 0), (-1, 0), 8), # Column
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8), # Column
        ('LEFTPADDING', (0, 1), (-1, -1), 15),
        ('RIGHTPADDING', (0, 1), (-1, -1), 15),
        ('TEXTCOLOR', (0, 0), (-1, -1), '#222B55'),
    ])

    for i in range(1, len(table_data)):
        table_style.add('LINEBELOW', (0, i), (-1, i), 1, '#EBECF0')

    col_widths = [125, 320, 125]
    table = Table(table_data, repeatRows=1, colWidths=col_widths)
    table.setStyle(table_style)

    # Add the table to the story
    story.append(table)


    # add_document_end_text
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.textColor = colors.HexColor("#7A8199")  # RGB values as hexadecimal
    style.fontSize = 9  # Set font size
    style.spaceBefore = 38  # Padding top (40px)
    style.spaceAfter = 30  # Padding bottom (30px)
    style.leftIndent = 15  # Padding left (15px)
    style.rightIndent = 15  # Padding right (15px)

    german_paragraphs = Paragraph(document_end_text, style)
    story.append(german_paragraphs)


    def add_footer(canvas, doc):
        canvas.saveState()

        # Get the dimensions of the letter-size page
        page_width, page_height = PdfPagesize

        # Logo in the center
        logo_path = "footer-image-3.png"
        # logo_width, logo_height = 129*mm, 31*mm
        logo_width, logo_height = 129*mm, 28*mm

        # Calculate the coordinates to center the image
        x_centered = (page_width - logo_width) / 2
        y_centered = 40  # You may need to adjust this value based on your requirements

        canvas.drawInlineImage(logo_path, x_centered + 9, y_centered, width=logo_width, height=logo_height)

        # Page number on the right side in a smaller font
        canvas.setFont("Helvetica", 8)
        page_num = canvas.getPageNumber()
        text = f"{page_num}"
        canvas.setFillColorRGB(0.686, 0.702, 0.753)

        # Adjust the x-coordinate to place the page number closer to the right edge
        x_page_num = page_width - 20
        canvas.drawRightString(x_page_num, 15, text)






        line1 = "Mit Finom.co erstellt"
        line2 = "Empowered by Solaris"

        # Draw the first line
        canvas.setFont("Helvetica", 9)
        canvas.setFillColorRGB(0.686, 0.702, 0.753)
        y_centered = 26  # You may need to adjust this value based on your requirements
        canvas.drawRightString(x_centered + logo_width - 2, y_centered, line1)

        # Draw the second line
        canvas.drawRightString(x_centered + logo_width + 2, y_centered - 10, line2)

        # Page number on the right side in a smaller font
        canvas.setFont("Helvetica", 9)
        page_num = canvas.getPageNumber()
        text = f"{page_num}"
        canvas.setFillColorRGB(0.686, 0.702, 0.753)

        # Adjust the x-coordinate to place the page number closer to the right edge
        x_page_num = page_width - 20
        canvas.drawRightString(x_page_num, 15, text)

        canvas.restoreState()

    # doc.build(story)
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    # Move the buffer's cursor to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer





def generate_invoice(
        csv_path,
        customer_name,
        customer_address,
        customer_account_name,
        customer_account_iban,
        customer_account_bic,
        issue_date,
        from_date,
        to_date,
        account_opening_balance,
        account_closing_balance,
    ):

    # Parse the CSV data
    data = parse_csv(csv_path)

    # Generate PDF and get the buffer
    pdf_buffer = generate_pdf(
        data,
        customer_name,
        customer_address,
        customer_account_name,
        customer_account_iban,
        customer_account_bic,
        issue_date,
        from_date,
        to_date,
        account_opening_balance,
        account_closing_balance,
    )

    # Save the PDF to a file (optional)
    with open("output.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_buffer.read())

generate_invoice(
    csv_path="your_data.csv",
    customer_name="Iris Tessel",
    customer_address="Brahmsstraße, 5, 73072, Donzdorf, Germany",
    customer_account_name="Main",
    customer_account_iban="DE04 1101 0101 5574 5917 79",
    customer_account_bic="SOBKDEB2XXX",
    issue_date="24.11.2023",
    from_date="01.11.2023",
    to_date="24.11.2023",
    account_opening_balance="0,00",
    account_closing_balance="2.448,71",
)
