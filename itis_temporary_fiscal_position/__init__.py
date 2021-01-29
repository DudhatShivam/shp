# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.

from . import models

from odoo import api, SUPERUSER_ID

def _add_server_action_menu(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    new_fiscal_position_contact = env.ref('itis_temporary_fiscal_position.action_set_new_fiscal_position_contact', False)
    new_fiscal_position_contact.create_action()
    remove_new_fiscal_position_contact = env.ref('itis_temporary_fiscal_position.action_remove_new_fiscal_position_contact', False)
    remove_new_fiscal_position_contact.create_action()
    appply_fiscal_position_sale = env.ref('itis_temporary_fiscal_position.action_apply_fiscal_position_sale', False)
    appply_fiscal_position_sale.create_action()
    appply_fiscal_position_purchase = env.ref('itis_temporary_fiscal_position.action_apply_fiscal_position_purchase', False)
    appply_fiscal_position_purchase.create_action()
    appply_fiscal_position_invoice = env.ref('itis_temporary_fiscal_position.action_apply_fiscal_position_invoice', False)
    appply_fiscal_position_invoice.create_action()
    apply_old_tax_sale = env.ref('itis_temporary_fiscal_position.action_apply_old_tax_sale', False)
    apply_old_tax_sale.create_action()
    apply_old_tax_purchase = env.ref('itis_temporary_fiscal_position.action_apply_old_tax_purchase', False)
    apply_old_tax_purchase.create_action()
    apply_old_tax_invoice = env.ref('itis_temporary_fiscal_position.action_apply_old_tax_invoice', False)
    apply_old_tax_invoice.create_action()
