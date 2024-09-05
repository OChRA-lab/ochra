from uuid import UUID


class RestProxyMixin:

    def _mixin_hook(self, endpoint: str, id: UUID) -> None:
        for field in self.model_fields.keys():

            def getter(self, name=field):
                value = f"GET {endpoint}/{id}/get_property/{name}"
                return value

            def setter(self, value, name=field):
                print(f"PATCH {endpoint}/{id}/set_property/{name} -> {value}")

            # Set the property on the class with the custom getter and setter
            setattr(self.__class__, field, property(getter, setter))
