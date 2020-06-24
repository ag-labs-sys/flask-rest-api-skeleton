from marshmallow import Schema, fields, post_load


class TaskSchema(Schema):

    id = fields.UUID()
    text = fields.Str()
    timestamp = fields.Str()

    class Meta:
        fields = ('id', 'text', 'timestamp')

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)


class Task():

    def __init__(self, id, text, timestamp):

        self.id = id
        self.text = text
        self.timestamp = timestamp

