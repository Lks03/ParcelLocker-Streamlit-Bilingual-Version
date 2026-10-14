# 页面使用稳定的键，切换语言不会改变保存的数据
# Stable keys keep language changes separate from saved data
TEXT = {
    'app_title': ('快递柜管理系统', 'Parcel Locker System'),
    'nav': ('导航', 'Navigation'),
    'pages': ('页面', 'Pages'),
    'home': ('首页', 'Home'),
    'register': ('登记包裹', 'Register Parcel'),
    'collect': ('领取包裹', 'Collect Parcel'),
    'records': ('包裹记录', 'Parcel Records'),
    'lockers': ('柜子状态', 'Locker Status'),
    'back': ('返回首页', 'Back to Home'),
    'welcome': ('欢迎使用', 'Welcome'),
    'choose': ('请选择需要办理的业务。', 'Choose what you would like to do.'),
    'staff_group': ('快递员 / 工作人员', 'Courier / Staff'),
    'courier': ('快递员', 'Courier'),
    'customer': ('收件人', 'Customer'),
    'staff': ('工作人员', 'Staff'),
    'local': ('本地文件存储', 'Local file storage'),
    'footer': ('本地演示 · 模拟柜门操作', 'Local demo · Simulated locker operation'),
    'name': ('收件人姓名', 'Recipient name'),
    'name_hint': ('请输入收件人姓名', 'Enter recipient name'),
    'contact': ('收件人联系方式', 'Recipient contact'),
    'contact_hint': ('请输入手机号或邮箱', 'Enter phone number or email'),
    'tracking': ('快递单号', 'Tracking number'),
    'tracking_hint': ('请输入快递单号', 'Enter tracking number'),
    'registered': ('包裹登记成功。', 'Parcel registered successfully.'),
    'assigned': ('分配柜号：{number:02d}', 'Assigned locker: {number:02d}'),
    'code_result': ('取件码：{code}', 'Pickup code: {code}'),
    'notification': ('通知预览：您的包裹已入柜，请及时领取。', 'Notification preview: Your parcel is ready for collection.'),
    'preview_only': ('仅供预览，未发送消息。', 'Preview only. No message sent.'),
    'code_label': ('六位取件码', '6-digit pickup code'),
    'code_hint': ('请输入取件码', 'Enter pickup code'),
    'verify': ('验证取件码', 'Verify Code'),
    'verified': ('取件码验证成功', 'Code verified'),
    'location': ('您的包裹在 {number:02d} 号柜。', 'Your parcel is in Locker {number:02d}.'),
    'take': ('请取出包裹并关闭柜门。', 'Please take your parcel and close the locker.'),
    'confirm': ('确认领取', 'Confirm Collection'),
    'collected': ('包裹领取成功。', 'Parcel collected successfully.'),
    'released': ('柜子已恢复空闲。', 'The locker is available again.'),
    'simulation': ('柜门开启为模拟操作。', 'Locker opening is simulated.'),
    'records_desc': ('查看已登记和已领取的包裹', 'Registered and collected parcels'),
    'empty': ('暂无包裹，请前往“登记包裹”添加第一条记录。', 'No parcels registered yet. Use Register Parcel to add the first parcel.'),
    'id': ('编号', 'ID'),
    'recipient': ('收件人', 'Recipient'),
    'locker': ('柜号', 'Locker'),
    'status': ('状态', 'Status'),
    'records_summary': ('共 {total} 条记录 · {stored} 件待领取 · {collected} 件已领取', 'Records: {total} · Stored: {stored} · Collected: {collected}'),
    'lockers_summary': ('共 {total} 个柜子 | 空闲 {available} 个 | 占用 {occupied} 个', 'Total: {total} | Available: {available} | Occupied: {occupied}'),
    'locker_number': ('{number:02d} 号柜', 'Locker {number:02d}'),
    'Available': ('空闲', 'Available'),
    'Occupied': ('占用', 'Occupied'),
    'Stored': ('待领取', 'Stored'),
    'Collected': ('已领取', 'Collected'),
    'unknown_error': ('操作失败，请刷新页面后重试。', 'The operation failed. Refresh the page and try again.'),
}

# 保持业务层独立，将已知错误翻译为所选语言
# Keep the business layer independent and translate known errors
ERRORS = {
    'All fields are required.': '请填写所有必填项。',
    'This tracking number is already registered.': '该快递单号已经登记，请勿重复提交。',
    'No available locker. The parcel cannot be registered.': '暂无空闲柜子，无法登记包裹。',
    'Enter a 6-digit pickup code.': '请输入六位数字取件码。',
    'Invalid pickup code.': '取件码无效，请检查后重试。',
    'This parcel has already been collected.': '该包裹已经领取，请勿重复操作。',
    'The locker record does not match this parcel. Please contact staff.': '柜子记录与包裹不匹配，请联系工作人员。',
    'This locker is already occupied.': '该柜子已被占用。',
    'Cannot read data.json. Check the file or restore a backup; existing data has not been replaced.': '无法读取 data.json。请检查文件或恢复备份；原有数据未被替换。',
    'Could not save the operation. Check folder permissions and available disk space, then try again.': '保存失败，请检查文件夹权限和可用磁盘空间后重试。',
    'The saved records are invalid. Restore a valid data.json backup before continuing.': '保存的记录无效，请先恢复有效的 data.json 备份。',
}


def translate(key, language='zh', **values):
    return TEXT[key][1 if language == 'en' else 0].format(**values)


def translate_error(message, language='zh'):
    if message in ERRORS:
        return message if language == 'en' else ERRORS[message]
    return translate('unknown_error', language)
