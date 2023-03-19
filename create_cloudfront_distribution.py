import boto3

# Create an AWS WAF client
waf_client = boto3.client('waf')

# Create an IP set
ip_set_response = waf_client.create_ip_set(
    Name='my-ip-set',
    ChangeToken=waf_client.get_change_token()['ChangeToken'],
    Addresses=[
        '192.0.2.0/24',
        '198.51.100.0/24'
    ]
)
ip_set_id = ip_set_response['IPSet']['IPSetId']

# Create a Web ACL
web_acl_response = waf_client.create_web_acl(
    Name='my-web-acl',
    ChangeToken=waf_client.get_change_token()['ChangeToken'],
    DefaultAction={
        'Type': 'BLOCK'
    },
    MetricName='my-metric',
    Rules=[
        {
            'Name': 'my-rule',
            'Priority': 1,
            'Action': {
                'Type': 'ALLOW'
            },
            'Statement': {
                'IPSetReferenceStatement': {
                    'Arn': f'arn:aws:waf::123456789012:ipset/{ip_set_id}',
                    'IPSetForwardedIPConfig': {
                        'HeaderName': 'X-Forwarded-For',
                        'FallbackBehavior': 'MATCH'
                    }
                }
            }
        }
    ]
)
web_acl_id = web_acl_response['WebACL']['WebACLId']

# Create a CloudFront distribution
cloudfront_client = boto3.client('cloudfront')
distribution_response = cloudfront_client.create_distribution(
    DistributionConfig={
        'CallerReference': 'my-caller-reference',
        'Aliases': {
            'Quantity': 0
        },
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'my-origin',
                    'DomainName': 'my-bucket.s3.amazonaws.com',
                    'S3OriginConfig': {
                        'OriginAccessIdentity': ''
                    }
                }
            ]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'my-origin',
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {
                    'Forward': 'none'
                },
                'Headers': {
                    'Quantity': 0
                },
                'QueryStringCacheKeys': {
                    'Quantity': 0
                }
            },
            'TrustedSigners': {
                'Enabled': False,
                'Quantity': 0
            },
            'ViewerProtocolPolicy': 'redirect-to-https',
            'MinTTL': 0
        },
        'CacheBehaviors': {
            'Quantity': 0
        },
        'CustomErrorResponses': {
            'Quantity': 0
        },
        'Comment': '',
        'Logging': {
            'Enabled': False,
            'IncludeCookies': False,
            'Bucket': '',
            'Prefix': ''
        },
        'PriceClass': 'PriceClass_All',
        'Enabled': True,
        'ViewerCertificate': {
            'CloudFrontDefaultCertificate': True
        },
        'WebACLId': web_acl_id,
        'HttpVersion': 'http2'
    }
)
distribution_id = distribution_response['Distribution']['Id']
