# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    new_property_account_position_id = fields.Many2one('account.fiscal.position', company_dependent=True, string="Temporary fiscal position")

    @api.onchange('property_account_position_id')
    def _onchange_property_account_position_id(self):
        self.new_property_account_position_id = False
        if self.property_account_position_id:
            self.new_property_account_position_id = self.property_account_position_id.related_fiscal_position_id.id or False

    @api.model
    def set_new_fiscal_position(self):
        fiscal_pool = self.env['account.fiscal.position']
        context = dict(self._context)
        records = self.search([('id', 'in', context.get('active_ids'))])
        for record in records:
            if record.property_account_position_id and record.property_account_position_id.related_fiscal_position_id:
                record.new_property_account_position_id = record.property_account_position_id.related_fiscal_position_id.id or False
            elif not record.property_account_position_id:
                fiscal_id = fiscal_pool.sudo().search([('default', '!=', False)], limit=1)
                if fiscal_id:
                    record.new_property_account_position_id = fiscal_id.id
        return True

    @api.model
    def remove_new_fiscal_position(self):
        context = dict(self._context)
        records = self.search([('id', 'in', context.get('active_ids'))])
        for record in records:
            record.new_property_account_position_id = False
            for child in record.child_ids:
                child.new_property_account_position_id = False
                related_ids = self.search([('parent_id', '=', child.id)])
                for related in related_ids:
                    related.new_property_account_position_id = False
        return True

    def set_new_property_account_position(self, new_property_account_position_id=False):
        for child in self.child_ids:
            child.new_property_account_position_id = new_property_account_position_id
            related_ids = self.search([('parent_id', '=', child.id)])
            for related in related_ids:
                related.new_property_account_position_id = new_property_account_position_id

    def write(self, values):
        res = super(ResPartner, self).write(values)
        if values.get('new_property_account_position_id'):
            for record in self:
                record.set_new_property_account_position(new_property_account_position_id=values.get('new_property_account_position_id'))
        return res


class ResCompany(models.Model):
    _inherit = 'res.company'

    fiscal_position_date_start = fields.Date(string='Start date')
    fiscal_position_date_stop = fields.Date(string='End date')
