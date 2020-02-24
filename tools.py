# 创建结点对象
class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        if left is not None and not isinstance(left, TreeNode):
            raise ValueError('左孩子结点必须是结点类')
        if right is not None and not isinstance(right, TreeNode):
            raise ValueError('左孩子结点必须是结点类')
        self.value = value  # 结点值
        self.left = left  # 左孩子结点
        self.right = right  # 右孩子结点

    def __repr__(self):
        return 'TreeNode({})'.format(self.value)

    def insert_left(self, value):
        # 在左边插入新的结点
        if self.left == None:
            self.left = TreeNode(value)
        else:
            # 若结点存在，把原来结点放到新结点的左孩子结点
            tmp = TreeNode(value)
            tmp.left = self.left
            self.left = tmp

    def insert_right(self, value):
        # 在右边插入新的结点
        if self.right == None:
            self.right = TreeNode(value)
        else:
            # 若结点存在，把原来结点放到新结点的右孩子结点
            tmp = TreeNode(value)
            tmp.right = self.right
            self.right = tmp

    def pre_order_traversal(self):
        # 先序遍历：根-左-右
        result = [self.value]  # 先访问根结点
        if self.left:
            # 再访问左边子树，在子树里面递归使用先序遍历里面的结点
            result += self.left.pre_order_traversal()
        if self.right:
            # 最后访问右边子树
            result += self.right.pre_order_traversal()
        return result

    def in_order_traversal(self):
        # 中序遍历：左-根-右
        result = []
        if self.left:
            # 遍历左边子树
            result += self.left.in_order_traversal()
        # 接着访问根结点
        result.append(self.value)
        if self.right:
            # 遍历右边子树
            result += self.right.in_order_traversal()
        return result

    def post_order_traversal(self):
        # 后序遍历：左-右-根
        result = []
        if self.left:
            result += self.left.post_order_traversal()
        if self.right:
            result += self.right.post_order_traversal()
        result.append(self.value)
        return result

# 创建二叉查找树对象
class BinarySearchTreeNode(object):
    def __init__(self, value, left=None, right=None):
        if left is not None and not isinstance(left, TreeNode):
            raise ValueError('左孩子结点必须是结点类')
        if right is not None and not isinstance(right, TreeNode):
            raise ValueError('左孩子结点必须是结点类')
        self.value = value  # 结点值
        self.left = left    # 左孩子结点
        self.right = right  # 右孩子结点
    def __repr__(self):
        return 'TreeNode({})'.format(self.value)
    def insert(self, value):
        # 二叉查找树插入操作
        if value <= self.value:
            # 左子树所有值<=双亲结点
            if self.left:
                self.left = self.left.insert(value)
            else:
                self.left = BinarySearchTreeNode(value)
        elif value > self.value:
            # 双亲结点<右子树所有值
            if self.right:
                self.right = self.right.insert(value)
            else:
                self.right = BinarySearchTreeNode(value)
        return self
    def in_order_traversal(self):
        result = []
        if self.left:
            result += self.left.in_order_traversal()
        result.append(self.value)
        if self.right:
            result += self.right.in_order_traversal()
        return result
    def find_min(self):
        # '查找二叉搜索树中最小值点
        if self.left:
            return self.left.find_min()
        else:
            return self
    def find_max(self):
        # 查找二叉查找树中最大值点
        if self.right:
            return self.right.find_max()
        else:
            return self
    def del_node(self, value):
        # 删除二叉搜索树中值为value的点
        if self == None:
            return
        if value < self.value:
            self.left = self.left.del_node(value)
        elif value > self.value:
            self.right = self.right.del_node(value)
        # 当value=self.value时，分为三种情况：只有左子树;只有右子树;有左右子树或者即无左子树又无右子树
        else:
            if self.left and self.right:
                # 既有左子树又有右子树，则需找到右子树中最小值节点
                tmp = self.right.find_min()
                self.value = tmp.value
                # 再把右子树中最小值节点删除
                self.right = self.right.del_node(tmp.value)
            elif self.right == None and self.left == None:  # 左右子树都为空
                self = None
            elif self.right == None:   # 只有左子树
                self = self.left
            elif self.left == None:    # 只有右子树
                self = self.right
        return self

def print_tree(root):
    """
    输入根结点: 使用上面定义的BinarySearchTreeNode
    结果是: 多行字符串
    """

    def get_tree_level(node):
        # 返回树的层数
        if not node:
            return 0
        return 1 + max(get_tree_level(node.left), get_tree_level(node.right))

    rows = get_tree_level(root)
    cols = 2 ** rows - 1  # 根据深度算出预留空间大小
    res = [[" "] * cols for _ in range(rows)]
    trunks = [[" "] * cols for _ in range(rows - 1)]

    def build_tree(node, level, pos, parent_index):
        if not node:
            return
        left_padding = 2 ** (rows - level - 1) - 1  # 偏移量
        spacing = 2 ** (rows - level) - 1  # 左右孩子结点偏移
        index = left_padding + pos * (spacing + 1)  # 确定偏移位置下标

        if parent_index:  # 根据双亲结点和孩子结点的下标，求出＂树枝＂的下标
            if parent_index > index:
                trunk_index = index + (parent_index - index) // 2
                trunk_val = "/"
            else:
                trunk_index = parent_index + (index - parent_index) // 2
                trunk_val = "\\"  # 第一个＂\＂是Python关键字，表示转义特殊字符，第二个＂\＂代表字符\
            trunks[level - 1][trunk_index] = trunk_val

        res[level][index] = str(node.value)  # 填入对应结点的数值
        build_tree(node.left, level + 1, pos << 1, index)  # 是否有下一个左结点
        build_tree(node.right, level + 1, (pos << 1) + 1, index)  # # 是否有下一个右结点，

    build_tree(root, 0, 0, None)
    # 在屏幕中输出二叉树
    for level in range(len(trunks)):
        print("".join(res[level]))  # 把列表数据变成字符串输出
        print("".join(trunks[level]))
    print("".join(res[-1]))
