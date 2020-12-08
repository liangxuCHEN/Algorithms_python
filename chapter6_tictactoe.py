import time
class Game(object):
    """井字游戏"""
    def __init__(self):
        # 实例化类便开始初始化游戏
        self.initialize_game()

    # 初始化棋盘
    def initialize_game(self):
        self.current_state = [['.','.','.'],
                              ['.','.','.'],
                              ['.','.','.']]
        # 玩家X用X作为标记，作为先手
        self.player_turn = 'X'

    # 打印棋盘在屏幕上
    def draw_board(self):
        for i in range(0, 3):
            for j in range(0, 3):
                # 如果棋盘没有放置，显示位置坐标
                if self.current_state[i][j] == ".":
                    val = "({},{})".format(i, j)
                else:
                    val = self.current_state[i][j]
                if j != 2:
                    print('%-5s|' % val, end=" ") # -5s是指定占位空间
                else: # 最后一个元素输出就换行
                    print('{}'.format(val))
        print()

    # 判断棋子位置是否合理
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2:
            return False # 坐标不在棋盘上，不通过
        elif self.current_state[px][py] != '.':
            return False # 坐标已经有标记了，不通过
        else: # 其他情况是合理的
            return True

    # 每一步之后都检查游戏是否结束，给出胜利者
    def is_end(self):
        for i in range(0, 3):
            # 水平是否连线
            if (self.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'
            # 垂直是否连线
            if self.current_state[0][i] != '.':
                if  self.current_state[0][i] == self.current_state[1][i] == self.current_state[2][i]:
                    return self.current_state[0][i] # 返回赢家(该位置上的符号)
        # 斜线是否连线
        if self.current_state[0][0] != '.':
            if self.current_state[0][0] == self.current_state[1][1]  == self.current_state[2][2]:
                return self.current_state[0][0]
        # 斜线是否连线
        if self.current_state[0][2] != '.':
            if self.current_state[0][2] == self.current_state[1][1] == self.current_state[2][0]:
                return self.current_state[0][2]
        # 棋盘是否已经放满
        for i in range(0, 3):
            if self.current_state[i].count(".") > 0: # 若还有"."，说明还有位置
                return None  # 还有位置，返回空，游戏继续
        return '.' # 平局返回"."

    # 符号 'O' 玩家是计算机，求极大值
    def max(self):
        # 有可能的价值为-1（失败），0（平局），1（胜利）
        max_val = -2 # max_val是初始化alpha值，-2已经小于所有值
        px = None # 坐标初始化
        py = None
        result = self.is_end() # 返回当前结果
        # 如果已经结束，就是递归返回
        # 这里是构建完整树图，所以不设置递归深度
        # 一直递归至游戏结束，根据结果返回评估值
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    # 遍历每一个位置，如果是可以放棋子，就尝试在这里放棋子
                    self.current_state[i][j] = 'O'
                    # 然后作为一个分支，在下一层求极小值中寻找极大值
                    (m, min_i, min_j) = self.min()
                    if m > max_val: # 若有极大值，则更新下棋坐标
                        max_val = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.' # 尝试结束后要清空这位置
        return (max_val, px, py)

    # 符号 'X' 玩家是人，是计算机对手，所以是求极小值
    def min(self):
        # 有可能的价值为-1（胜利），0（平局），1（失败），刚好与计算机相反
        min_val = 2 # min_val初始化，2已经大于所有值
        qx = None # 坐标初始化
        qy = None
        result = self.is_end() # 返回当前结果
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    # 遍历每一个位置，如果是可以放棋子，就尝试在这里放棋子
                    self.current_state[i][j] = 'X'
                    # 然后作为一个分支，在下一层求极大值中寻找极小值
                    (m, max_i, max_j) = self.max()
                    if m < min_val: # 若有极小值，则更新下棋坐标
                        min_val = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'
        return (min_val, qx, qy)

    # 开始游戏，程序入口
    def play(self):
    	# 极大值极小值算法
        while True: # 轮流下棋，直到游戏结束
            self.draw_board() # 先把当前棋盘打印在屏幕上
            self.result = self.is_end()  # 判断是否结束游戏
            if self.result != None:      # 游戏结束
                if self.result == 'X':   # 如果是X是胜利者
                    print('胜者为X!')
                elif self.result == 'O': # 反之亦然
                    print('胜者为O!')
                elif self.result == '.': # 平局
                    print("平局")
                self.initialize_game() # 初始化棋盘，结束游戏
                return
            # 若没有结束游戏，看到谁下棋
            if self.player_turn == 'X': # 到X下棋
                while True:
                    start = time.time() # 记录X的思考时间
                    # 这里可以忽略，不给人类提示也可以的
                    (m, qx, qy) = self.min() # X是代表人，也就是程序对手，所以找极小值
                    end = time.time() # 思考结束，得到下棋的坐标qx，qy
                    print('用时: {}s'.format(round(end - start, 7)))
                    print('推荐步骤: X = {}, Y = {}'.format(qx, qy))
                    try:
                        px = int(input('输入坐标值x: '))
                        py = int(input('输入坐标值y: '))
                    except:
                        # 若输入不能转化为整数，请再次输入
                        print('输入不符合要求，请再次输入。')
                        break
                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('输入不符合要求，请再次输入。')
            else:
                (m, px, py) = self.max() # 到计算机下棋，所以要找极大值
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'

    def max_alpha_beta(self, alpha, beta):
        max_val = -2
        px = None
        py = None
        result = self.is_end()
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > max_val:
                        max_val = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'
                    # 前面的思路是一样的，主要添加以下剪枝条件的判断
                    alpha = max(max_val, alpha)
                    if beta <= alpha:
                        return (max_val, px, py)
        return (max_val, px, py)

    def min_alpha_beta(self, alpha, beta):
        min_val = 2
        qx = None
        qy = None
        result = self.is_end()
        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < min_val:
                        min_val = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'
                    # 前面的思路是一样的，主要添加以下剪枝条件的判断
                    beta = min(min_val, beta)
                    if beta <= alpha:
                        return (min_val, qx, qy)
        return (min_val, qx, qy)

    def play_alpha_beta(self):
    	# 极大极小值算法+剪枝算法
        while True:
            self.draw_board()  # 先把当前棋盘打印在屏幕上
            self.result = self.is_end()  # 判断是否结束游戏
            if self.result != None:  # 游戏结束
                if self.result == 'X':  # 如果是X是胜利者
                    print('胜者为X!')
                elif self.result == 'O':  # 反之亦然
                    print('胜者为O!')
                elif self.result == '.':  # 平局
                    print("平局")
                self.initialize_game()  # 初始化棋盘，结束游戏
                return

            if self.player_turn == 'X':
                while True:
                    start = time.time()
                    # X是代表人，也就是程序对手，所以找极小值，alpha,beta初始化值为-2,2
                    (m, qx, qy) = self.min_alpha_beta(-2, 2)
                    end = time.time()
                    print('用时: {}s'.format(round(end - start, 7)))
                    print('推荐步骤: X = {}, Y = {}'.format(qx, qy))
                    try:
                        px = int(input('输入坐标值x: '))
                        py = int(input('输入坐标值y: '))
                    except:
                        # 若输入不能转化为整数，请再次输入
                        print('输入不符合要求，请再次输入。')
                        break

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('输入不符合要求，请再次输入。')
            else:
                # 到计算机下棋，所以要找极大值,alpha,beta初始化值为-2,2
                (m, px, py) = self.max_alpha_beta(-2, 2)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'


if __name__ == "__main__":
    g = Game()
    g.play_alpha_beta()