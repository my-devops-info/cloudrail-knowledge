from cloudrail.knowledge.context.azure.webapp.constants import FtpsState


class SiteConfig:

    def __init__(self, ftps_state: FtpsState) -> None:
        super().__init__()
        self.ftps_state: FtpsState = ftps_state
