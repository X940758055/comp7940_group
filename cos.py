import configparser
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
class tencent_cos():
    __bucket = ""
    def __init__(self, Region, bucket, secret_id, secret_key, token=None, scheme='https'):
        config = CosConfig(Region=Region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        client = CosS3Client(config)
        self.__client = client
        self.__bucket = bucket

    def uploadFile(self, path, name):
        response = self.__client.upload_file(
            Bucket=self.__bucket,
            LocalFilePath=path,  # 本地文件的路径
            Key=name,  # 上传到桶之后的文件名
        )
        return response['ETag']

    def downloadFile(self, name):
        return self.__client.get_object_url(Bucket=self.__bucket, Key=name)




config = configparser.ConfigParser()
config.read('config.ini')
Region = (config['COS']['REGION'])
bucket = (config['COS']['BUCKET'])
secret_id = (config['COS']['SECRETID'])
secret_key = (config['COS']['SECRETKEY'])
cos = tencent_cos(Region, bucket, secret_id, secret_key)
res = cos.uploadFile("./image/first.png", "first.png")
res = cos.downloadFile("first.png")


