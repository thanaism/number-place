class ClassA:
    def __init__(self):
        self.var_a = 1
        self.var_b = 2


class_a = ClassA()
# コンストラクタで定義されている変数
print(class_a.var_a)

# クラス内に定義されていないインスタンス変数を外部から作成できる
class_a.var_c = 3
print(class_a.var_c)

# どうやらクラス変数も外部から作成できる
ClassA.var_global = 100
print(ClassA.var_global)
