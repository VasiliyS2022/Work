from rest_framework import serializers
from album.models import Album
from copy import copy, deepcopy


class AlbumSerializer(serializers.ModelSerializer):
    album = serializers.StringRelatedField(read_only=True, source="__str__")
    artist_name = serializers.StringRelatedField(source="artist.name")
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ["album", "name", "artist_name", "tracks"]

    def to_representation(self, value):
        primitive_repr = super(AlbumSerializer, self).to_representation(value)
        fields = self.get_fields().items()

        return self.rename_fields(fields, primitive_repr)

    @staticmethod
    def rename_fields(fields, primitive_repr):
        primitive_repr = copy(primitive_repr)

        for field_name, field_type in fields:
            if (
                isinstance(field_type, serializers.StringRelatedField)
                and len(field_type.source.split(".")) > 1
            ):
                new_field_name = field_type.source.replace(".", "@")
                primitive_repr[new_field_name] = primitive_repr[field_name]
                primitive_repr.pop(field_name)
        return primitive_repr