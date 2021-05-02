from dataclasses import dataclass, field
from typing import List, Optional, Dict
from cloudrail.knowledge.context.aws.aws_connection import ConnectionInstance
from cloudrail.knowledge.context.aws.cloudfront.origin_access_identity import OriginAccessIdentity
from cloudrail.knowledge.context.aws.service_name import AwsServiceName, AwsServiceType, AwsServiceAttributes
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


@dataclass
class OriginConfig:
    domain_name: str
    origin_id: str
    oai_path: str
    origin_access_identity_list: List[OriginAccessIdentity] = field(default_factory=list)


@dataclass
class ViewerCertificate:
    cloudfront_default_certificate: bool
    minimum_protocol_version: str


@dataclass
class CacheBehavior:
    allowed_methods: List[str]
    cached_methods: List[str]
    target_origin_id: str
    viewer_protocol_policy: str
    precedence: int
    path_pattern: str = field(default="*")
    trusted_signers: List[str] = field(default=list)
    field_level_encryption_id: str = field(default=None)


class CloudFrontDistribution(AwsResource, ConnectionInstance):

    def __init__(self,
                 arn: str,
                 name: str,
                 distribution_id: str,
                 account: str,
                 viewer_cert: ViewerCertificate,
                 cache_behavior_list: List[CacheBehavior],
                 origin_config_list: List[OriginConfig],
                 tags: Dict[str, str] = None):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_CLOUDFRONT_DISTRIBUTION_LIST,
                         aws_service_attributes=AwsServiceAttributes(AwsServiceType.CLOUDFRONT.value))
        ConnectionInstance.__init__(self)
        self.arn: str = arn
        self.name: str = name
        self.distribution_id: str = distribution_id
        self.viewer_cert: ViewerCertificate = viewer_cert
        self._cache_behavior_list: List[CacheBehavior] = cache_behavior_list
        self.origin_config_list: List[OriginConfig] = origin_config_list
        if tags:
            self.tags = tags

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.distribution_id

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudFront Distribution'
        else:
            return 'CloudFront Distributions'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudfront/home?region={1}#distribution-settings:{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.distribution_id)

    @property
    def is_tagable(self) -> bool:
        return True

    def get_default_behavior(self) -> Optional[CacheBehavior]:
        for cache in self._cache_behavior_list:
            if cache.path_pattern == "*":
                return cache
        return None

    def get_ordered_behavior_list(self) -> List[CacheBehavior]:
        return [cache for cache in self._cache_behavior_list if cache.path_pattern != "*"]

    def get_all_cache_behaviors(self):
        return list(self._cache_behavior_list)
