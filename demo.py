# =============================================
# 实现功能：使用Selenium实现
#           控件获取与元素基本操作,
#           浏览器前进、后退、刷新控制,
#           获取窗口信息（标题、URL、页面源代码等）
#           浏览器窗口大小&位置调整,打印检查,
#           浏览器窗口与 frame 切换,
#           获取、处理加工静态文本和属性数据,
#           按钮，单选框的状态读取（是否选中、是否可用）,
#           模拟鼠标点击、双击等操作,
#           模拟键盘输入、复制、粘贴、选中、删除、特殊按键操作,
#           使用动作链进行键盘组合操作，
#           处理消息框（确认、取消、输入、获取文本）,
#           下拉表操作（获取选项、根据各条件选中、取消、获取选项文本等）,
#           文件上传下载（启动配置）,
#           页面和元素截图（含使用pillow），验证码图像获取
# 实验时间：2025年5月14日
# 作    者：⬛⬛⬛ 
# 学    号：⬛⬛⬛⬛⬛⬛⬛⬛⬛  
# 班    级：⬛⬛⬛⬛⬛⬛  
# 版    本：v1.0
# 测试环境：
#     - 操作系统：Windows 11
#     - Python版本：3.12
#     - Selenium版本：4.8.3
#     - 浏览器：Firefox 138.0
#     - geckodriver版本：0.36.0
#     - 开发工具：PyCharm 2024.1.1
#     - 本地服务器：WampServer 2.2e
#     - PHP版本：5.3.13
#     - Apache版本：2.2.22
#     - MySQL版本：5.5.24
#     - 测试站点：ECShop Release 2.7.1 本地商城页面
#     - 依赖库：
#         - selenium 4.8.3
#         - pillow 11.2.1
#         - ddddocr 15.6
# =============================================

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from time import sleep
import ddddocr
from PIL import ImageGrab

# Firefox启动配置，实例化一个配置对象
set_config = webdriver.FirefoxOptions()
# 通过配置对象添加配置信息，设置默认下载文件夹为自定义
set_config.set_preference('browser.download.folderList', 2)
# 设置下载文件存放目录
set_config.set_preference('browser.download.dir', 'D:\\IMI\\Download')
# 设置不显示开始
set_config.set_preference('browser.download.manager.showWhenStarting', False)
# 设置对.csv文件类型不再弹出框进行询问
set_config.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/csv,application/octet-stream')
# 禁止内置的 PDF 预览器
set_config.set_preference('pdfjs.disabled', True)
# 以配置对象启动浏览器
driver = webdriver.Firefox(options=set_config)
# 创建 ActionChains 对象
actions = ActionChains(driver)
# 打开后台页
driver.get('http://localhost:8082/upload/admin/index.php')
# 输入用户名：admin
driver.find_element(By.NAME, 'username').send_keys('admin')
# 输入密码：admin123
driver.find_element(By.NAME, 'password').send_keys('admin123')
# 定位验证码输入框
code_input = driver.find_element(By.CLASS_NAME, 'capital')
# 等待验证码图片加载出来:1秒
sleep(1)
# 定位识别验证码元素（包含）
code_img = driver.find_element(By.XPATH, '//img[contains(@src, "index.php?act=captcha")]')
# 将图片元素截图保存,D:\IMI\ScreenShot\check.png
code_img.screenshot(r'D:\IMI\ScreenShot\check.png')
# 读取图片
img_bytes = open(r'D:\IMI\ScreenShot\check.png', 'rb').read()
# 创建ocr对象
ocr = ddddocr.DdddOcr()
# 识别验证码
check_code = ocr.classification(img_bytes)
# 输入验证码
code_input.send_keys(check_code)
# 将输入结果截图保存,D:\IMI\ScreenShot\check_code_input.png
driver.save_screenshot(r'D:\IMI\ScreenShot\check_code_input.png')
# 测试中，识别有概率错误，因此输入万能验证码
code_input.clear()
code_input.send_keys('0')
# 获取“请保存我这次的登录信息。”按钮控件
record_checkbox = driver.find_element(By.ID, 'remember')
# 执行双击操作
actions.double_click(record_checkbox).perform()
print('执行双击操作')
# 检查单选框是否选中，若否，则点击“进入管理中心“
if not record_checkbox.is_selected():
    driver.find_element(By.CLASS_NAME, 'button').click()
# 进行截屏,D:\IMI\ScreenShot\center_shot.png
driver.save_screenshot(r'D:\IMI\ScreenShot\center_shot.png')
# 等待1秒
sleep(1)
# 切换frame:menu-frame
driver.switch_to.frame('menu-frame')
# 对左侧菜单栏元素进行截图,D:\IMI\Download\menu_shot.csv
driver.find_element(By.CSS_SELECTOR, 'body').screenshot(r'D:\IMI\ScreenShot\menu_shot.png')
# 点击“商品批量上传”
driver.find_element(By.LINK_TEXT, '商品批量上传').click()
# 切换到默认主页
driver.switch_to.default_content()
# 切换frame:main-frame
driver.switch_to.frame('main-frame')
# 对右侧区域进行截屏:D:\IMI\Download\upload_shot.png
driver.find_element(By.CLASS_NAME, "main-div").screenshot(r'D:\IMI\ScreenShot\upload_shot.png')
# 定位”数据格式“下拉表，并封装Select对象
data_cat = Select(driver.find_element(By.ID, 'data_cat'))
# 数据格式选择value为“ecshop”的选项
data_cat.select_by_value('ecshop')
# 定位”所属分类“下拉表，并封装Select对象
cat = Select(driver.find_element(By.ID, 'cat'))
# 所属分类选择“    小灵通/固话充值卡”
cat.select_by_visible_text('    小灵通/固话充值卡')
# 定位”文件编码“下拉表，并封装Select对象
charset = Select(driver.find_element(By.ID, 'charset'))
# 文件编码选择第二个选项:“简体中文”
charset.select_by_index(1)
# 获取“浏览”按钮控件并上传文件：D:\IMI\Download\test.csv
driver.find_element(By.NAME, 'file').send_keys(r'D:\IMI\Download\test.csv')
# 点击“确定”按钮
driver.find_element(By.ID, 'submit').click()
# 等待页面刷新
sleep(1)
# 再次点击"确定"按钮
driver.find_element(By.NAME, 'submit').click()
# 切换到默认主页
driver.switch_to.default_content()
# 切换frame:menu-frame
driver.switch_to.frame('menu-frame')
# 点击“商品批量上传”
driver.find_element(By.LINK_TEXT, '商品批量上传').click()
# 切换到默认主页
driver.switch_to.default_content()
# 切换frame:main-frame
driver.switch_to.frame('main-frame')
# 点击下载批量CSV文件（简体中文）
driver.find_element(By.LINK_TEXT, '下载批量CSV文件（简体中文）').click()
# 切换回默认主网页
driver.switch_to.default_content()
# 切换frame
driver.switch_to.frame('header-frame')
# 点击“设置导航栏”
driver.find_element(By.LINK_TEXT, '设置导航栏').click()
# 切换回默认主网页
driver.switch_to.default_content()
# 切换frame:main-frame
driver.switch_to.frame('main-frame')
# 左侧下拉表的状态是一直继承的（要保证第二次测试时左侧要有内容）
# 获取“设置个人导航”的右侧下拉表的Select对象
list_select = Select(driver.find_element(By.NAME, 'all_menu_list'))
# 选择右侧下拉表从第4个到第10个选项
for i in range(3, 10):
    list_select.select_by_index(i)
# 选择value是“ad_position.php?act=list”的选项
list_select.select_by_value('ad_position.php?act=list')
# 打印已选中的选项的文本内容
options = list_select.all_selected_options
for option in options:
    print(f'已选中的选项的文本内容:{option.text}')
# 取消第8个选项
list_select.deselect_by_index(7)
# 取消文本是“    商品类型“的选项
list_select.deselect_by_visible_text('    商品类型')
# 取消value是“goods.php?act=trash”的选项
list_select.deselect_by_value('goods.php?act=trash')
# 取消右侧下拉列表所有选项
list_select.deselect_all()
# 选择右侧文本是”    商品列表“的选项
list_select.select_by_visible_text('    商品列表')
all_options = list_select.options
# 选择倒数三个（-3 到末尾）
for option in all_options[-3:]:
    list_select.select_by_visible_text(option.text)
# 如果“增加“按钮为可用，则点击它
add_btn = driver.find_element(By.ID, 'btnAdd')
if add_btn.is_enabled():
    add_btn.click()
# 获取“设置个人导航“左侧下拉列表的Select对象
menu_select = Select(driver.find_element(By.NAME, 'menus_navlist'))
# 获取“设置个人导航“左侧下拉列表的所有选项
left_options = menu_select.options
# 选中“设置个人导航“左侧下拉列表的第一个选项
menu_select.select_by_index(0)
# 获取第一个选项的本文
fist_text = left_options[0].text
# 如果“下移“按钮为可用，则点击它
down_btn = driver.find_element(By.ID, 'btnMoveDown')
if down_btn.is_enabled():
    down_btn.click()
# 先取消第一个选择
menu_select.deselect_by_visible_text(fist_text)
# 获取“设置个人导航“左侧下拉列表的所有选项的长度
options_len = len(left_options)
# 选中“设置个人导航“左侧下拉列表的最后一个选项
menu_select.select_by_index(options_len - 1)
# 如果“上移“按钮为可用，则点击它
up_btn = driver.find_element(By.ID, 'btnMoveUp')
if up_btn.is_enabled():
    up_btn.click()
# 更新“设置个人导航“左侧下拉列表的所有选项
left_options = menu_select.options
# 选择”设置个人导航“左侧下拉列表的所有选项
for option in left_options:
    menu_select.select_by_visible_text(option.text)
# 打印“设置个人导航“左侧下拉列表被选中选项中的第一个的文本内容
print(f"左侧下拉列表被选中选项中的第一个的文本内容:{menu_select.first_selected_option.text}")
# 如果“移除“按钮为可用，则点击它
remove_btn = driver.find_element(By.ID, 'btnRemove')
if remove_btn.is_enabled():
    remove_btn.click()
# 将操作结果进行截图:D:\IMI\ScreenShot\select_shot.png
driver.find_element(By.XPATH, "//table[@style='width:300px']").screenshot(r'D:\IMI\ScreenShot\select_shot.png')
# 等待1秒
sleep(1)
# 点击”确定“按钮
driver.find_element(By.XPATH, "//input[@type='submit']").click()
# 等待1秒
sleep(1)
# 页面自动刷新后，切换默认主页
driver.switch_to.default_content()
# 切换frame:header-frame
driver.switch_to.frame('header-frame')
# 点击“查看网店”，打开新页面
driver.find_element(By.LINK_TEXT, '查看网店').click()
# 获取窗口句柄
handles = driver.window_handles
# 访问网址：http://www.sahitest.com/demo/promptTest.htm
driver.get('http://www.sahitest.com/demo/promptTest.htm')
# 点击Click For Prompt按钮
prompt = driver.find_element(By.NAME, 'b1')
prompt.click()
# 等待1秒
sleep(1)
# 切换到消息框
input_alert = driver.switch_to.alert
# 点击”取消“
input_alert.dismiss()
# 点击Click For Prompt按钮
prompt.click()
# 切换到消息框
input_alert = driver.switch_to.alert
# 打印消息框的文本信息
print(f'消息框的文本信息:{input_alert.text}')
# 输入“hello”
input_alert.send_keys('hello')
# 点击“确定”
input_alert.accept()
# 获取文本框控件
input_text = driver.find_element(By.NAME, 't1')
# 打印文本框当前内容
print(f'文本框当前内容:{input_text.get_attribute('value')}')
# 关闭当前页面
driver.close()
# 切换最新的窗口：登录页面
driver.switch_to.window(handles[-1])
# 打印当前网页的标题
print(f'当前网页的标:{driver.title}')
# 点击”登录“
driver.find_element(By.XPATH, "//a[@href='user.php']").click()
# 打印网页源代码
print(f'网页源代码:\n{driver.page_source}')
# 浏览器窗口最小化
driver.minimize_window()
# 设置浏览器在屏幕的位置（）
driver.set_window_position(1000, 2000)
# 打印浏览器在屏幕上的位置
print(f'浏览器在屏幕上的位置:\n{driver.get_window_position()}')
# 自定义浏览器窗口大小（2000,3000）
driver.set_window_size(2000, 3000)
# 打印浏览器大小
print(f'浏览器大小:\n{driver.get_window_size()}')
# 浏览器窗口最大化
driver.maximize_window()
# 将当前页面截屏保存：D:\IMI\ScreenShot\screen_shot.png
driver.save_screenshot(r'D:\IMI\ScreenShot\screen_shot.png')
# 点击”立即登录“
driver.find_element(By.NAME, 'submit').click()
# 使用pillow进行截图, D:\IMI\ScreenShot\alert_shot.png
image = ImageGrab.grab()
image.save(r"D:\IMI\ScreenShot\alert_shot.png")
# 切换到消息框
alert = driver.switch_to.alert
# 打印消息框里的信息
print(f'消息框的文本信息:\n{alert.text}')
# 点击确定
alert.accept()
# 获取用户名文本框
username_input = driver.find_element(By.NAME, 'username')
# 获取密码文本框
password_input = driver.find_element(By.NAME, 'password')
# 在用户名文本框输入用户名：vip
username_input.send_keys('vip')
# 连续使用组合按键Ctrl+a和Ctrl+c全选后复制其中内容
username_input.send_keys(Keys.CONTROL, 'a')
username_input.send_keys(Keys.CONTROL, 'c')
# 到密码文本框里使用组合键Ctrl+v粘贴
password_input.click()
password_input.send_keys(Keys.CONTROL, 'v')
# 将密码文本框的内容进行清空
password_input.clear()
# 到密码文本框里输入密码：vip,输入回车键确认登录
password_input.send_keys('vip', Keys.ENTER)
# 等待1秒
sleep(1)
# 自动刷新页面后，对包含网站图标在内的最上侧区域进行截屏：D:\IMI\ScreenShot\header_shot.png
driver.find_element(By.CLASS_NAME, 'block.clearfix').screenshot(r'D:\IMI\ScreenShot\header_shot.png')
# 获取关键字文本框控件
search_input = driver.find_element(By.ID, 'keyword')
# 使用链式写法：在关键字文本框输入关键字：806，按下回车进行搜索
actions.click(search_input).send_keys('806').send_keys(Keys.ENTER).perform()
# 等待1秒
sleep(1)
# 页面刷新后需要重新定位控件
search_input = driver.find_element(By.ID, 'keyword')
# 多个参数模拟多个按键组合操作：点击关键字文本框，依次按下END、ARROW_LEFT、DELETE键删除6，再次按下回车来进行搜索
actions.click(search_input).send_keys(Keys.END, Keys.ARROW_LEFT, Keys.DELETE, Keys.ENTER).perform()
# 使用分步写法：点击关键字文本框，连续按下键盘上的Tab键两次，此时当前焦点位于“高级搜索”这个元素，在这个焦点位置按下回车
actions.click(search_input)
actions.send_keys(Keys.TAB, Keys.TAB)
actions.send_keys(Keys.ENTER)
actions.perform()
# 等待1秒
sleep(1)
# 检查”搜索简介“是否选中，若否，则选中
check_box = driver.find_element(By.ID, 'sc_ds')
if not check_box.is_selected():
    check_box.click()
# 获取”分类下拉表“的Select对象
select_select = Select(driver.find_element(By.ID, 'select'))
# 选择分类下拉列表里的“手机类型”选项
select_select.select_by_visible_text('手机类型')
# 在下方的关键字搜索框输入：8
driver.find_element(By.ID, 'keywords').send_keys('8')
# 点击“立即搜索”
driver.find_element(By.NAME, 'Submit').click()
# 等待1秒
sleep(1)
# 获取第二个排序规则下拉列表的Select对象
order_select = Select(driver.find_element(By.NAME, 'order'))
# 获取第二个排序规则下拉列表里当前选项文本并打印
order_text = order_select.first_selected_option.text
print(f'第二个排序规则:{order_text}')
# 如果是“倒序”，就选择文本是“正序”的选项
if order_text == '倒序':
    order_select.select_by_visible_text('正序')
# 点击按钮"GO"
driver.find_element(By.XPATH, "//input[@alt='go']").click()
# 获取第一个排序规则下拉列表的Select对象
sort_select = Select(driver.find_element(By.NAME, 'sort'))
# 获取第一个排序规则下拉列表里当前选项文本并打印
sort_text = sort_select.first_selected_option.text
print(f'第一个排序规则:{sort_text}')
# 如果包含“上架时间”，就从所有选项中选择“按照价格排序”的选项
if "上架时间" in sort_text:
    for option in sort_select.options:
        if "价格" in option.text:  # 或精确匹配：option.text == "按照价格排序"
            sort_select.select_by_visible_text(option.text)
            break
# 点击按钮"GO"
driver.find_element(By.XPATH, "//input[@alt='go']").click()
# 等待1秒
sleep(1)
# 使用关键词搜索，回车进行搜索
driver.find_element(By.ID, 'keyword').send_keys(Keys.ENTER)
# 等待1秒
sleep(1)
# 点击下方商品”诺基亚N96“
driver.find_element(By.LINK_TEXT, '诺基亚N96').click()
# 如果评级等级为2的选项为可选，则选中
rank_two = driver.find_element(By.ID, 'comment_rank2')
if rank_two.is_enabled():
    rank_two.click()
# 在”评论内容“文本框输入：手机一般，不算推荐！
driver.find_element(By.NAME, 'content').send_keys('手机一般，不算推荐！')
# 定位识别验证码元素（包含）
captcha_img = driver.find_element(By.XPATH, '//img[contains(@src, "captcha.php?")]')
# 将图片元素截图保存,D:\IMI\ScreenShot\check_comment.png
captcha_img.screenshot(r'D:\IMI\ScreenShot\check_comment.png')
# 读取图片
img_bytes = open(r'D:\IMI\ScreenShot\check_comment.png', 'rb').read()
# 识别验证码
check_comment_code = ocr.classification(img_bytes)
# 输入验证码(由于黄色背景带圈的验证图容易识别错误，因此有概率失败)
driver.find_element(By.NAME, 'captcha').send_keys(check_comment_code)
# 将输入结果截图保存,D:\IMI\ScreenShot\check_comment_code_input.png
driver.save_screenshot(r'D:\IMI\ScreenShot\check_comment_code_input.png')
# 等待1秒
sleep(1)
# 点击”提交评论“
driver.find_element(By.NAME, '').click()
# 点击消息框”确定“
driver.switch_to.alert.accept()
# 后退
driver.back()
# 点击下方商品”三星BC01“
driver.find_element(By.LINK_TEXT, '三星BC01').click()
# 后退
driver.back()
# 刷新页面
driver.refresh()
# 前进
driver.forward()
# 打印当前URL
print(f'当前URL:{driver.current_url}')
main_handle = driver.current_window_handle
# 点击”EC论坛“
driver.find_element(By.LINK_TEXT, 'EC论坛').click()
# 等待6秒
sleep(6)
# 获取窗口句柄
new_handles = driver.window_handles
# 切换最新窗口
driver.switch_to.window(new_handles[-1])
# 打印当前URL
print(f'当前URL:{driver.current_url}')
# 将窗口内容进行截图保存：D:\IMI\ScreenShot\ec_shot.png
driver.save_screenshot(r'D:\IMI\ScreenShot\ec_shot.png')
# 关闭该窗口
driver.close()
# 切换到第一个窗口
driver.switch_to.window(main_handle)
# 获取”购买数量输入框“控件
number_input = driver.find_element(By.ID, 'number')
# 打印当前URL
print(f'当前URL:{driver.current_url}')
# 打印商品货号
product_code = (driver.find_element(By.XPATH, "//dd[strong[text()='商品货号：']]")
                .text.strip().replace('商品货号：', '').strip())
print(f'商品货号:{product_code}')
# 打印商品库存数量
product_num = (driver.find_element(By.XPATH, "//dd[strong[text()='商品库存：']]")
               .text.strip().replace('商品库存：', '').strip())
print(f'商品库存:{product_num}')
# 打印商品重量
product_weight = (driver.find_element(By.XPATH, "//dd[strong[text()='商品重量：']]")
                  .text.strip().replace('商品重量：', '').strip())
print(f'商品重量:{product_weight}')
# 打印商品点击数
product_hit = (driver.find_element(By.XPATH, "//dd[strong[text()='商品点击数：']]")
               .text.strip().replace('商品点击数：', '').strip())
print(f'商品点击数：{product_hit}')
# 打印上架时间
product_time = (driver.find_element(By.XPATH, "//dd[strong[text()='上架时间：']]")
                .text.strip().replace('上架时间：', '').strip())
print(f'上架时间:{product_time}')
# 打印商品牌对应内容href属性
brand_href = driver.find_element(By.XPATH, "//dd[strong[text()='商品品牌：']]/a").get_attribute('href')
print(f'商品牌href属性:{brand_href}')
# 打印购买数量输入框的value属性
number_value = number_input.get_attribute('value')
print(f'数量输入框的value属性:{number_value}')
# 删除购买数量的默认值
number_input.send_keys(Keys.CONTROL, 'a')
number_input.send_keys(Keys.DELETE)
# 在购买数量输入框输入：4
number_input.send_keys('4')
# 点击选项”黑色“，让鼠标对输入框失焦
driver.find_element(By.ID, 'spec_value_194').click()
# 获取并打印商品总价
total = (driver.find_element(By.XPATH, "//dd[strong[text()='商品总价：']]")
         .text.strip().replace('商品总价：￥', '').replace('元', '').strip())
print(f'商品总价:{total}')
# 如果商品总价等于1120，则点击”加入购物车“
if total == '1120':
    driver.find_element(By.XPATH, "//img[@src='themes/default/images/bnt_cat.gif']").click()
# 将购买数量修改为：2
new_num_input = driver.find_element(By.XPATH, "//input[contains(@id, 'goods_number_')]")
new_num_input.clear()
new_num_input.send_keys('2')
# 点击”更新购物车“
driver.find_element(By.NAME, 'submit').click()
# 不等页面自动刷新，点击”返回购物车“
driver.find_element(By.LINK_TEXT, '返回购物车').click()
# 等待1秒
sleep(1)
# 点击”删除“
driver.find_element(By.LINK_TEXT, '删除').click()
# 点击消息框的”取消“
driver.switch_to.alert.dismiss()
# 点击”放入收藏夹“
driver.find_element(By.LINK_TEXT, '放入收藏夹').click()
# 点击消息框的”确定“
driver.switch_to.alert.accept()
# 点击下方”我的收藏“中第一个商品
driver.find_element(By.XPATH, "//tr[1]/td[1]/a[contains(@class, 'f6')]").click()
# 获取商品图的src属性值，打印图片存储路径
img_url = driver.find_element(By.XPATH, "//img[@alt='P806']").get_attribute('src')
print(f'图片存储路径:{img_url}')
# 打印商品名的文本内容
name_text = driver.find_element(By.XPATH, "//p[@class='f_l']").text
print(f'商品名:{name_text}')
# 点击网站图标返回首页
driver.find_element(By.XPATH, "//img[@src='themes/default/images/logo.gif']").click()
# 在搜索框输入”三星SGH-F258“,回车搜索
driver.find_element(By.ID, 'keyword').send_keys('三星SGH-F258', Keys.ENTER)
# 等待1秒
sleep(1)
# 点击商品”三星SGH-F258“
driver.find_element(By.LINK_TEXT, '三星SGH-F...').click()
# 等待1秒
sleep(1)
# 打印颜色选项的”黑色“是否被选中的判断结果
print(f'”黑色“是否被选中的判断结果:{driver.find_element(By.ID, "spec_value_196").is_selected()}')
# 如果”白色“可选，则选择“白色”
white_radio = driver.find_element(By.ID, "spec_value_198")
if white_radio.is_enabled():
    white_radio.click()
# 点击“加入购物车”
driver.find_element(By.XPATH, "//img[@src='themes/default/images/bnt_cat.gif']").click()
# 点击消息框的“确定”
driver.switch_to.alert.accept()
# 等待1秒
sleep(1)
# 获取“订购数量”输入框控件
num_input = driver.find_element(By.NAME, 'number')
# 获取“订购描述”输入框控件
desc_input = driver.find_element(By.NAME, 'desc')
# 清空“订购数量”
num_input.clear()
# 在“订购数量”输入框输入：3
num_input.send_keys('3')
# 获取“订购描述”输入框输入：1. 请在周五前发货。\n
desc_input.send_keys('1. 请在周五前发货。\n')
# 在“联系人”输入框输入：vip
driver.find_element(By.NAME, 'linkman').send_keys('vip')
# 在“电子邮件地址”输入框输入："vip@qq.com"
driver.find_element(By.NAME, 'email').send_keys('vip@qq.com')
# 获取“订购描述”输入框输入："2. 商品需用气泡袋包好，避免运输破损。\n"
desc_input.send_keys('2. 商品需用气泡袋包好，避免运输破损。\n')
# 在“联系电话”输入框输入：13829574632
driver.find_element(By.NAME, 'tel').send_keys('13829574632')
# 获取“订购描述”输入框输入："3. 如需，请及时联系备用电话：17580327496。"
desc_input.send_keys('3. 如需，请及时联系备用电话：17580327496。\n')
# 点击“提交缺货登记”
driver.find_element(By.NAME, 'submit').click()
# 页面自动刷新后，截图保存“系统信息”模块内容：D:\IMI\ScreenShot\box_shot.png
sleep(1)
driver.find_element(By.CLASS_NAME, 'box_1').screenshot(r'D:\IMI\ScreenShot\box_shot.png')
# 退出浏览器
driver.quit()
