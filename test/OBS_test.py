from obs import ObsClient
from obs import PutObjectHeader
from SmartGlovesProject_Server.Data_Prepare.credential import obs_Access_Key_Id, obs_Secret_Access_Key, obs_endpoint, \
    obs_location

if __name__ == '__main__':
    obsClient = ObsClient(access_key_id=obs_Access_Key_Id,
                          secret_access_key=obs_Secret_Access_Key,
                          server=obs_endpoint)

    # # 创建桶
    # resp = obsClient.createBucket(bucketName="spec-data", location="cn-east-3")
    # if resp.status < 300:
    #     print('requestId:', resp.requestId)
    # else:
    #     print('errorCode:', resp.errorCode)
    #     print('errorMessage:', resp.errorMessage)

    # 获取桶列表
    # try:
    #     resp = obsClient.listBuckets(True)
    #     if resp.status < 300:
    #         print('requestId:', resp.requestId)
    #         print('name:', resp.body.owner.owner_id)
    #         print('create_date:', resp.body.owner.owner_name)
    #         index = 1
    #         for bucket in resp.body.buckets:
    #             print('bucket [' + str(index) + ']')
    #             print('name:', bucket.name)
    #             print('create_date:', bucket.create_date)
    #             print('location:', bucket.location)
    #             index += 1
    #     else:
    #         print('errorCode:', resp.errorCode)
    #         print('errorMessage:', resp.errorMessage)
    # except:
    #     import traceback
    #
    #     print(traceback.format_exc())

    # 列举桶内对象
    try:
        resp = obsClient.listObjects('wav-data', max_keys=100)

        if resp.status < 300:
            print('requestId:', resp.requestId)
            print('name:', resp.body.name)
            print('prefix:', resp.body.prefix)
            print('max_keys:', resp.body.max_keys)
            print('is_truncated:', resp.body.is_truncated)
            index = 1
            for content in resp.body.contents:
                print('object [' + str(index) + ']')
                print('key:', content.key)
                print('lastModified:', content.lastModified)
                print('etag:', content.etag)
                print('size:', content.size)
                print('storageClass:', content.storageClass)
                print('owner_id:', content.owner.owner_id)
                print('owner_name:', content.owner.owner_name)
                index += 1
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        import traceback

        print(traceback.format_exc())


    # # 获取桶配额，0表示无上限
    # try:
    #     resp = obsClient.getBucketQuota('wav-data')
    #
    #     if resp.status < 300:
    #         print('requestId:', resp.requestId)
    #         print('quota:', resp.body.quota)
    #     else:
    #         print('errorCode:', resp.errorCode)
    #         print('errorMessage:', resp.errorMessage)
    # except:
    #     import traceback
    #
    #     print(traceback.format_exc())

    # # 上传文件
    # try:
    #     from obs import PutObjectHeader
    #
    #     headers = PutObjectHeader()
    #     headers.contentType = 'text/plain'
    #
    #     resp = obsClient.putFile('wav-data',
    #                              objectKey='Happy/TRRRULH128F92CDB2E.mp3',
    #                              file_path='resources/mp3/Angry/TRRRULH128F92CDB2E.mp3',
    #                              metadata={'mood': 'Happy'},
    #                              headers=headers)
    #
    #     if resp.status < 300:
    #         print('requestId:', resp.requestId)
    #         print('etag:', resp.body.etag)
    #         print('versionId:', resp.body.versionId)
    #         print('storageClass:', resp.body.storageClass)
    #     else:
    #         print('errorCode:', resp.errorCode)
    #         print('errorMessage:', resp.errorMessage)
    # except:
    #     import traceback
    #
    #     print(traceback.format_exc())

    # 下载文件
    # try:
    #     resp = obsClient.getObject('wav-data',
    #                                objectKey='Happy/TRRRULH128F92CDB2E.mp3',
    #                                downloadPath='resources/mp3/TRRRULH128F92CDB2E.mp3', )
    #
    #     if resp.status < 300:
    #         print('requestId:', resp.requestId)
    #         print('url:', resp.body.url)
    #     else:
    #         print('errorCode:', resp.errorCode)
    #         print('errorMessage:', resp.errorMessage)
    # except:
    #     import traceback
    #
    #     print(traceback.format_exc())
