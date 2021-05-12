from cloudrail.knowledge.context.aws.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import PrincipalType
from cloudrail.knowledge.context.aws.iam.role import Role


def is_allowing_external_assume(policy: AssumeRolePolicy, role: Role) -> bool:
    valid_principal_values = [role.account, 'amazonaws.com']
    for statement in policy.statements:
        return statement.principal.principal_values and \
               statement.principal.principal_type != PrincipalType.SERVICE and \
               any(all(valid_string not in value for valid_string in valid_principal_values) for value in statement.principal.principal_values) and \
               statement.effect == StatementEffect.ALLOW and \
               any('AssumeRole' in action for action in statement.actions)
