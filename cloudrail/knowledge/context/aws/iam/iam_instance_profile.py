from typing import List

from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class IamInstanceProfile(AwsResource):
    """
        Attributes:
            role_name: The name of the role.
            iam_instance_profile_id: The ID of the instance profile.
            ec2_instance_data: The Ec2Instance using this profile.
    """
    def __init__(self, account: str, region: str, role_name: str, iam_instance_profile_id: str):
        super().__init__(account, region, AwsServiceName.AWS_IAM_INSTANCE_PROFILE)
        self.role_name: str = role_name
        self.region: str = region
        self.iam_instance_profile_id: str = iam_instance_profile_id
        self.ec2_instance_data: Ec2Instance = None

    def get_keys(self) -> List[str]:
        return [self.iam_instance_profile_id]

    def get_extra_data(self) -> str:
        role_name = 'role_name: {}'.format(self.role_name) if self.role_name else ''

        return ', '.join([role_name])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Instance profile'
        else:
            return 'IAM Instance profiles'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#InstanceDetails:instanceId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.ec2_instance_data.instance_id)

    @property
    def is_tagable(self) -> bool:
        return False
