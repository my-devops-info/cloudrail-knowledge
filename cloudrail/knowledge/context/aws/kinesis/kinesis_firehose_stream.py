from typing import List

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class KinesisFirehoseStream(AwsResource):

    def __init__(self,
                 stream_name: str,
                 stream_arn: str,
                 encrypted_at_rest: bool,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_KINESIS_FIREHOSE_DELIVERY_STREAM)
        self.stream_name: str = stream_name
        self.stream_arn: str = stream_arn
        self.encrypted_at_rest: bool = encrypted_at_rest

    def get_keys(self) -> List[str]:
        return [self.stream_arn]

    def get_name(self) -> str:
        return self.stream_name

    def get_arn(self) -> str:
        return self.stream_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Kinesis Data Firehose'
        else:
            return 'Kinesis Data Firehoses'

    def get_cloud_resource_url(self) -> str:
        return '{0}firehose/home?region={1}#/details/{2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.stream_name)

    @property
    def is_tagable(self) -> bool:
        return True
