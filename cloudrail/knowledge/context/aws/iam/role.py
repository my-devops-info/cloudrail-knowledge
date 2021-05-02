from typing import List, Dict, Optional

from cloudrail.knowledge.context.aws.aws_connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.iam.iam_identity import IamIdentity


class Role(IamIdentity):

    def __init__(self, account: str,
                 qualified_arn: str,
                 role_name: str,
                 instance_profile_ids: List[str],
                 role_id: str,
                 permission_boundary_arn: Optional[str],
                 arn: str = None):
        super().__init__(account, qualified_arn, arn, AwsServiceName.AWS_IAM_ROLE)
        self.role_name: str = role_name
        self.instance_profile_ids: List[str] = instance_profile_ids
        self.role_id: str = role_id
        self.permission_boundary_arn: Optional[str] = permission_boundary_arn
        self.assume_role_policy: AssumeRolePolicy = None
        self.policy_evaluation_result_map: Dict[str, PolicyEvaluation] = {}

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_id(self) -> str:
        return self.role_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Role'
        else:
            return 'IAM Roles'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/roles/{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.role_name)

    def clone(self):
        role = Role(account=self.account, qualified_arn=self.qualified_arn, role_name=self.role_name,
                    instance_profile_ids=list(self.instance_profile_ids), role_id=self.role_id,
                    permission_boundary_arn=self.permission_boundary_arn, arn=self.arn)
        role.assume_role_policy = self.assume_role_policy
        return role

    @property
    def is_tagable(self) -> bool:
        return True
