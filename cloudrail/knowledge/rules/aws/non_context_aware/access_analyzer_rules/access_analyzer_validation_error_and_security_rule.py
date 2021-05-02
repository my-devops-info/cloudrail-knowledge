from typing import Set

from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_base_rule import AccessAnalyzerValidationBaseRule


class AccessAnalyzerValidationErrorAndSecurityRule(AccessAnalyzerValidationBaseRule):

    def get_id(self) -> str:
        return 'not_car_access_analyzer_validation_error_and_security'

    def _get_violated_finding_types(self) -> Set[str]:
        return {'ERROR', 'SECURITY_WARNING'}
