import time

form_data = {
    'field13103': '[time]',
    'requestname': '学生出校申请与审批流程-[name]-[date]',
    'uploadType': '0',
    'workflowRequestLogId': '-1',
    'field11237': '[xmid]',
    'field11238': '[username]',
    'field11239': '[class]',
    'field11240': '[department]',
    'field11404': '0',
    'field11783': '40416',
    'field12523': '1',
    'field11663': '6',
    'field11683': '吃饭',
    'field11250': '[out-date]',
    'field11251': '[out-time]',
    'field11241': '宝龙城市广场',
    'field11304': '步行或骑行',
    'field13063': '[in-date]',
    'field11255': '[in-time]',
    'mainId': '21',
    'subId': '182',
    'secId': '841',
    'field11259': '0',
    'field11260': '1',
    'field11261': '本人承诺上述信息均属实，如有不实，愿承担由此引起的一切后果及法律责任。',
    'field11262': '1',
    'field11263': '本人承诺在外出期间做好个人防护工作，如有不适，将及时向辅导员报告。',
    'field11297': '8213',
    'workflowid': '2382',
    'workflowtype': '81',
    'nodeid': '9047',
    'nodetype': '0',
    'src': 'submit',
    'iscreate': '1',
    'formid': '-143',
    'isbill': '1',
    'needcheck': 'field13063,field12523,field13057,field11404,field11663,field11304,field11241,field11250,field11251,field11255,field11259,field11260,field11262,field11683',
    'requestid': '-1',
    'rand': '[token]',
    'htmlfieldids': 'field11683;具体事由;1,field11241;出校去向;1',
    'needwfback': '1',
    'f_weaver_belongto_userid': 'null',
    'f_weaver_belongto_usertype': 'null',
    '41315_2382_addrequest_submit_token': '[token]',
    'lastloginuserid': '[xmid]',
    'freeNode': '0',
    'freeDuty': '1'
}

keys = {
    # common
    'xmid': 'field11237',  # xmid
    'xh': "field11238",  # 学号
    'xb': "field12165",  # 性别
    'xby': "field11240",  # 学部 (院)
    'bj': "field11239",  # 班级
    'zy': "field12166",  # 专业

    # non-common
    'out-date': 'field11250',  # 出校日期
    'in-date': 'field13063',  # 出校时间段
    'out-time': 'field11251',  # 返校日期
    'in-time': 'field11255'  # 返校时间段
}


def gen_data(info: dict, xmid: str, now_float: float) -> dict:
    new_data = form_data.copy()

    now = time.localtime(now_float)
    now_time = str(now.tm_hour).zfill(2) + ':' + str(now.tm_min).zfill(2)
    now_date = str(now.tm_year).zfill(4) + '-' + str(now.tm_mon).zfill(2) + \
        '-' + str(now.tm_mday).zfill(2)
    token = str(int(time.time() * 1000))

    new_data['requestname'] = \
        new_data['requestname'].replace('[name]', info['xm'])  # 流程标题
    new_data['requestname'] = \
        new_data['requestname'].replace('[date]', now_date)  # 流程标题
    new_data[keys['xmid']] = xmid  # xmid
    new_data['lastloginuserid'] = xmid  # xmid
    new_data['field13103'] = now_time  # 当前时间
    new_data['rand'] = token  # 口令
    new_data['41315_2382_addrequest_submit_token'] = token  # 口令
    new_data[keys['xh']] = info['xh']  # 学号
    new_data[keys['bj']] = info['bj']  # 班级
    new_data[keys['xby']] = info['xby']  # 学部 (院)

    now_number = '5'
    if now.tm_hour < 12:
        now_number = '4'
    new_data[keys['out-date']] = now_date  # 出校日期
    new_data[keys['out-time']] = now_number  # 出校时间段
    new_data[keys['in-date']] = now_date  # 返校日期
    new_data[keys['in-time']] = now_number  # 返校时间段

    return new_data
