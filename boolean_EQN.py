import sympy
import numpy as np
import math
import queue


class Node:

    def __init__(self, term, level) -> None:
        '''
        项
        '''
        self.level = level # '-'的个数
        self.term = term   # 二进制形式（含有-)
        self.covered = False

    def one_num(self):
        '''
        返回term中'1'的个数
        '''
        return self.term.count('1')

    def compare(self, node1):
        '''
        比较两个Node能否合并
        '''
        res = []
        for i in range(len(self.term)):
            if self.term[i] == node1.term[i]:
                continue
            elif self.term[i] == '-' or node1.term[i] == "-":
                return (False, None)
            else:
                res.append(i)
        if len(res) == 1:
            return (True, res[0])
        return (False, None)

    def term2logic(self):
        logic_term = ''
        count=0
        for i in range(len(self.term)):
            if self.term[i] == "-":
                count+=1
            elif self.term[i] == "1":
                if count == 0:
                    logic_term += 'A'
                elif count==1:
                    logic_term += 'B'
                elif count==2:
                    logic_term += 'C'
                elif count==3:
                    logic_term += 'D'
                elif count==4:
                    logic_term += 'E'
                count+=1    
            else:
                if count == 0:
                    logic_term += "A'"
                elif count==1:
                    logic_term += "B'"
                elif count==2:
                    logic_term += "C'"
                elif count==3:
                    logic_term += "D'"
                elif count==4:
                    logic_term += "E'"
                count+=1    
        if len(logic_term) == 0: # 补充结果为1的情况
            logic_term = '1'
        return logic_term


class QM:

    def __init__(self, num, lst) -> None:
        self.max_bits = num
        self.minterm_list = sorted(lst) # sort from min to max.
        if len(self.minterm_list) == 0:
            print(0)
            exit()
        if self.minterm_list[-1] >= 2**self.max_bits:
            raise ValueError('input wrong！')
        self.node_list = []
        self.PI = []

    def num2str(self, num):
        '''
        将十进制数num转成二进制字符串term
        '''
        str = format(num, "b").zfill(self.max_bits)
        return str

    def _comp_binary_same(self, term, number):
        '''
        比较一个term是否能cover一个二进制串number
        '''
        for i in range(len(term)):
            if term[i] != '-':
                if term[i] != number[i]:
                    return False
        return True

    def _initial(self):
        '''
        将所有最小项以节点的形式储存，并根据'1'的个数分组
        '''
        flag = True # 判断是否需要进行下一轮递归比较
        groups = [[] for i in range(self.max_bits + 1)]
        for minterm in self.minterm_list:
            tmp_node = Node(term=self.num2str(minterm), level=0)
            groups[tmp_node.one_num()].append(tmp_node)
            flag = True
        self.node_list.append(groups)
        return flag

    def merge(self, level):
        '''
        多次合并
        '''
        flag = False                                        # flag用于判断是否需要进行下一轮的递归比较
        if level == 0:
            flag = self._initial()
        else:
            groups = self.node_list[level - 1]
            new_groups = [[] for i in range(self.max_bits + 1)]
            term_set = set()                                # 用来判断某个形式是否已经存在
            for i in range(len(groups) - 1):
                for node0 in groups[i]:
                    for node1 in groups[i + 1]:
                        cmp_res = node0.compare(node1)
                        if cmp_res[0]:
                            node0.covered = True
                            node1.covered = True
                            new_term = '{}-{}'.format(
                                node0.term[:cmp_res[1]],
                                node0.term[cmp_res[1] + 1:]
                            )
                            tmp_node = Node(term=new_term, level=level)
                            if tmp_node.term not in term_set:
                                new_groups[tmp_node.one_num()].append(tmp_node)
                                term_set.add(tmp_node.term)
                                # print(tmp_node.term)
                                flag = True
            self.node_list.append(new_groups)
        if flag:
            self.merge(level + 1)

    def backtracking(self):
        '''
        收集所有的主蕴含项PI
        '''
        for groups in self.node_list:
            for group in groups:
                for node in group:
                    if not node.covered:
                        self.PI.append(node)
        return self.PI

    def find_essential_prime(self, Chart):
        '''
        找到质主蕴含项
        '''
        pos = np.argwhere(Chart.sum(axis=0) == 1)
        essential_prime = []
        for i in range(len(self.PI)):
            for j in range(len(pos)):
                if Chart[i][pos[j][0]] == 1:
                    essential_prime.append(i)
        essential_prime = list(set(essential_prime)) # 去除重复
        return essential_prime

    def cover_left(self, Chart):
        '''
        用BFS（广度优先搜索）的方法遍历，找出项最少的方法
        '''
        list_result = []
        max_len = len(Chart)                           # 最大广度，也就是最多用到的项数
        myQueue = queue.Queue(math.factorial(max_len)) # 队列
        for i in range(max_len):
            myQueue.put([i])

        stop_flag = False                          # 停止搜索标志
        while not myQueue.empty():
            minterm_mark = np.zeros(len(Chart[0])) # 用于标记剩余的最小项是否被cover了
            choice = myQueue.get()
            if stop_flag and len(list_result[-1]) < len(choice):
                break

            for row in choice:
                minterm_mark += Chart[row]

            if all(minterm_mark): # 如果当前choice能cover所有minterm
                list_result.append(choice)
                stop_flag = True  # 设置标志但不马上退出，防止有多解

            for row in range(choice[-1] + 1, max_len):
                myQueue.put(choice + [row]) # 产生新节点，加入队列
        return list_result

    def find_minimum_cost(self, Chart):
        '''
        找到项数最少的方案
        '''
        QM_final = []
        essential_prime = self.find_essential_prime(Chart)

        # 更新Chart
        for i in range(len(essential_prime)):
            for j in range(len(Chart[0])):
                if Chart[essential_prime[i]][j] == 1:
                    for row in range(len(Chart)):
                        Chart[row][j] = 0

        # 如果Chart都是0，说明质主蕴含项已经覆盖所有最小项，已经得到最终结果了
        if not np.sum(Chart):
            QM_final = [essential_prime]
        # 否则找出未被质主蕴含项covered的minterm，以及那些能cover它们的PI（的行坐标）
        else:
            pos_col_left = np.argwhere(Chart.sum(axis=0) > 0) # 注意这一步得到的是二维数组
            pos_row_left = np.argwhere(Chart.sum(axis=1) > 0) # 这里还是二维数组，之前写错了

            # 生成新的Chart，删去全为0的行列
            new_Chart = np.zeros([len(pos_row_left), len(pos_col_left)])
            for i in range(len(pos_row_left)):
                for j in range(len(pos_col_left)):
                    if Chart[pos_row_left[i][0]][pos_col_left[j][0]] == 1:# 这里也相应地修改为二维的形式
                        new_Chart[i][j] = 1

            list_result = self.cover_left(new_Chart)
            for lst in list_result:
                final_solution = essential_prime + list(
                    map(lambda x: pos_row_left[x], lst)
                )
                QM_final.append(final_solution)
        return QM_final

    def select(self):
        '''
        选择最终方案并输出
        '''
        Chart = np.zeros([len(self.PI), len(self.minterm_list)])
        for i in range(len(self.PI)):
            for j in range(len(self.minterm_list)):
                if self._comp_binary_same(
                    self.PI[i].term, self.num2str(self.minterm_list[j])
                ):
                    Chart[i][j] = 1

        primes = self.find_minimum_cost(Chart)
        # primes = list(set(primes))
        count=0
        for prime in primes:
            str = ''
            for i in range(len(self.PI)):
                for j in prime:
                    if i == j:
                        str = str + self.PI[i].term2logic() + ', '
                        count+=1
            if str[-2] == ',':
                str = str[:-2]
        return str,count

    def run(self):
        '''
        运行入口
        '''
        self.merge(0)
        self.backtracking()
        #self.select()
    
    def get_prime_implicants(self):
        """Returns the Prime Implicants and their count."""
        prime_implicants = ", ".join([pi.term2logic() for pi in self.PI])
        count = len(self.PI)
        return prime_implicants, count
    


def extract_variables(expression):
    """从给定的布尔表达式中提取变量。"""
    return sorted(set(filter(lambda x: x.isalpha(), expression)))

def get_minterms(expression, variables):
    minterms = []
    symbols = {var: sympy.symbols(var) for var in variables}
    for var in variables:
        expression = expression.replace(f"{var}!S", f"~{var}")

    expr = sympy.sympify(expression, locals=symbols)
    total_vars = len(variables)
    for i in range(2**total_vars):
        assignments = {symbols[var]: (i >> j) & 1 for j, var in enumerate(reversed(variables))}
        if expr.subs(assignments):
            minterms.append(i)
    return minterms

def get_maxterms(expression, variables):
    maxterms = []
    symbols = {var: sympy.symbols(var) for var in variables}
    for var in variables:
        expression = expression.replace(f"{var}!S", f"~{var}")

    expr = sympy.sympify(expression, locals=symbols)
    total_vars = len(variables)
    for i in range(2**total_vars):
        assignments = {symbols[var]: (i >> j) & 1 for j, var in enumerate(reversed(variables))}
        if not expr.subs(assignments):
            maxterms.append(i)
    return maxterms

def minterms_to_SOP(minterms, variables):
    sop_expressions = []
    for minterm in minterms:
        terms = []
        for idx, var in enumerate(variables):
            if (minterm >> idx) & 1:
                terms.append(var)
            else:
                terms.append(f"~{var}")
        sop_expressions.append(f"({' & '.join(terms)})")
    return " | ".join(sop_expressions)

def maxterms_to_POS(maxterms, variables):
    pos_expressions = []
    for maxterm in maxterms:
        terms = []
        for idx, var in enumerate(variables):
            if (maxterm >> idx) & 1:
                terms.append(f"~{var}")
            else:
                terms.append(var)
        pos_expressions.append(f"({' | '.join(terms)})")
    return " & ".join(pos_expressions)

def minimized_SOP(expression, variables):
    # Convert string representation of variables to SymPy symbols
    symbols = {var: sympy.symbols(var) for var in variables}
    
    # Convert notations like A' to ~A
    for var in variables:
        expression = expression.replace(f"{var}'", f"~{var}")

    # Convert the string expression to a SymPy expression
    expr = sympy.sympify(expression, locals=symbols)

    # Use sympy's simplify function
    minimized_expr = sympy.simplify_logic(expr, form='dnf')

    return str(minimized_expr)

def extract_literals(expression):
    """Returns a set of all literals in the expression."""
    literals = set()
    for char in expression:
        if char.isalpha():  # Check if char is a letter (A-Z, a-z)
            literals.add(char)
    return literals

def saved_literals(original, minimized):
    original_literals = extract_literals(original)
    minimized_literals = extract_literals(minimized)
    return len(original_literals - minimized_literals)

def minimized_POS(expression, variables):
    # Convert string representation of variables to SymPy symbols
    symbols = {var: sympy.symbols(var) for var in variables}
    
    # Convert notations like A' to ~A
    for var in variables:
        expression = expression.replace(f"{var}'", f"~{var}")

    # Convert the string expression to a SymPy expression
    expr = sympy.sympify(expression, locals=symbols)

    # Use sympy's simplify function
    minimized_expr = sympy.simplify_logic(expr, form='cnf')

    return str(minimized_expr)

def write_to_file(filename, data):
    with open(filename, 'a') as f: # 'a' means append mode
        f.write(data + '\n')

def main(input_filename, output_filename):
    output_data = []

    with open(input_filename, 'r') as infile:
        for line in infile:
            expression = line.strip()
            variables = extract_variables(expression)


            # SOP
            minterms = get_minterms(expression, variables)
            sop_expression = minterms_to_SOP(minterms, variables)
            output_data.append(f"SOP: {sop_expression}")

            # POS
            maxterms = get_maxterms(expression, variables)
            pos_expression = maxterms_to_POS(maxterms, variables)
            output_data.append(f"POS: {pos_expression}")

            # Inverse SOP
            inverse_expr = f"~({expression})"
            inverse_minterms = get_minterms(inverse_expr, variables)
            inverse_sop_expression = minterms_to_SOP(inverse_minterms, variables)
            output_data.append(f"Inverse SOP: {inverse_sop_expression}")

            # Inverse POS
            inverse_maxterms = get_maxterms(inverse_expr, variables)
            inverse_pos_expression = maxterms_to_POS(inverse_maxterms, variables)
            output_data.append(f"Inverse POS: {inverse_pos_expression}")

            # Minimized SOP
            minimized_sop_expression = minimized_SOP(expression, variables)
            output_data.append(f"Minimized SOP: {minimized_sop_expression}")

            literal_savings = saved_literals(sop_expression, minimized_sop_expression)
            output_data.append(f"Saved literals (vs canonical SOP): {literal_savings}")

            # Minimized POS
            minimized_pos_expression = minimized_POS(expression, variables)
            output_data.append(f"Minimized POS: {minimized_pos_expression}")

            literal_savings_pos = saved_literals(pos_expression, minimized_pos_expression)
            output_data.append(f"Saved literals (vs canonical POS): {literal_savings_pos}")

            # Extract prime implicants and their count and add to output data
            minterms_list = get_minterms(expression, variables)
            qm = QM(len(variables), minterms_list)
            qm.run()
            epi,epi_count=qm.select()
            prime_implicants, pi_count = qm.get_prime_implicants()
            output_data.append(f"Prime Implicants: {prime_implicants}")
            output_data.append(f"Number of Prime Implicants: {pi_count}")
            output_data.append(f"Essential Prime Implicants: {epi}")
            output_data.append(f"Number of Essential Prime Implicants: {epi_count}")

            minterms = get_minterms(expression, variables)
            output_data.append(f"ON-Set minterms: {minterms}")
            output_data.append(f"Number of ON-Set minterms: {len(minterms)}")

            maxterms  = get_maxterms(expression, variables)
            output_data.append(f"ON-Set minterms: {maxterms}")
            output_data.append(f"Number of ON-Set minterms: {len(maxterms)}")



            output_data.append("\n")  # Separate line for readability

    with open(output_filename, 'w') as outfile:
        for line in output_data:
            outfile.write(line + "\n")


if __name__ == "__main__":
    main("input.eqn", "output_ENQ.txt")

