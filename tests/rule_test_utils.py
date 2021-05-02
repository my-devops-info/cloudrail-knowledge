import inspect


def create_empty_entity(class_type):
    signature = inspect.signature(class_type.__init__)
    params = {}
    for param in list(signature.parameters)[1:]:
        params[param] = None
    return class_type(**params)
