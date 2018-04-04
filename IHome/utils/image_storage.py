# -*- coding:utf-8 -*-
# 上传存储照片到七牛云


import qiniu

access_key = "yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW"
bucket_name = 'ihome'
# 拼接访问全路径 ： http://oyucyko3w.bkt.clouddn.com/FqhIJdJoTv5t4bE93eiFbCnEGW6v


def upload_image(image_data):
    """实现上传、存储图片到七牛云"""

    q = qiniu.Auth(access_key, secret_key)

    token = q.upload_token(bucket_name)
    ret, info = qiniu.put_data(token, None, image_data)

    print ret
    print info
    # 魔法数字写在前面
    if 200 == info.status_code:
        return ret.get('key')
    else:
        raise Exception('上传图片失败')

    # if ret is not None:
    #     print('All is OK')
    # else:
    #     print(info)  # error message in info


if __name__ == '__main__':
    path = '/Users/sheep-yang/Desktop/Images/mm02.jpg'
    with open(path, 'rb') as file:
        upload_image(file.read())
