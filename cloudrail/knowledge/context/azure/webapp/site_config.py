from cloudrail.knowledge.context.azure.webapp.constants import FtpState


class SiteConfig:

    def __init__(self, ftp_state: FtpState) -> None:
        super().__init__()
        self.ftp_state: FtpState = ftp_state
