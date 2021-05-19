# Cloudrail's Rules' Evidence Field

![Sample CAR Evidence](imgs/evidence_car_example.png)

Cloudrail’s context can be as rich as you want to design the CAR (context-aware rule). The challenge is determining how to showcase your logic! This is where the evidence field comes into play.

The above example highlights critical resources that explain the path-to-violation. Let’s call these “nodes”.  Between the nodes, all components of the context in relation between node <> node are listed. In the above case, the particular violation was network related, but you may have a mixture of IAM and network objects to reveal!

Note, all evidence fields must use this format. In order to get the evidence field to look like this, you will need to use the following syntax:

For “nodes”, use “~” before and after the text. Currently, the text formatted is very sensitive to special characters. Make sure all of the text is part of the “node”, and between the starting “~” and ending “~”. Additionally, Cloudrail will recognize text as a “node” object by ending with a period. In fact, will treat any dot notation as a delimiter as a new line. Make sure to include dot notation!

This example:

```
~text referring to the node should be included within here~. If you. put the string. like this. it will look like. ~this~.
```

Translates to the following:

```
text referring to the node should be included within here
   | if you
   | put the string
   | like this
   | it will look like
this
```

If you want to reference an actual object (e.g. name of the EC2 instance or subnet), the text should be highlighted as 
shown in the screenshot above. To do this, make sure the object reference is wrapped by single backticks like this:

```
`aws_instance.public_ins.id`
```

The text is delimited into a new line whenever you start a new sentence. 
This is how the above example (screenshot at the top) looks like pre-formatted:

```
issues.append(Issue(
    f'~Internet~. '
    f"Instance `{rds_instance.get_friendly_name()}` is "
    f"in {rds_cluster.get_type()} `{rds_cluster.get_friendly_name()}`. "
    f"{rds_instance.get_type()} is on {rds_instance.network_resource.vpc.get_type()}"
    f" `{rds_instance.network_resource.vpc.get_friendly_name()}`. "
    f"{rds_instance.get_type()} uses subnet(s) "
    f"`{', '.join([x.get_friendly_name() for x in rds_instance.network_resource.security_groups])}`. "
    f"{rds_instance.get_type()} is reachable from the internet due to subnet(s) and route table(s). "
    f"Subnet uses Network ACL's "
    f"`{', '.join([x.network_acl.get_friendly_name() for x in rds_instance.network_resource.subnets])}`. "
    f"Network ACL's and security group(s) allows the RDS configured ports. "
    f'~{rds_instance.get_type()}~',
    rds_cluster, security_group))
```