import functools
import logging
import re
from typing import Set, List, Optional, Iterable, Dict


@functools.lru_cache(maxsize=None)
def is_action_fully_defined(contained_action: str, container_action: str):
    try:
        if container_action == '*':
            return True
        if contained_action == '*':
            return False

        contained_splitted = contained_action.split(':')
        container_splitted = container_action.split(':')

        if not contained_splitted[0] == container_splitted[0]:
            return False

        pattern = re.compile(container_action.replace('*', '.*', -1))
        return pattern.fullmatch(contained_action)
    except Exception:
        logging.exception('got exception while checking action {} vs {}'.format(contained_action, container_action))
        return False


def get_intersected_actions(actions: Iterable[str], action: str) -> List[str]:
    results = [get_intersect_action(action, action_from_set) for action_from_set in actions]
    return [result for result in results if result is not None]


@functools.lru_cache(maxsize=None)
def get_intersect_action(action_a: str, action_b: str) -> Optional[str]:
    if is_action_fully_defined(action_a, action_b):
        return action_a
    if is_action_fully_defined(action_b, action_a):
        return action_b
    return None


def is_combo_escalation_permissions_match(actions: Set[str]) -> bool:
    esc_actions_list: List[Set[str]] = _get_actions_combo_by_action_prefix(actions)
    for action in actions:
        for esc_actions_combo in esc_actions_list:
            for esc_action in set(esc_actions_combo):
                if attribute_match(action, esc_action):
                    esc_actions_combo.remove(esc_action)
                    if len(esc_actions_combo) == 0:
                        return True
    return False


@functools.lru_cache(maxsize=None)
def attribute_match(src_attr: str, target_attr: str):
    src_attr = src_attr.replace("*", ".*").replace(" ", "")
    target_attr = target_attr.replace(" ", "")
    return re.search(src_attr, target_attr)


def _get_actions_combo_by_action_prefix(actions: Set[str]) -> List[Set[str]]:
    esc_actions_map: Dict[str, List[Set[str]]] = {}
    for action in actions:
        action_prefix: str = parse_service_name(action)
        if action_prefix not in esc_actions_map:
            esc_actions_map[action_prefix] = get_esc_action_set_list(action_prefix)
    return [esc_actions_set for esc_actions_set_list in esc_actions_map.values() for esc_actions_set in esc_actions_set_list]


@functools.lru_cache(maxsize=None)
def parse_service_name(action: str) -> str:
    return action.split(":")[0]


def get_esc_action_set_list(action_prefix: str) -> List[Set[str]]:
    action_set_list: List[Set] = []

    if action_prefix == "iam":
        for key, actions_set_list in SERVICE_TO_ESC_ACTIONS_COMBO_SETS.items():
            if key.__contains__(action_prefix):
                for actions_set in actions_set_list:
                    action_set_list.append(set(actions_set))
    else:
        for actions_set in SERVICE_TO_ESC_ACTIONS_COMBO_SETS.get(action_prefix, []) + \
                           SERVICE_TO_ESC_ACTIONS_COMBO_SETS.get("iam" + action_prefix, []):
            action_set_list.append(set(actions_set))
    return action_set_list


LAMBDA_UPDATE_ACTION: str = "lambda:updatefunctioncode"
LAMBDA_INVOKE_FUNCTION_ACTION: str = "lambda:invokefunction"
LAMBDA_CREATE_EVENT_ACTION: str = "lambda:createeventsourcemapping"
LAMBDA_CREATE_FUNCTION_ACTION: str = "lambda:createfunction"
EC2_RUN_INSTANCE_ACTION: str = "ec2:runinstances"
IAM_CREATE_KEY_ACTION: str = "iam:CreateAccessKey"
IAM_CREATE_PROFILE_ACTION: str = "iam:CreateLoginProfile"
IAM_UPDATE_PROFILE_ACTION: str = "iam:UpdateLoginProfile"
IAM_PASS_ROLE_ACTION: str = "iam: passrole"
IAM_ALL_ACTIONS: str = "iam:*"
IAM_CREATE_POLICY_VERSION_ACTION: str = "iam: CreatePolicyVersion"
IAM_SET_DEFAULT_POLICY_VERSION_ACTION: str = "iam: SetDefaultPolicyVersion"
IAM_PUT_USER_POLICY_ACTION: str = "iam: PutUserPolicy"
IAM_PUT_GROUP_POLICY_ACTION: str = "iam: PutGroupPolicy"
IAM_PUT_ROLE_POLICY_ACTION: str = "iam: PutRolePolicy"
IAM_ATTACH_USER_POLICY_ACTION: str = "iam: AttachUserPolicy"
IAM_ATTACH_GROUP_POLICY_ACTION: str = "iam: AttachGroupPolicy"
IAM_ATTACH_ROLE_POLICY_ACTION: str = "iam: AttachRolePolicy"
IAM_ADD_USER_GROUP_ACTION: str = "iam: AddUserToGroup"
GLUE_UPDATE_EVENT_ACTION: str = "glue: updatedevendpoint"
GLUE_CREATE_EVENT_ACTION: str = "glue: createdevendpoint"
CLOUD_FORMATION_CREATE_ACTION: str = "cloudformation:createstack"
DATA_PIPELINE_CREATE_ACTION: str = "datapipeline:createpipeline"

ACTIONS_EXCLUDE_LIST: List[str] = [IAM_CREATE_KEY_ACTION, IAM_CREATE_PROFILE_ACTION, IAM_UPDATE_PROFILE_ACTION, LAMBDA_UPDATE_ACTION]
SERVICE_TO_ESC_ACTIONS_COMBO_SETS: Dict[str, List[Set[str]]] = \
    {
        "iam": [
            {IAM_ALL_ACTIONS}, {IAM_CREATE_POLICY_VERSION_ACTION}, {IAM_SET_DEFAULT_POLICY_VERSION_ACTION}, {IAM_PUT_USER_POLICY_ACTION},
            {IAM_PUT_GROUP_POLICY_ACTION},
            {IAM_PUT_ROLE_POLICY_ACTION}, {IAM_ATTACH_USER_POLICY_ACTION}, {IAM_ATTACH_GROUP_POLICY_ACTION}, {IAM_ATTACH_ROLE_POLICY_ACTION},
            {IAM_ADD_USER_GROUP_ACTION}, {IAM_CREATE_KEY_ACTION}, {IAM_CREATE_PROFILE_ACTION}
        ],
        "glue": [{GLUE_UPDATE_EVENT_ACTION}],
        "lambda": [{LAMBDA_UPDATE_ACTION}],
        "iamec2": [{IAM_PASS_ROLE_ACTION, EC2_RUN_INSTANCE_ACTION}],
        "iamlambda": [{IAM_PASS_ROLE_ACTION, LAMBDA_CREATE_FUNCTION_ACTION, LAMBDA_INVOKE_FUNCTION_ACTION},
                      {IAM_PASS_ROLE_ACTION, LAMBDA_CREATE_FUNCTION_ACTION, LAMBDA_CREATE_EVENT_ACTION}
                      ],
        "iamglue": [{IAM_PASS_ROLE_ACTION, GLUE_CREATE_EVENT_ACTION}],
        "iamcloudformation": [{IAM_PASS_ROLE_ACTION, CLOUD_FORMATION_CREATE_ACTION}],
        "iamdatapipeline": [{IAM_PASS_ROLE_ACTION, DATA_PIPELINE_CREATE_ACTION}],
        "*": [{"*"}]
    }

SERVICE_TO_ESC_ACTIONS_LIST: Dict[str, List[str]] = \
    {
        "iam": [
            IAM_ALL_ACTIONS, IAM_CREATE_POLICY_VERSION_ACTION, IAM_SET_DEFAULT_POLICY_VERSION_ACTION, IAM_PUT_USER_POLICY_ACTION,
            IAM_PUT_GROUP_POLICY_ACTION,
            IAM_PUT_ROLE_POLICY_ACTION, IAM_ATTACH_USER_POLICY_ACTION, IAM_ATTACH_GROUP_POLICY_ACTION, IAM_ATTACH_ROLE_POLICY_ACTION,
            IAM_ADD_USER_GROUP_ACTION, IAM_CREATE_KEY_ACTION, IAM_CREATE_PROFILE_ACTION, IAM_PASS_ROLE_ACTION
        ],
        "glue": [GLUE_UPDATE_EVENT_ACTION, GLUE_CREATE_EVENT_ACTION],
        "lambda": [
            LAMBDA_UPDATE_ACTION, LAMBDA_CREATE_FUNCTION_ACTION, LAMBDA_INVOKE_FUNCTION_ACTION, LAMBDA_CREATE_EVENT_ACTION
        ],
        "ec2": [EC2_RUN_INSTANCE_ACTION],
        "cloudformation": [CLOUD_FORMATION_CREATE_ACTION],
        "datapipeline": [DATA_PIPELINE_CREATE_ACTION],
        "*": ["*"]
    }
