from cloudrail.knowledge.context.azure.webapp.constants import FtpsState


class SiteConfig:
    """
        Attributes:
            http2_enabled: Indication if http2 protocol should be enabled or not.
    """
    def __init__(self, ftps_state: FtpsState, http2_enabled: bool) -> None:
        super().__init__()
        self.ftps_state: FtpsState = ftps_state
        self.http2_enabled: bool = http2_enabled
