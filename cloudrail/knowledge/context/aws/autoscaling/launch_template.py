from typing import List, Optional

from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class LaunchTemplate(AwsResource):

    def __init__(self,
                 template_id: str,
                 name: str,
                 http_token: str,
                 image_id: str,
                 security_group_ids: List[str],
                 version_number: int,
                 region: str,
                 account: str,
                 iam_instance_profile: Optional[str],
                 network_configurations: List[NetworkConfiguration] = None):
        super().__init__(account, region, AwsServiceName.AWS_LAUNCH_TEMPLATE)
        self.template_id: str = template_id
        self.name: str = name
        self.http_token: str = http_token
        self.image_id: str = image_id
        self.security_group_ids: List[str] = security_group_ids
        self.version_number: int = version_number
        self.iam_instance_profile: Optional[str] = iam_instance_profile
        self.network_configurations: List[NetworkConfiguration] = network_configurations or []
        self.security_groups: List[SecurityGroup] = []

    def get_keys(self) -> List[str]:
        return [self.template_id, self.version_number]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.template_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Launch template'
        else:
            return 'Launch templates'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#LaunchTemplateDetails:launchTemplateId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.template_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
