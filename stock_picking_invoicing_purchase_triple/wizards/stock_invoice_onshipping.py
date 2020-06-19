# Copyright (C) 2020-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class StockInvoiceOnshipping(models.TransientModel):
    _inherit = 'stock.invoice.onshipping'

    @api.multi
    def _get_invoice_line_values(self, moves, invoice_values, invoice):
        values = super()._get_invoice_line_values(
            moves=moves, invoice_values=invoice_values, invoice=invoice)
        inv_type = invoice_values['type']
        move = fields.first(moves)
        product = move.product_id
        if inv_type in ['in_invoice', 'in_refund']:
            if len(moves.mapped('purchase_line_id')) == 1:
                purchase_line = moves.mapped('purchase_line_id')[0]
                price = purchase_line.price_unit or 0
                discount = purchase_line.discount or 0
                discount2 = purchase_line.discount2 or 0
                discount3 = purchase_line.discount3 or 0
                uom = moves.mapped('product_uom')[0] \
                    if len(moves.mapped('product_uom')) == 1 else product.uom_id
                if uom.id != product.uom_id.id:
                    price *= uom.factor / product.uom_id.factor
                values.update({
                    'uom_id': uom.id,
                    'price_unit': price,
                    'discount': discount,
                    'discount2': discount2,
                    'discount3': discount3,
                    'purchase_line_id': purchase_line.id if purchase_line else False,
                })
        return values
