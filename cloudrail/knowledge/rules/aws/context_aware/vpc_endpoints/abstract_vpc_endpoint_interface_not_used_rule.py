from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.aws.ec2.vpc_endpoint import VpcEndpointInterface
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.aws.service_name import AwsServiceType
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_rule import AbstractVpcEndpointRule


class AbstractVpcEndpointInterfaceNotUsedRule(AbstractVpcEndpointRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        vpc_list, region_to_service_map, vpc_to_eni_map = self._init_maps(env_context)
        issues_list: List[Issue] = []

        for vpc in vpc_list:
            for eni in vpc_to_eni_map.get(vpc, []):
                violating_eni_found: bool = False
                if not isinstance(eni.owner, VpcEndpointInterface) and self._is_service_eni_match(eni):
                    for service in region_to_service_map[eni.vpc.region]:
                        if eni.is_outbound_public() and not ((vpc.enable_dns_support or vpc.enable_dns_hostnames)
                                                             and self._is_vpce_interface_connection_exist(eni)):
                            issues_list.append(Issue(f"The service {self.aws_service_type.name} is in use in region `{vpc.region}`,"
                                                     f" but VPC `{vpc.get_friendly_name()}`. is not configured to"
                                                     f" use a VPC Endpoint for {self.aws_service_type.name}",
                                                     service, vpc))
                            violating_eni_found = True
                if violating_eni_found:
                    break
        return issues_list


class SqsVpcEndpointExposureRule(AbstractVpcEndpointInterfaceNotUsedRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.SQS, (443, ), [], False)

    def get_id(self) -> str:
        return 'vpc_endpoint_sqs_exposure'


class Ec2VpcEndpointExposureRule(AbstractVpcEndpointInterfaceNotUsedRule):

    def __init__(self) -> None:
        super().__init__(AwsServiceType.EC2, (443, ), [], False)

    def get_id(self) -> str:
        return 'vpc_endpoint_ec2_exposure'
