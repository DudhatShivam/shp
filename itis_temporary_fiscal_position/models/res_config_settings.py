# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fiscal_position_date_start = fields.Date(string='Start date', related='company_id.fiscal_position_date_start', readonly=False)
    fiscal_position_date_stop = fields.Date(string='End date', related='company_id.fiscal_position_date_stop', readonly=False)
