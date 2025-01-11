import sys

# sys.argv[0] 是脚本名称
# sys.argv[1:] 是传递给脚本的参数
if len(sys.argv) > 1:
    print(f"命令行参数：{sys.argv[1:]}")
else:
    print("没有传递命令行参数")
