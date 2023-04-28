from typing_extensions import Self


class BaseDataIntermediary:
    @classmethod
    def from_model(cls, obj) -> Self:
        raise NotImplementedError

    def to_schema(self):
        raise NotImplementedError

    @classmethod
    def model_to_schema(cls, obj):
        return cls.from_model(obj).to_schema()
