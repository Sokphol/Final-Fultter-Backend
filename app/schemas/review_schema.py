from marshmallow import Schema, fields, validate


class ReviewCreateSchema(Schema):
    product_id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    title = fields.Str(validate=validate.Length(max=200))
    body = fields.Str(validate=validate.Length(max=5000))


class ReviewUpdateSchema(Schema):
    rating = fields.Int(validate=validate.Range(min=1, max=5))
    title = fields.Str(validate=validate.Length(max=200))
    body = fields.Str(validate=validate.Length(max=5000))
