from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

styles = getSampleStyleSheet()
style = styles['Normal']
bold_style = styles['Heading1']


customer_name_style = ParagraphStyle(
    'customer_name_style',
    margin=0,
    padding=0,
    textColor='#212B54',
    fontSize=14,
    fontName=bold_style.fontName
)

address_style = ParagraphStyle(
    'address_style',
    textColor='#212B54',
    fontSize=11,
)

kontoauszug_style = ParagraphStyle(
    'customer_name_style',
    margin=0,
    padding=0,
    textColor='#FF5761',
    fontSize=28,
    fontName=bold_style.fontName

)



account_heading_style = ParagraphStyle(
    'account_heading_style',
    textColor='#212B54',
    fontSize=11,
    fontName=bold_style.fontName
)
account_number_style = ParagraphStyle(
    'account_number_style',
    textColor='#212B54',
    fontName="NumericFont",
)
about_number_style = ParagraphStyle(
    'about_number_style',
    textColor='#212B54',
)
about_number_style_bold = ParagraphStyle(
    'about_number_style_bold',
    fontName=bold_style.fontName,
    textColor='#212B54',
)

invoice_detail_style = ParagraphStyle(
    'invoice_detail_style',
    textColor='#212B54',
    fontSize=11,
    alignment=2
)
invoice_detail_style_bold = ParagraphStyle(
    'invoice_detail_style_bold',
    textColor='#212B54',
    fontSize=11,
    fontName="EuclidSemiBold",
    alignment=2
)
