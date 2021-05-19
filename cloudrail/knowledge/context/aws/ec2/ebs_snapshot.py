from typing import List
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class EBSSnapshot(AwsResource):

    def __init__(self,
                 snap_id: str,
                 is_encrypted: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.NONE)
        self.snap_id: str = snap_id
        self.is_encrypted: bool = is_encrypted

    def get_keys(self) -> List[str]:
        return [self.volume_id]

    def get_id(self) -> str:
        return self.volume_id

    def get_name(self) -> str:
        return self.volume_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EBS Snapshot'
        else:
            return 'EBS Snapshots'

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#Snapshots:sort=snapshotId'.format(self.AWS_CONSOLE_URL, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
