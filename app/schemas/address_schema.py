from marshmallow import Schema, fields, validate


class AddressCreateSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    phone = fields.Str(required=True, validate=validate.Length(min=6, max=20))
    street = fields.Str(required=True, validate=validate.Length(min=5, max=255))
    city = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    state = fields.Str(validate=validate.Length(max=100))
    postal_code = fields.Str(validate=validate.Length(max=20))
    country = fields.Str(validate=validate.Length(max=100))
    is_default = fields.Bool(load_default=False)


class AddressUpdateSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=2, max=100))
    phone = fields.Str(validate=validate.Length(min=6, max=20))
    street = fields.Str(validate=validate.Length(min=5, max=255))
    city = fields.Str(validate=validate.Length(min=2, max=100))
    state = fields.Str(validate=validate.Length(max=100))
    postal_code = fields.Str(validate=validate.Length(max=20))
    country = fields.Str(validate=validate.Length(max=100))
    is_default = fields.Bool()
