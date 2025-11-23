from functools import wraps
from dependency_injector import containers, providers
from recomendations.core.service.impl.recomendations_service_impl import RecomendationsServiceImpl
from recomendations.core.service.recomendations_service import RecomendationsService


# -----------------------
# Contenedor de dependencias
# -----------------------
class Container(containers.DeclarativeContainer):
    # El nombre debe coincidir con lo que el decorador @inject espera
    recomendationsService = providers.Factory(RecomendationsServiceImpl)


# -----------------------
# Decorador de inyección de dependencias
# -----------------------
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
            # Llamar al constructor original
            original_init(self, *args, **kwargs)

            # Crear la instancia de la dependencia
            if isinstance(provider_class_or_callable, type):
                # Obtener el nombre del proveedor en el container
                container_method_name = provider_class_or_callable.__name__[0].lower() + provider_class_or_callable.__name__[1:]
                container = Container()
                if not hasattr(container, container_method_name):
                    raise AttributeError(f"Container no tiene un proveedor llamado '{container_method_name}'")
                instance = getattr(container, container_method_name)()
            else:
                # Si es callable, se ejecuta para obtener la instancia
                instance = provider_class_or_callable()

            # Asignar la dependencia al atributo de la clase
            setattr(self, attr_name, instance)

        cls.__init__ = new_init
        return cls
    return decorator
