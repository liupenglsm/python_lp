# __init__.py

# 定义变量
version = '1.0'


# 定义函数
def greeting(name):
    print(f'Hello, {name}!')


# 导入模块
from . import BeautifulSoupTest
from . import RegularExpressionTest

# 控制导入行为
__all__ = ['RegularExpressionTest', 'BeautifulSoupTest', 'greeting']
