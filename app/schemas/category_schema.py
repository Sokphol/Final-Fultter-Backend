from marshmallow import Schema, fields, validate


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    image_url = fields.Str(validate=validate.Length(max=500))
    is_active = fields.Bool(load_default=True)
    sort_order = fields.Int(load_default=0)


class CategoryUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    image_url = fields.Str(validate=validate.Length(max=500))
    is_active = fields.Bool()
    sort_order = fields.Int()
