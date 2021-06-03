from cloudrail.knowledge.context.azure.azure_resources.web_app.constants import FieldMode


class AuthSettings:

    def __init__(self, enabled: bool, client_cert_mode: FieldMode) -> None:
        self.enabled: bool = enabled
        self.client_cert_mode: FieldMode = client_cert_mode
