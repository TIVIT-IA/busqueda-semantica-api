from functools import wraps
from dependency_injector import containers, providers
from recomendations.core.service.impl.recomendations_service_impl import RecomendationsServiceImpl
from recomendations.core.service.recomendations_service import RecomendationsService



class Container(containers.DeclarativeContainer):
    recomendationsService = providers.Factory(RecomendationsServiceImpl)


def inject(attr_name: str, provider_class_or_callable):
    """
    Decorador de clase para inyección automática.
    - attr_name: nombre del atributo que recibirá la dependencia
    - provider_class_or_callable: puede ser una clase o un callable que devuelve la instancia
    """
    def decorator(cls):
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            if isinstance(provider_class_or_callable, type):
                container_method_name = provider_class_or_callable.__name__[0].lower() + provider_class_or_callable.__name__[1:]
                container = Container()
                if not hasattr(container, container_method_name):
                    raise AttributeError(f"Container no tiene un proveedor llamado '{container_method_name}'")
                instance = getattr(container, container_method_name)()
            else:
                instance = provider_class_or_callable()
            setattr(self, attr_name, instance)

        cls.__init__ = new_init
        return cls
    return decorator
