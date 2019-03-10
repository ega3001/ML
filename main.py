import numpy as np


class  MyAntResolver:
    Q = 1e11
    A = 1
    B = 2

    ants_quan = 2000  
    pher_speed = 0.03 
    len_regular_coef = 8

    def __init__(self, len_matr):
        self.len_matrix = len_matr
        self.quan_vers = len(len_matrix)
        self.pher_matrix = np.random.randint(1, 4, size=(self.quan_vers, self.quan_vers)).astype(float)

    def len_regular(self, length):
        return length ** self.len_regular_coef

    # Возвращает (Tij**A)/(Lij**B), где
    # i, j = ver1, ver2
    def get_relevance(self, ver1, ver2):
        return (self.pher_matrix[ver1][ver2] ** self.A) / (self.len_matrix[ver1][ver2] ** self.B)

    # Выбирает следующую вершину для прохода
    # :param cur_ver: текущая вепшина
    # :param past_vers: пройденные вершины
    # :return: следующая вершина
    def get_vertex(self, cur_ver, past_vers):
        gen_sum = 0
        for tmp_ver in range(self.quan_vers):
            if past_vers.count(tmp_ver) > 0:
                continue
            gen_sum += self.get_relevance(cur_ver, tmp_ver)

        prob = {}
        p_sum = 0

        for tmp_ver in range(self.quan_vers):
            if past_vers.count(tmp_ver) > 0:
                continue
            p_sum += 100 * self.get_relevance(cur_ver, tmp_ver) / gen_sum
            prob[tmp_ver] = p_sum

        rand = np.random.randint(1, 100000) / 1000.0
        for key in prob.keys():
            if rand < prob[key]:
                return key

        print("error")
        return -1

    # Имитирует проход одного муравья
    # :return: длина пути и пройденные вершины
    def cycle(self):
        way_len, t = [0, 0]
        past_vers = []
        start_ver = np.random.randint(0, self.quan_vers)
        cur_ver = start_ver
        past_vers.append(cur_ver)
        while len(past_vers) < self.quan_vers:
            next_ver = self.get_vertex(cur_ver, past_vers)

            way_len += self.len_matrix[cur_ver][next_ver]
            cur_ver = next_ver
            past_vers.append(cur_ver)

        past_vers.append(start_ver)
        way_len += self.len_matrix[cur_ver][start_ver]

        return [way_len, past_vers]

    # Имитирует проход жадного по феромонам муравья
    # :return: длина пути и пройденные вершины
    def emit_greedy_ant(self):
        way_len, t = [0, 0]
        past_vers = []
        start_ver = np.random.randint(0, self.quan_vers)
        cur_ver = start_ver
        past_vers.append(cur_ver)
        while len(past_vers) < self.quan_vers:
            pher = 0
            ver = 0
            for i in range(self.quan_vers):
                if past_vers.count(i) > 0:
                    continue
                if self.pher_matrix[cur_ver][i] > pher:
                    ver = i
                    pher = self.pher_matrix[cur_ver][i]

            next_ver = ver

            way_len += self.len_matrix[cur_ver][next_ver]
            cur_ver = next_ver
            past_vers.append(cur_ver)

        past_vers.append(start_ver)
        way_len += self.len_matrix[cur_ver][start_ver]

        return [way_len, past_vers]

    def resolve(self):
        for i in range(self.ants_quan):
            way_len, past_vers = self.cycle()

            delta_pher = self.Q / self.len_regular(way_len)

            for j in range(len(self.len_matrix)):
                self.pher_matrix[j] = [(1 - self.pher_speed) * pher for pher in self.pher_matrix[j]]

            for j in range(len(past_vers) - 1):
                self.pher_matrix[past_vers[j]][past_vers[j + 1]] += delta_pher
        return self.emit_greedy_ant()[0]


i = 0
cnt = 1
len_matrix = []
while i < cnt:
    a = list(map(int, input().split()))
    cnt = len(a)
    len_matrix.append(a)
    i += 1

obj = MyAntResolver(len_matrix)
print(obj.resolve())