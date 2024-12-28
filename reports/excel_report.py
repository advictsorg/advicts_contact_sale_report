from odoo import models


class ContactSaleXlsx(models.AbstractModel):
    _name = 'report.advicts_contact_sale_report.contact_sale_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        style = workbook.add_format({
            'bold': True,
            'bg_color': '#c9c5c5',
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'align': 'center'
        })
        style_data = workbook.add_format({
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'align': 'center',
        })
        style_data_row = workbook.add_format({
            'border': 1,  # 1 is for a thin border
            'valign': 'vcenter',
            'bg_color': '#EEEEEE',
            'align': 'center'
        })

        title = 'Contact Sales Report'

        report_name = title
        sheet = workbook.add_worksheet(report_name[:31])
        sheet.merge_range("A1:E1", title, style)
        sheet.write(0, 5, 'From', style)
        sheet.write(0, 6, data['start_date'], style)
        sheet.write(0, 7, 'To', style)
        sheet.write(0, 8, data['end_date'], style)
        sheet.write(0, 9, 'To', style)
        sheet.write(0, 10, data['partner_id'], style)

        sheet.write(2, 0, '#', style_data_row)
        sheet.write(2, 1, 'Number', style_data_row)
        sheet.write(2, 2, 'Order Date', style_data_row)
        sheet.write(2, 3, 'Contract Number', style_data_row)
        sheet.write(2, 4, 'Salesperson', style_data_row)
        sheet.write(2, 5, 'Company', style_data_row)
        sheet.write(2, 6, 'Total Before Discount', style_data_row)
        sheet.write(2, 7, 'Discount', style_data_row)
        sheet.write(2, 8, 'Total', style_data_row)
        sheet.write(2, 9, 'Invoice Status', style_data_row)
        sheet.write(2, 10, 'Tags', style_data_row)
        row = 3
        count = 0
        for line in data['data']:
            row += 1
            count += 1
            sheet.write(row, 0, count, style_data)
            sheet.write(row, 1, line['number'], style_data)
            sheet.write(row, 2, line['date'], style_data)
            sheet.write(row, 3, line['contract_number'], style_data)
            sheet.write(row, 4, line['salesperson'], style_data)
            sheet.write(row, 5, line['company'], style_data)
            sheet.write(row, 6, line['amount_undiscounted'], style_data)
            sheet.write(row, 7, line['amount_discount'], style_data)
            sheet.write(row, 8, line['amount_total'], style_data)
            sheet.write(row, 9, line['invoice_status'], style_data)
            tags = ', '.join(tag['name'] for tag in line['tags'])
            sheet.write(row, 10, tags, style_data)
