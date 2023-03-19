aws wafv2 create-ip-set \
    --name my-ip-set \
    --scope REGIONAL \
    --addresses '192.0.2.0/24' '198.51.100.0/24' \
    --tags Key=my-tag,Value=my-value

aws wafv2 create-web-acl \
    --name my-web-acl \
    --default-action Type=BLOCK \
    --rules Name=my-rule,Priority=1,Action=ALLOW,Statement=OverrideAction=NONE,IPSetReferenceStatement=Arn=arn:aws:wafv2:us-east-1:123456789012:/ipset/my-ip-set \
    --scope REGIONAL \
    --visibility-config SampledRequestsEnabled=True,CloudWatchMetricsEnabled=True \
    --tags Key=my-tag,Value=my-value

aws cloudfront create-distribution \
    --distribution-config '{"CallerReference": "my-caller-reference","Aliases":{"Quantity":0},"DefaultRootObject":"index.html","Origins":{"Quantity":1,"Items":[{"Id":"my-origin","DomainName":"my-bucket.s3.amazonaws.com","S3OriginConfig":{"OriginAccessIdentity":""}}]},"DefaultCacheBehavior":{"TargetOriginId":"my-origin","ForwardedValues":{"QueryString":false,"Cookies":{"Forward":"none"},"Headers":{"Quantity":0},"QueryStringCacheKeys":{"Quantity":0}},"TrustedSigners":{"Enabled":false,"Quantity":0},"Viewer
