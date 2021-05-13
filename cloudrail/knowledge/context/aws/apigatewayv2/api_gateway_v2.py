from typing import List, Optional

from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class ApiGateway(AwsResource):

    def __init__(self,
                 account: str,
                 region: str,
                 api_gw_id: str,
                 api_gw_name: str,
                 protocol_type: str,
                 arn: Optional[str]):
        super().__init__(account, region, AwsServiceName.AWS_REST_API_GW)
        self.api_gw_id: str = api_gw_id
        self.api_gw_name: str = api_gw_name
        self.protocol_type: str = protocol_type
        self.arn: Optional[str] = arn

    def get_keys(self) -> List[str]:
        return [self.api_gw_id]

    def get_id(self) -> str:
        return self.api_gw_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'API Gateway'
        else:
            return 'API Gateways'

    def get_arn(self) -> str:
        if self.arn:
            return self.arn
        else:
            return f'arn:aws:apigateway:{self.region}::/apis/{self.api_gw_id}'

    def get_cloud_resource_url(self) -> str:
        return '{0}apigateway/main/api-detail/?api={1}&region={2}'\
            .format(self.AWS_CONSOLE_URL, self.api_gw_id, self.region)

    @property
    def is_tagable(self) -> bool:
        return True
