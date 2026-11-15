from marshmallow import Schema, fields, validate


class CartAddItemSchema(Schema):
    product_id = fields.Int(required=True)
    variant_id = fields.Int(allow_none=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1, max=100))


class CartUpdateItemSchema(Schema):
    quantity = fields.Int(required=True, validate=validate.Range(min=1, max=100))
