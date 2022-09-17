"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3
import pulumi_eks as eks
import pulumi_random as random


# Create an EKS(k8) cluster.
cluster = eks.Cluster("ml-cluster",
    create_oidc_provider= True,
)

# create postgresql Database for model metadata in Mlflow
mlflow_db_password = random.RandomPassword("mlflow_db_password",
    length=16,
    special= False
)

mlflow_db = aws.rds.Instance("mlflow",
    allocated_storage=10,
    engine="postgres",
    engine_version="13",
    instance_class="db.t3.micro",
    name="mlflow",
    password="mlflow_db_password",
    skip_final_snapshot=True,
    username="postgres",
    
    # Make sure that our EKS(K8) cluster is able to access the RDS(Mlflow_DB) instance.
    vpc_security_group_ids= [cluster.cluster_security_group, cluster.node_security_group],
)

# Export the cluster's kubeconfig.
pulumi.export('kubeconfig', cluster.kubeconfig)

# # Create an AWS resource (S3 Bucket)
# bucket = s3.Bucket('my-bucket')

# # Export the name of the bucket
# pulumi.export('bucket_name', bucket.id) 