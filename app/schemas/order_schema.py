from marshmallow import Schema, fields, validate


class OrderCreateSchema(Schema):
    address_id = fields.Int(required=True)
    notes = fields.Str(validate=validate.Length(max=1000))
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(["cash_on_delivery", "credit_card", "paypal", "bank_transfer"])
    )


class OrderCancelSchema(Schema):
    reason = fields.Str(required=True, validate=validate.Length(min=5, max=500))
