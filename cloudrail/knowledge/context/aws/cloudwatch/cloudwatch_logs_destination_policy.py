from typing import List
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement


class CloudWatchLogsDestinationPolicy(Policy):

    def __init__(self,
                 destination_name: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 region: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_CLOUDWATCH_LOG_DESTINATION_POLICY)
        self.destination_name: str = destination_name
        self.region: str = region

    def get_keys(self) -> List[str]:
        return [self.destination_name, self.region, self.account]

    def get_name(self) -> str:
        return self.destination_name + " policy"

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudWatch Logs Destination policy'
        else:
            return 'CloudWatch Logs Destination policies'

    @property
    def is_tagable(self) -> bool:
        return False
