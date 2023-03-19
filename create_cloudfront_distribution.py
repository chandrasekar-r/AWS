import sys
import boto3


config = {
    'profile': 'default',
    'region': 'us-east-1',
    'account_id': '123456789012',
    'ip_set_name': 'my-ip-set',
    'web_acl_name': 'my-web-acl',
    'distribution_name': 'my-distribution',
    'origin_domain_name': 'my-bucket.s3.amazonaws.com',
}


def create_ip_set(wafv2_client, ip_set_name):
    response = wafv2_client.create_ip_set(
        Name=ip_set_name,
        Scope='REGIONAL',
        Addresses=['192.0.2.0/24', '198.51.100.0/24'],
        Tags=[{'Key': 'my-tag', 'Value': 'my-value'}]
    )
    return response['IPSet']['ARN']


def create_web_acl(wafv2_client, web_acl_name, ip_set_arn):
    response = wafv2_client.create_web_acl(
        Name=web_acl_name,
        Scope='REGIONAL',
        DefaultAction={'Type': 'BLOCK'},
        VisibilityConfig={'SampledRequestsEnabled': True, 'CloudWatchMetricsEnabled': True},
        Rules=[
            {
                'Name': 'my-rule',
                'Priority': 1,
                'Action': {'Type': 'ALLOW'},
                'Statement': {
                    'OverrideAction': {'Type': 'NONE'},
                    'IPSetReferenceStatement': {'ARN': ip_set_arn}
                }
            }
        ],
        Tags=[{'Key': 'my-tag', 'Value': 'my-value'}]
    )
    return response['WebACL']['ARN']


def create_cloudfront_distribution(cloudfront_client, web_acl_arn, origin_domain_name, distribution_name):
    response = cloudfront_client.create_distribution(
        DistributionConfig={
            'CallerReference': 'my-caller-reference',
            'Aliases': {'Quantity': 0},
            'DefaultRootObject': 'index.html',
            'Origins': {
                'Quantity': 1,
                'Items': [
                    {
                        'Id': 'my-origin',
                        'DomainName': origin_domain_name,
                        'S3OriginConfig': {'OriginAccessIdentity': ''}
                    }
                ]
            },
            'DefaultCacheBehavior': {
                'TargetOriginId': 'my-origin',
                'ForwardedValues': {
                    'QueryString': False,
                    'Cookies': {'Forward': 'none'},
                    'Headers': {'Quantity': 0},
                    'QueryStringCacheKeys': {'Quantity': 0}
                },
                'TrustedSigners': {'Enabled': False, 'Quantity': 0},
                'ViewerProtocolPolicy': 'redirect-to-https',
                'MinTTL': 0
            },
            'Enabled': True,
            'ViewerCertificate': {'CloudFrontDefaultCertificate': True},
            'WebACLId': web_acl_arn
        }
    )
    return response['Distribution']

if __name__ == '__main__':
    session = boto3.Session(profile_name=config['profile'])
    wafv2_client = session.client('wafv2', region_name=config['region'])
    cloudfront_client = session.client('cloudfront')

    try:
        ip_set_arn = create_ip_set(wafv2_client, config['ip_set_name'])
        print(f"IP set created with ARN: {ip_set_arn}")
    except Exception as e:
        print(f"Error creating IP set: {e}")
        sys.exit(1)

    try:
        web_acl_arn = create_web_acl(wafv2_client, config['web_acl_name'], ip_set_arn)
        print(f"Web ACL created with ARN: {web_acl_arn}")
    except Exception as e:
        print(f"Error creating Web ACL: {e}")
        sys.exit(1)

    try:
        distribution = create_cloudfront_distribution(
            cloudfront_client, web_acl_arn, config['origin_domain_name'], config['distribution_name'])
        print(f"CloudFront distribution created with ID: {distribution['Id']}")
    except Exception as e:
        print(f"Error creating CloudFront distribution: {e}")
        sys.exit(1)

# Again, make sure to replace the values in the config dictionary with the appropriate values for your own use case before running the code.
