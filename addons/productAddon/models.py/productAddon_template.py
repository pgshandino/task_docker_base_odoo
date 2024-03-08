from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    slug = fields.Char(string="Slug", compute="_compute_slug")
    additional_barcode = fields.Char(string="Additional Barcode", required=True, unique=True)

    @api.depends('name')
    def _compute_slug(self):
        for record in self:
            # Generate a slug from the product name (replace spaces with hyphens)
            record.slug = record.name.lower().replace(" ", "-")

    @api.onchange('additional_barcode')
    def _check_unique_barcode(self):
        for record in self:
            # Check if the additional barcode already exists for another product
            if self.search_count([('additional_barcode', '=', record.additional_barcode), ('id', '!=', record.id)]):
                # Raise an error if the barcode is not unique
                raise ValidationError("This additional barcode is already used for another product.")