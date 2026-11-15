from marshmallow import Schema, fields, validate


class BrandCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    logo_url = fields.Str(validate=validate.Length(max=500))
    website = fields.Str(validate=validate.Length(max=255))
    is_active = fields.Bool(load_default=True)


class BrandUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=1000))
    logo_url = fields.Str(validate=validate.Length(max=500))
    website = fields.Str(validate=validate.Length(max=255))
    is_active = fields.Bool()
