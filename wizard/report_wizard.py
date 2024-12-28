from odoo import models, fields, _, api
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError


class ReportWizard(models.TransientModel):
    _name = "contact.sale.report"
    _description = "Contact Sales Report"

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', required=True, default=lambda self: date.today())
    partner_id = fields.Many2one('res.partner', string='Contact', required=True, )
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        if self.start_date > self.end_date:
            raise ValidationError(_('Start Date must be before End Date'))

    def _get_report_data(self):
        if self.start_date:
            sales = self.env['sale.order'].search(
                [('date_order', '>=', self.start_date),
                 ('date_order', '<=', self.end_date),
                 ('state', 'in', ['draft','sent','sale','done']),
                 ('partner_id', '=', self.partner_id.id),
                 ('company_id', '=', self.company_id.id),
                 ])
        else:
            sales = self.env['sale.order'].search(
                [('date_order', '<=', self.end_date),
                 ('state', 'in', ['sale','done']),
                 ('partner_id', '=', self.partner_id.id),
                 ('company_id', '=', self.company_id.id),
                 ])
        contact_data = []
        for sale in sales:
            tags = []
            for tag in sale.tag_ids:
                tags.append(
                    {
                        'name': tag.name,
                        'color': tag.color,
                    }
                )
            contact_data.append(
                {
                    'number': sale.name,
                    'date': sale.date_order,
                    'customer': sale.partner_id.name,
                    'salesperson': sale.user_id.name,
                    'company': sale.company_id.name,
                    'tags': tags,
                    'invoice_status': sale.invoice_status,
                    'amount_undiscounted': sale.amount_undiscounted,
                    'amount_discount': sale.amount_discount,
                    'amount_total': sale.amount_total,
                    'contract_number': sale.contract_number,

                })
        print(contact_data)

        report_data = {
            'partner_id': self.partner_id.name,
            'data': contact_data,
            'start_date': self.start_date if self.start_date else '',
            'end_date': self.end_date,
        }
        return report_data

    def action_print_pdf_report(self):
        report_data = self._get_report_data()
        return self.env.ref('advicts_contact_sale_report.contact_sale_report_action').report_action(self,
                                                                                                    data=report_data)

    def action_print_xlsx_report(self):
        report_data = self._get_report_data()
        return self.env.ref('advicts_contact_sale_report.contact_sale_report_action_xlsx').report_action(self,
                                                                                                         data=report_data)
