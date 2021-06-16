from typing import List, Optional

from cloudrail.knowledge.context.aws.lambda_.lambda_alias import create_lambda_function_arn
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.utils.utils import hash_list


class LambdaPolicyStatements(Policy):
    """
        Attributes:
            function_name: The name of the Lambda Function the policy statements are for.
            statements: The statements themselves.
            qualifier: A Lambda Function may have a qualified set, this will be it
                (or None).
    """
    def __init__(self, account: str, region: str, function_name: str,
                 statements: List[PolicyStatement], qualifier: str = None):
        super().__init__(account, statements, None, AwsServiceName.AWS_LAMBDA_PERMISSION)
        self.function_name: str = function_name
        self.statements: List[PolicyStatement] = statements
        self.qualifier: str = qualifier
        self.region: str = region

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_id(self) -> str:
        return str(hash_list([stat.statement_id for stat in self.statements]))

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}lambda/home?{1}#/functions/{2}?tab=permissions'\
            .format(self.AWS_CONSOLE_URL, self.region, self.function_name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def lambda_func_arn(self) -> str:
        if ':' in self.function_name:
            return self.function_name
        else:
            return create_lambda_function_arn(self.account, self.region, self.function_name, self.qualifier)
