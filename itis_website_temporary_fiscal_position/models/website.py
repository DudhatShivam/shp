# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        self.ensure_one()
        partner = self.env.user.partner_id
        sale_order = super(Website, self).sale_get_order(force_create=force_create, code=code, update_pricelist=update_pricelist, force_pricelist=force_pricelist)
        if sale_order:
            if force_create or code:
                # set fiscal position
                sale_order.onchange_partner_id()
            if self.env.ref('base.de').id == sale_order.partner_id.country_id.id:
            # if sale_order.partner_id != request.website.user_id.sudo().partner_id:
                sale_order.partner_id.with_context({'active_ids': [sale_order.partner_id.id]}).set_new_fiscal_position()
                sale_order.onchange_partner_id()
                sale_order.onchange_partner_shipping_id() # fiscal position
        return sale_order
