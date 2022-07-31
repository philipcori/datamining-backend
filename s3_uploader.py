import boto3
from botocore.exceptions import ClientError


class S3Uploader():
    def __init__(self):
        self.bucket = "matrix-imgs-pcori"
        self.s3_client = boto3.client('s3')

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        print('uploading file to s3...')

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        try:
            response = self.s3_client.upload_file(file_name, self.bucket, object_name)
        except ClientError as e:
            print("Error uploading file: %s" % e)
            raise e
        print('file uploaded!')

    # get presigned url for file
    def get_presigned_url(self, object_name):
        print('getting presigned url...')
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket,
                                                                'Key': object_name},
                                                        ExpiresIn=3600)
        except ClientError as e:
            print("Error getting presigned url: %s" % e)
            raise e

        print('presigned url: ' + response)
        return response