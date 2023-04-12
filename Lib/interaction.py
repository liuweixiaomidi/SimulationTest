def space():
    print()


def conversation():
    """
    运行后的对话信息
    用于进行策略选择
    :return: None
    """
    space()
    print('仿真测试发单设置: ')
    space()
    print('策略: 发单策略的设置, 根据提示进行选择')
    order_type = int(input('   - 订单类型(取放货订单: 1, 分拨单: 2, 混合类型: 3): '))
    if order_type in [1, 2, 3]:
        print(order_type)


if __name__ == '__main__':
    conversation()
