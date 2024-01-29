from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer



class ExtendedAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    group_name = None
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)



    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class



    def get_serializer_context(self):
        """
        Extra context provided to the serializer class, containing scope and consumer.
        """
        return {
            'scope': self.scope,
            'consumer': self
        }
    
    def save_model_serializer_data(serializer):
        serializer.save()





class ExtendedWebsocketConsumer(WebsocketConsumer):
    group_name = None
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)



    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class



    def get_serializer_context(self):
        """
        Extra context provided to the serializer class, containing scope and consumer.
        """
        return {
            'scope': self.scope,
            'consumer': self
        }


    def save_model_serializer_data(serializer):
        serializer.save()