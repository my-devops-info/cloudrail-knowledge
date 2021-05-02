from typing import List
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class CodeBuildProject(AwsResource):

    def __init__(self,
                 project_name: str,
                 encryption_key: str,
                 arn: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_CODEBUILD_PROJECT)
        self.project_name: str = project_name
        self.encryption_key: str = encryption_key
        self.arn: str = arn
        self.kms_data: KmsKey = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.project_name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CodeBuild'
        else:
            return 'CodeBuilds'

    def get_cloud_resource_url(self) -> str:
        return '{0}codesuite/codebuild/{1}/projects/{2}/'\
            .format(self.AWS_CONSOLE_URL, self.account, self.project_name)

    @property
    def is_tagable(self) -> bool:
        return True
