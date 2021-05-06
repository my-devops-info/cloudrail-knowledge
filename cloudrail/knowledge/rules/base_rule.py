import logging
import time
from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, TypeVar, Generic
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.mergeable import Mergeable


@dataclass
class Issue:
    evidence: str
    exposed: Mergeable
    violating: Mergeable


class RuleResultType(str, Enum):
    SUCCESS = 'success'
    FAILED = 'failed'
    SKIPPED = 'skipped'


@dataclass
class RuleResponse:
    rule_id: str
    status: RuleResultType
    issues: List[Issue] = field(default_factory=list)


EnvCtx = TypeVar('EnvCtx')


class BaseRule(Generic[EnvCtx]):
    def validate_parameters(self, parameter_types: List[ParameterType]) -> bool:
        for parameter_type in self.get_needed_parameters():
            if parameter_type not in parameter_types:
                logging.warning('Rule : {} failed to run!\nMissing parameter type: {}'.format(self.get_id(),
                                                                                              parameter_type))
                return False
        return True

    def run(self,
            environment_context: EnvCtx,
            parameters: Dict[ParameterType, dict]) -> RuleResponse:
        if not self.should_run_rule(environment_context):
            logging.info('skipped rule {}, reason {}'.format(self.get_id(), 'no relevant resources'))
            return RuleResponse(self.get_id(), RuleResultType.SKIPPED)

        logging.info('start run rule {}'.format(self.get_id()))
        start_time: float = time.time()
        if self.validate_parameters(list(parameters.keys())):
            total_issues = self.execute(environment_context, parameters)
            filtered_missing_data_issues = self._filter_missing_data_issues(total_issues)

            logging.info(f'run rule {self.get_id()} completed in {(time.time() - start_time)}s.\n'
                         f'number of total issue items: {len(total_issues)}\n'
                         f'number of non missing data issues: {len(filtered_missing_data_issues)}\n')
            final_issues_list = filtered_missing_data_issues

            if not final_issues_list:
                rule_result = RuleResponse(self.get_id(), RuleResultType.SUCCESS)
            else:
                rule_result = RuleResponse(self.get_id(), RuleResultType.FAILED, final_issues_list)
        else:
            rule_result = RuleResponse(self.get_id(), RuleResultType.SKIPPED)
        logging.info('finish run rule {}'.format(self.get_id()))
        return rule_result

    @staticmethod
    def _filter_missing_data_issues(issues: List[Issue]) -> List[Issue]:
        return [issue for issue in issues if issue.exposed and issue.violating]

    @abstractmethod
    def execute(self, env_context: EnvCtx, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_needed_parameters(self) -> List[ParameterType]:
        pass

    @staticmethod
    def filter_non_iac_managed_issues() -> bool:
        return True

    @abstractmethod
    def should_run_rule(self, environment_context: EnvCtx) -> bool:
        return True
