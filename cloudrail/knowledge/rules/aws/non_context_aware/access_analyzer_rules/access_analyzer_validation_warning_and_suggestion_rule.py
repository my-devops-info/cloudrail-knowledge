from typing import Set

from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_base_rule import AccessAnalyzerValidationBaseRule


class AccessAnalyzerValidationWarningAndSuggestionRule(AccessAnalyzerValidationBaseRule):

    def get_id(self) -> str:
        return 'not_car_access_analyzer_validation_warning_and_suggestion'

    def _get_violated_finding_types(self) -> Set[str]:
        return {'WARNING', 'SUGGESTION'}
