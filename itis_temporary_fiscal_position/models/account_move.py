# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    new_fiscal_position_id = fields.Many2one('account.fiscal.position', string='Temporary fiscal position', readonly=True, states={'draft': [('readonly', False)]})

    @api.onchange('partner_id', 'company_id', 'date_invoice')
    def _onchange_partner_id(self):
        result = super(AccountMove, self)._onchange_partner_id()
        self.new_fiscal_position_id = False
        if self.partner_id and self.partner_id.new_property_account_position_id:
            date_ref = self.invoice_date or datetime.now().date()
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
                for line in record.invoice_line_ids:
                    #Apply temporary tax
                    taxes = line.tax_ids
                    line.tax_ids = record.partner_id.new_property_account_position_id.map_tax(taxes, line.product_id, line.move_id.partner_id) if record.partner_id.new_property_account_position_id else taxes
                    #Apply temporary account
                    if record.new_fiscal_position_id:
                        account_id = record.new_fiscal_position_id.map_account(account=line.account_id)
                        if account_id:
                            line.account_id = account_id.id
            record.with_context(skip_check_balanced=True)._recompute_dynamic_lines(recompute_all_taxes=True)
        return True

    def _check_balanced(self):
        if self.env.context.get('skip_check_balanced'):
            return True
        else:
            return super(AccountMove, self)._check_balanced()

    def apply_old_tax(self):
        fiscal_pool = self.env['account.fiscal.position']
        context = dict(self._context)
        for record in self.search([('id', 'in', context.get('active_ids'))]):
            if record.state != 'draft':
                raise ValidationError(_('You can only apply old tax on draft records.'))
            new_fiscal_position = record.new_fiscal_position_id
            if new_fiscal_position:
                for line in record.invoice_line_ids:
                    taxes = []
                    for tax in line.tax_ids:
                        taxes.append(tax.id)
                        for fo_tax in new_fiscal_position.tax_ids:
                            if fo_tax.tax_dest_id and tax.id == fo_tax.tax_dest_id.id:
                                if tax.id in taxes:
                                    taxes.remove(tax.id)
                                taxes.append(fo_tax.tax_src_id.id)    
                    line.tax_ids = [(6, 0, list(set(taxes)))]
                    account_id = line.account_id.id
                    for fo_account in new_fiscal_position.account_ids:
                        if line.account_id.id == fo_account.account_dest_id.id:
                            account_id = fo_account.account_src_id.id
                    line.account_id = account_id
            record.new_fiscal_position_id = False
            record.with_context(skip_check_balanced=True)._recompute_dynamic_lines(recompute_all_taxes=True)
        return True

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def default_get(self, default_fields):
        # OVERRIDE
        values = super(AccountMoveLine, self).default_get(default_fields)
        if values.get('account_id') and values.get('new_fiscal_position_id'):
            new_fiscal_position = self.env['account.fiscal.position'].browse(values.get('new_fiscal_position_id'))
            account = self.env['account.account'].browse(values.get('account_id'))
            account_id = new_fiscal_position.map_account(account=account)
            if account_id:
                values['account_id'] = account_id.id
        return values

    new_fiscal_position_id = fields.Many2one('account.fiscal.position', string='Temporary fiscal position')

    def _get_computed_account(self):
        self.ensure_one()

        if not self.product_id:
            return

        fiscal_position = self.move_id.new_fiscal_position_id or self.move_id.fiscal_position_id
        accounts = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
        if self.move_id.is_sale_document(include_receipts=True):
            # Out invoice.
            return accounts['income']
        elif self.move_id.is_purchase_document(include_receipts=True):
            # In invoice.
            return accounts['expense']

    @api.onchange('product_id')
    def _onchange_product_id(self):
        result = super(AccountMoveLine, self)._onchange_product_id()
        for line in self:
            if line.tax_ids and line.move_id.new_fiscal_position_id:
                line.tax_ids = line.move_id.new_fiscal_position_id.map_tax(line.tax_ids._origin, partner=line.move_id.partner_id)
        return result

    @api.onchange('account_id')
    def _onchange_account_id(self):
        ''' Recompute 'tax_ids' based on 'account_id'.
        /!\ Don't remove existing taxes if there is no explicit taxes set on the account.
        '''
        if not self.display_type and (self.account_id.tax_ids or not self.tax_ids):
            taxes = self._get_computed_taxes()

            fiscal_position = self.move_id.new_fiscal_position_id or self.move_id.fiscal_position_id
            if taxes and fiscal_position:
                taxes = fiscal_position.map_tax(taxes, partner=self.partner_id)

            self.tax_ids = taxes

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'
    _description = 'Fiscal Position'
    _order = 'sequence'

    related_fiscal_position_id = fields.Many2one('account.fiscal.position', string='Temporary fiscal position')
    default = fields.Boolean(string='Default temp. fiscal position')
