from typing import Optional, List, Dict

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class OriginAccessIdentity(AwsResource):

    def __init__(self, account: str, region: str, oai_id: str, cloudfront_access_identity_path: str,
                 iam_arn: str, s3_canonical_user_id: str, tags: Dict[str, str] = None):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDFRONT_ORIGIN_ACCESS_IDENTITY)
        self.oai_id: str = oai_id
        self.cloudfront_access_identity_path: str = cloudfront_access_identity_path
        self.iam_arn: str = iam_arn
        self.s3_canonical_user_id: str = s3_canonical_user_id
        if tags:
            self.tags = tags

    def get_keys(self) -> List[str]:
        return [self.oai_id]

    def get_arn(self) -> str:
        return self.iam_arn

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}cloudfront/home?region={1}#/oai:' \
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
