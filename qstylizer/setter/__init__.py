

class Setter(object):

    _descriptor_cls = None

    @classmethod
    def get_attributes(cls):
        attributes = {}
        for class_ in cls.__bases__:
            if not issubclass(class_, Setter) or class_._descriptor_cls is None:
                continue
            attributes.update({
                key: value for key, value in class_.__dict__.items()
                if isinstance(value, class_._descriptor_cls)
            })
            attributes.update(class_.get_attributes())
        if cls._descriptor_cls is not None:
            attributes.update({
                key: value for key, value in cls.__dict__.items()
                if isinstance(value, cls._descriptor_cls)
            })
        return attributes

    @classmethod
    def get_attr_options(cls):
        return set(
            [x.replace("_", "-") for x, y in cls.get_attributes().items()]
        )
