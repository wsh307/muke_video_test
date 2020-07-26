# coding:utf-8

def check_and_get_video_type(type_obj, type_video, message):
    # 视频类型判断函数
    try:
        type_obj(type_video)
    except:
        return {'code':-1,'msg':message}

    return {'code':0, 'msg':'success'}
