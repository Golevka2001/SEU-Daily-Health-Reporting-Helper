class Info:
    #################### 必填 ####################
    # 学号（将 220000000 替换为您的一卡通号）
    user_id = ["220000000", "220000001"
               ]  # 如需要添加打卡账号，请按照此格式向下添加；如只有一个一个用户，请删除列表中多余项但不要删除中括号[]，下同。

    # 登录网上办事大厅的密码（将 ****** 替换为登录信息门户的密码）
    password = ["******", "******"]

    # chromedriver 可执行文件路径
    chrome_driver_path = "/usr/bin/chromedriver"

    #################### 可选 ####################
    # 是否需要发送邮件通知打卡结果（yes/no）
    notification = ["no", "no"]

    # 只有尝试打卡失败后，才发送邮件（yes/no）
    notify_failure_only = ["no", "no"]

    # 发送打卡状态的邮箱地址。对于东南大学邮箱，为 "USER_NAME@seu.edu.cn"（将 USER_NAME 替换为您的域名）
    from_addr = "USER_NAME@seu.edu.cn"

    # 发送打卡状态的邮箱密码（将 ****** 替换为您邮箱的密码）
    email_password = "******"

    # 发送打卡状态的邮箱的 smtp 服务器地址。对于东南大学邮箱，为 "smtp.seu.edu.cn"
    smtp_server = "smtp.seu.edu.cn"

    # 发送打卡状态的邮箱的 smtp 服务器端口号。对于东南大学邮箱，为25，其他邮箱请自行查询后填写，建议使用SSL协议的端口号
    port = 25

    # 接收打卡状态的邮箱地址
    to_addr = ["name1@example.com", "name@example.com"]
