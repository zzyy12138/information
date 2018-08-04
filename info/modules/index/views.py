"""create by zhouzhiyang"""
from info import redis_store
from info.models import User, News, Category
from info.utils.response_code import RET
from . import index_blu
from flask import render_template, current_app, session, jsonify


# 首页内容
@index_blu.route('/', methods=['GET', 'POST'])
def show_index_page():
    # 测试redis
    redis_store.set('name', 'zhangsan')

    # 测试session
    # session['name'] = 'banzhang'
    # print('helloworld')

    # logging.debug('调试信息')
    # logging.info('详细信息!!')
    # logging.warning('警告信息')
    # logging.error('错误信息')

    # 上面四句话可以写成如下形式,使用current_app,多了分割线,但是在文件中输出的内容完全一样
    # current_app.logger.debug('调试信息++')
    # current_app.logger.info('详细信息!!++')
    # current_app.logger.warning('警告信息++')
    # current_app.logger.error('错误信息++')

    # 获取session中的用户信息
    user_id = session.get("user_id")

    # 获取用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 查询热门新闻前10条
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="新闻查询失败")

    # 将新闻对象列表,转成字典列表
    click_news_list = []
    for news in news_list:
        click_news_list.append(news.to_dict())

    # 查询分类数据
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="分类查询失败")

    # 将分类对象列表,转成字典列表
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    data = {
        # 判断user如果有值,返回左边内容,否则返回右边的值
        "user_info": user.to_dict() if user else "",
        "click_news_list": click_news_list,
        "categories": category_list
    }

    return render_template('news/index.html', data=data)


# 浏览器在访问,在访问每个网站的时候,都会发送一个Get请求,向/favicon.ico地址获取logo
# app中提供了方法send_static_file,会自动寻找static静态文件下面的资源
@index_blu.route('/favicon.ico')
def get_web_logo():
    return current_app.send_static_file('news/favicon.ico')
