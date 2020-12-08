import unittest
import time
from random import randint  # 使用randint产生随机整数


class SortAlgorithm(object):

    def __init__(self, arr):
        self.origin_arr = arr

    def bubble_sort(self):
        """冒泡排序"""
        arr = self.origin_arr.copy()
        start = time.clock() # 记录开始时间
        number = len(arr)  # 数组的长度
        has_changed = True  # 一趟遍历中是否发生过交换
        x = 0
        while has_changed:
            has_changed = False  # 每次循环复位
            for i in range(1, number - x):  # 每次循环减少一次，因为后面的数列已经是有序
                if arr[i - 1] > arr[i]:
                    arr[i - 1], arr[i] = arr[i], arr[i - 1]  # 交换位置
                    has_changed = True
            x += 1
        operation_time =time.clock() - start
        return arr, operation_time

    def selection_sort(self):
        """选择排序"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间
        for i in range(len(arr)):
            min_index = i  # 初始化下标，以无序序列的第一个元素为开始
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_index]:  # 从待排序序列中找最小值
                    min_index = j  # 把最小值下标记录下来
            arr[min_index], arr[i] = arr[i], arr[min_index]  # 当前位置元素交换位置
        operation_time = time.clock() - start
        return arr, operation_time

    def insertion_sort(self):
        """直接插入排序"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间
        for i in range(len(arr)):
            key = arr[i]  # 暂存当前元素值
            position = i  # 记录位移位置
            while position > 0 and key < arr[position - 1]:
                arr[position] = arr[position - 1]
                position -= 1  # 位移多一次，下标值减一
            arr[position] = key  # 把之前元素插入到这个位置
        operation_time = time.clock() - start
        return arr, operation_time

    def binary_sertion_sort(self):
        """折半插入排序"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间
        for i in range(len(arr)):
            key = arr[i]  # 暂存当前元素值
            position_low = 0  # 有序序列第一位元素下标
            position_hight = i - 1  # 有序序列末位元素下标
            while position_low <= position_hight:
                mid = (position_low + position_hight) // 2  # 中间元素下标
                if key > arr[mid]:
                    position_low = mid + 1  # 看中间位置右半部分
                else:
                    position_hight = mid - 1  # 看中间位置左半部分
            # 找到插入位置后，下标值为position_low(mid值也相同)
            for j in range(i, position_low, -1):
                arr[j] = arr[j - 1]  # 向右位移，腾出空间插入新元素
            arr[position_low] = key  # 插入新元素
        operation_time = time.clock() - start
        return arr, operation_time

    def merge_sort(self):
        """归并排序"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间

        def merge(left, right):
            """左右子序列合并"""
            merged = left + right  # 创建一个和左右子序列相同大小的列表
            left_positon, right_positon = 0, 0
            while left_positon < len(left) and right_positon < len(right):
                # 对左右子序列每个元素进行比较排序，放到新的有序序列里面
                if left[left_positon] <= right[right_positon]:
                    merged[left_positon + right_positon] = left[left_positon]
                    left_positon += 1
                else:
                    merged[left_positon + right_positon] = right[right_positon]
                    right_positon += 1
            # 如果某一边子序列已经排序结束，那么把另外一边的子序列直接加到新的序列后面
            for left_positon in range(left_positon, len(left)):
                merged[left_positon + right_positon] = left[left_positon]
            for right_positon in range(right_positon, len(right)):
                merged[left_positon + right_positon] = right[right_positon]
            return merged

        def sort(arr):
            if len(arr) <= 1:  # 不多于一个元素，最小的子序列，不用继续拆分
                return arr
            mid = len(arr) // 2  # 找到序列中间位置的下标
            # 中间分开左右两个子序列，子序列递归调用merge_sort()函数进行归并排序
            left, right = sort(arr[:mid]), sort(arr[mid:])
            # 返回的结果是有序的子序列，然后把子序列通过merge()函数合并子序列
            return merge(left, right)

        arr = sort(arr)
        operation_time = time.clock() - start
        return arr, operation_time

    def quick_sort(self):
        """快速排序"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间

        def partition(arr, begin, end):
            base_index = begin  # 选择序列第一个元素作为基准值
            for i in range(begin + 1, end + 1):
                if arr[i] <= arr[begin]:  # 如果元素大于基准值位置不变，若否则调换位置
                    base_index += 1  # 记录基准值的新位置
                    arr[i], arr[base_index] = arr[base_index], arr[i]
            arr[base_index], arr[begin] = arr[begin], arr[base_index]  # 把基准值放到新位置
            return base_index

        def quick_sort_recursion(arr, begin, end):
            if begin >= end:  # 若开始下标和结束下标重合，就是最小的子序列不用继续拆解
                return
            base_index = partition(arr, begin, end)  # 找出基准值的新下标
            quick_sort_recursion(arr, begin, base_index - 1)  # 小于基准值的子序列
            quick_sort_recursion(arr, base_index + 1, end)  # 大于基准值的子序列

        def sort_1(arr):
            """快速排序"""
            begin = 0  # 刚开始是整个列表
            end = len(arr) - 1  # 列表最末端下标
            quick_sort_recursion(arr, begin, end)  # 递归求解

        sort_1(arr)
        operation_time = time.clock() - start
        return arr, operation_time

    def quick_sort_2(self):
        """快速排序优化"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间

        def partition_random(arr, begin, end):
            """优化选择基准值的方式"""
            base_index = randint(begin, end)  # 随机选择序列某个元素作为基准值
            arr[begin], arr[base_index] = arr[base_index], arr[begin]  # 把基准值调到最前面
            base_index = begin
            for i in range(begin + 1, end + 1):
                if arr[i] <= arr[begin]:  # 如果元素大于基准值位置不变，若否则调换位置
                    base_index += 1  # 记录基准值的新位置
                    arr[i], arr[base_index] = arr[base_index], arr[i]
            arr[base_index], arr[begin] = arr[begin], arr[base_index]  # 把基准值放到新位置
            return base_index

        def quick_sort_recursion(arr, begin, end):
            if begin >= end:  # 若开始下标和结束下标重合，就是最小的子序列不用继续拆解
                return
            base_index = partition_random(arr, begin, end)  # 找出基准值的新下标
            quick_sort_recursion(arr, begin, base_index - 1)  # 小于基准值的子序列
            quick_sort_recursion(arr, base_index + 1, end)  # 大于基准值的子序列

        def sort_2(arr):
            """快速排序"""
            begin = 0  # 刚开始是整个列表
            end = len(arr) - 1  # 列表最末端下标
            quick_sort_recursion(arr, begin, end)  # 递归求解

        sort_2(arr)
        operation_time = time.clock() - start
        return arr, operation_time

    def python_sort(self):
        """Python内置排序"""
        arr = self.origin_arr.copy()
        start = time.clock()  # 记录开始时间
        arr.sort()
        operation_time = time.clock() - start
        return arr, operation_time


class TestCase_sort(unittest.TestCase):
    """排序算法比较"""
    def setUp(self):
        # 测试用例执行前的初始化操作
        print('比较1:5000个随机排列的数')
        self.number = 5000
        self.input_arr = [randint(0, 1000000) for _ in range(self.number)]
        # 用内置排序的结果作为标准答案，用于验证排序的正确性
        self.answer = sorted(self.input_arr)
        # 创建对象，所有排序使用同样的输入
        self.sort = SortAlgorithm(self.input_arr)
        self.result = [] # 用于记录排序结果，做对比

    def tearDown(self):
        # 测试用例执行后运行
        self.result.sort(key=lambda x:x[1]) # 结果按用时排序
        for data in self.result:  # 输入结果到屏幕
            print("{},{}".format(data[0], data[1]))

    def test1_5000_sort(self):
        """测试"""
        arr, op_time = self.sort.bubble_sort()
        random_index = randint(0, self.number) # 随机挑选一个位置，对比答案
        # 测试用例期望两个结果相等，若不相等，测试结束
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['冒泡排序', op_time]) # 记录排序用时

        arr, op_time = self.sort.selection_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['选择排序', op_time])

        arr, op_time = self.sort.insertion_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['插入排序', op_time])

        arr, op_time = self.sort.merge_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['归并排序', op_time])

        arr, op_time = self.sort.quick_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['快速排序', op_time])

        arr, op_time = self.sort.quick_sort_2()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['快速排序优化版', op_time])

        arr, op_time = self.sort.python_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['Python内置排序', op_time])


class TestCase_sort2(unittest.TestCase):
    """排序算法比较"""
    def setUp(self):
        # 测试用例执行前的初始化操作
        print('2500个升序排序的数和2500个随机数')
        self.number = 5000
        self.input_arr = [_ for _ in range(1,2500)]
        self.input_arr += [randint(0, 1000000) for _ in range(self.number-2500)]
        # 用内置排序的结果作为标准答案，用于验证排序的正确性
        self.answer = sorted(self.input_arr)
        # 创建对象，所有排序使用同样的输入
        self.sort = SortAlgorithm(self.input_arr)
        self.result = [] # 用于记录排序结果，做对比

    def tearDown(self):
        # 测试用例执行后运行
        self.result.sort(key=lambda x:x[1]) # 结果按用时排序
        for data in self.result:  # 输入结果到屏幕
            print("{},{}".format(data[0], data[1]))

    def test1_5000_sort(self):
        """测试"""
        arr, op_time = self.sort.bubble_sort()
        random_index = randint(0, self.number) # 随机挑选一个位置，对比答案
        # 测试用例期望两个结果相等，若不相等，测试结束
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['冒泡排序', op_time]) # 记录排序用时

        arr, op_time = self.sort.selection_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['选择排序', op_time])

        arr, op_time = self.sort.insertion_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['插入排序', op_time])

        arr, op_time = self.sort.merge_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['归并排序', op_time])

        arr, op_time = self.sort.quick_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['快速排序', op_time])

        arr, op_time = self.sort.quick_sort_2()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['快速排序优化版', op_time])

        arr, op_time = self.sort.python_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['Python内置排序', op_time])


class TestCase_sort3(unittest.TestCase):
    """排序算法比较"""
    def setUp(self):
        # 测试用例执行前的初始化操作
        print('2500个降序排序的数和2500个随机数')
        self.number = 5000
        self.input_arr = [_ for _ in range(2500, 0, -1)]
        self.input_arr += [randint(0, 1000000) for _ in range(self.number-2500)]
        # 用内置排序的结果作为标准答案，用于验证排序的正确性
        self.answer = sorted(self.input_arr)
        # 创建对象，所有排序使用同样的输入
        self.sort = SortAlgorithm(self.input_arr)
        self.result = [] # 用于记录排序结果，做对比

    def tearDown(self):
        # 测试用例执行后运行
        self.result.sort(key=lambda x:x[1]) # 结果按用时排序
        for data in self.result:  # 输入结果到屏幕
            print("{},{}".format(data[0], data[1]))

    def test1_5000_sort(self):
        """测试"""
        arr, op_time = self.sort.bubble_sort()
        random_index = randint(0, self.number) # 随机挑选一个位置，对比答案
        # 测试用例期望两个结果相等，若不相等，测试结束
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['冒泡排序', op_time]) # 记录排序用时

        arr, op_time = self.sort.selection_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['选择排序', op_time])

        arr, op_time = self.sort.insertion_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['插入排序', op_time])

        arr, op_time = self.sort.merge_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number )
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['归并排序', op_time])

        arr, op_time = self.sort.quick_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['快速排序', op_time])

        arr, op_time = self.sort.quick_sort_2()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['快速排序优化版', op_time])

        arr, op_time = self.sort.python_sort()
        # 随机挑选一个位置，对比答案
        random_index = randint(0,self.number)
        self.assertEqual(arr[random_index], self.answer[random_index])
        self.result.append(['Python内置排序', op_time])


if __name__ == '__main__':
    unittest.main()  # 启动测试

