_scene_registry = {}


def register(name, scene_cls):
    _scene_registry[name] = scene_cls


def get_scene(name):
    scene_cls = _scene_registry.get(name)
    if scene_cls is None:
        raise ValueError(f"Scene '{name}' is not registered.")
    return scene_cls
