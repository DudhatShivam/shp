# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    new_fiscal_position_id = fields.Many2one('account.fiscal.position', string='Temporary fiscal position')

    @api.onchange('partner_id', 'company_id', 'date_order')
    def onchange_partner_id(self):
        result = super(PurchaseOrder, self).onchange_partner_id()
        self.new_fiscal_position_id = False
        if self.partner_id and self.partner_id.new_property_account_position_id:
            date_ref = self.date_order.date()
            from_date = self.company_id.fiscal_position_date_start
            to_date = self.company_id.fiscal_position_date_stop
            #check date limit
            if (from_date and to_date and from_date <= date_ref and to_date >= date_ref) or (not from_date and to_date and to_date >= date_ref) or (from_date and not to_date and from_date <= date_ref) or (not from_date and not to_date):
                self.new_fiscal_position_id = self.partner_id.new_property_account_position_id.id
            else:
                self.new_fiscal_position_id = False
        return result

    @api.model
    def apply_fiscal_position(self):
        fiscal_pool = self.env['account.fiscal.position']
        context = dict(self._context)
        for record in self.search([('id', 'in', context.get('active_ids'))]):
            if record.state != 'draft':
                raise ValidationError(_('You can only apply temporary fiscal position on draft records.'))
            if record.partner_id.new_property_account_position_id:
                record.new_fiscal_position_id = record.partner_id.new_property_account_position_id.id
                for line in record.order_line:
                    taxes = line.taxes_id
                    line.taxes_id = record.partner_id.new_property_account_position_id.map_tax(taxes, line.product_id, line.order_id.partner_id) if record.partner_id.new_property_account_position_id else taxes
        return True

    @api.model
    def apply_old_tax(self):
        fiscal_pool = self.env['account.fiscal.position']
        context = dict(self._context)
        for record in self.search([('id', 'in', context.get('active_ids'))]):
            if record.state != 'draft':
                raise ValidationError(_('You can only apply old tax on draft records.'))
            new_fiscal_position = record.new_fiscal_position_id
            if new_fiscal_position:
                for line in record.order_line:
                    taxes = []
                    for tax in line.taxes_id:
                        taxes.append(tax.id)
                        for fo_tax in new_fiscal_position.tax_ids:
                            if fo_tax.tax_dest_id and tax.id == fo_tax.tax_dest_id.id:
                                if tax.id in taxes:
                                    taxes.remove(tax.id)
                                taxes.append(fo_tax.tax_src_id.id)    
                    line.taxes_id = [(6, 0, list(set(taxes)))]
            record.new_fiscal_position_id = False
        return True

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _compute_tax_id(self):
        for line in self:
            fpos = line.order_id.new_fiscal_position_id or line.order_id.fiscal_position_id or line.order_id.partner_id.with_context(force_company=line.company_id.id).property_account_position_id
            # If company_id is set, always filter taxes by the company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: not line.company_id or r.company_id == line.company_id)
            line.taxes_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_id) if fpos else taxes
