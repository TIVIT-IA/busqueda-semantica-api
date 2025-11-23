from typing import Callable
from fastapi import APIRouter

# -----------------------
# Decoradores para endpoints
# -----------------------
def post(path: str):
    def wrapper(func: Callable):
        func._endpoint = {"method": "POST", "path": path}
        return func
    return wrapper

def get(path: str):
    def wrapper(func: Callable):
        func._endpoint = {"method": "GET", "path": path}
        return func
    return wrapper

# -----------------------
# BaseController que registra métodos
# -----------------------
class BaseController:
    def __init__(self, prefix: str = ""):
        # Asegurarse de que prefix siempre sea string
        self._prefix = prefix or ""

    def register_routes(self, router: APIRouter):
        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if callable(method) and hasattr(method, "_endpoint"):
                info = method._endpoint
                # Concatenar el prefix seguro
                full_path = self._prefix.rstrip("/") + info["path"]
                router.add_api_route(
                    path=full_path,
                    endpoint=method,
                    methods=[info["method"]]
                )

# -----------------------
# Decorador de clase para router
# -----------------------
def router(prefix: str):
    def wrapper(cls):
        from recomendations.config.dependency_injection import Container

        r = APIRouter(prefix=prefix)

        init_params = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]
        kwargs = {param: None for param in init_params}

        # Crear instancia del container
        container = Container()

        # Si la clase tiene atributo service, inyectarlo aquí
        if hasattr(cls, '__annotations__') and 'service' in cls.__annotations__:
            kwargs['service'] = container.recomendationsService() # type: ignore

        instance = cls(**kwargs) if init_params else cls()

        instance.register_routes(r)
        cls.router = r
        return cls
    return wrapper

