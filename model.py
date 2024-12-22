import copy

from constant import *
import uuid


class People:
    def __init__(self):
        self.age: int = 0

        self.ability: list = [
            Subject("语文", VectorDescriber(-1, -1)),
            Subject("数学", VectorDescriber(1, -1)),
            Subject("物理", VectorDescriber(1, 1)),
            Subject("经济", VectorDescriber(-1, 1)),
        ]
        self.interest: list = [
            Subject("语文", VectorDescriber(-1, -1)),
            Subject("数学", VectorDescriber(1, -1)),
            Subject("物理", VectorDescriber(1, 1)),
            Subject("经济", VectorDescriber(-1, 1)),
        ]

        self.ability_num: list = []
        self.interest_num: list = []

        self.learning: learn_list = [
            Subject("语文", VectorDescriber(-1, -1)),
            Subject("数学", VectorDescriber(1, -1)),
            Subject("物理", VectorDescriber(1, 1)),
            Subject("经济", VectorDescriber(-1, 1)),
        ]

        self.choose_subject_index: list = []
        self.choose_subject = None
        self.is_creative_sub: bool = False

    def talent_generate(self):
        while True:
            t_s = np.random.dirichlet(np.ones(self.ability.__len__()), size=1)
            is_ok = True
            for o in t_s[0]:
                if 0.2 <= o <= 0.3:
                    continue
                else:
                    is_ok = False
            if is_ok:
                break
        self.ability_num = t_s[0]
        for i in range(self.ability.__len__() - 1):
            self.ability[i]: Subject
            t_ = int(t_s[0][i] * 100)
            v_ = VectorDescriber(
                self.ability[i].attr.x_weight, self.ability[i].attr.y_weight, t_
            )
            self.ability[i].upload_data(v_)
        v_ = VectorDescriber(
            self.ability[self.ability.__len__() - 1].attr.x_weight,
            self.ability[self.ability.__len__() - 1].attr.y_weight,
            int(t_s[0][self.ability.__len__() - 1] * 100),
        )
        self.ability[self.ability.__len__() - 1].upload_data(v_)
        # for i in self.ability:
        #     print(i)
        while True:
            t_s = np.random.dirichlet(np.ones(self.ability.__len__()), size=1)
            is_ok = True
            for o in t_s[0]:
                if 0.2 <= o <= 0.3:
                    continue
                else:
                    is_ok = False
            if is_ok:
                break
        self.interest_num = t_s[0]
        for i in range(self.interest.__len__() - 1):
            self.interest[i]: Subject
            t_ = int(t_s[0][i] * 100)
            v_ = VectorDescriber(
                self.interest[i].attr.x_weight, self.interest[i].attr.y_weight, t_
            )
            self.interest[i].upload_data(v_)
        v_ = VectorDescriber(
            self.interest[self.interest.__len__() - 1].attr.x_weight,
            self.interest[self.interest.__len__() - 1].attr.y_weight,
            int(t_s[0][self.interest.__len__() - 1] * 100),
        )
        self.interest[self.interest.__len__() - 1].upload_data(v_)

    def learn(self, kn: learn_list, mode: bool = False) -> bool:  # false通识,true专识
        # TODO: 让学习知识量随文明进步而进步
        if not mode:
            age_l_ability: float = age_learn(self.age)
            index: int = 0
            for k in self.learning:
                k: Subject
                a = self.ability_num[index]
                new_k = k.attr.k_weight + age_l_ability * a  # 分配学习增加
                v_ = VectorDescriber(
                    k.attr.x_weight,
                    k.attr.y_weight,
                    new_k,
                )
                k.upload_data(v_)

                # print(k.attr.k_weight)
                index += 1
        # ------------------
        # 专识教育
        # ------------------
        # TODO: 没有让非选择学科的学习参与运算，也没有限制这些的学习量不能超过总量
        else:
            age_l_ability: float = age_learn(self.age)
            if self.is_creative_sub:
                self.learning[-1].upload_data(VectorDescriber(
                    self.learning[-1].attr.x_weight, self.learning[-1].attr.y_weight, self.learning[-1].attr.k_weight +
                                                                                      c_subject_allow(age_l_ability)))
                a = age_l_ability * (1 - 0.8) / (self.learning.__len__() - 1)
                # 其余每个Subject 的k+a
                for k in self.learning:
                    if k is not self.learning[-1]:
                        new_k = k.attr.k_weight + a
                        v_ = VectorDescriber(
                            k.attr.x_weight, k.attr.y_weight, new_k
                        )
                        k.upload_data(v_)
            else:
                # 找到在civic中与person chooseSubject同名的Subject的k
                # print(self.choose_subject)
                for k in kn:
                    if k.name == self.choose_subject.name:
                        s_max = k.attr.k_weight
                        break
                for k in self.learning:
                    if k.name == self.choose_subject.name:
                        # print(normal_increase(k.attr.k_weight, age_l_ability, s_max,))
                        k.upload_data(VectorDescriber(
                            k.attr.x_weight, k.attr.y_weight, k.attr.k_weight +
                                                              normal_increase(k.attr.k_weight, age_l_ability, s_max,)))
                    else:
                        a = age_l_ability * (1 - 0.8) / (self.learning.__len__() - 1)
                        new_k = k.attr.k_weight + a
                        v_ = VectorDescriber(
                            k.attr.x_weight, k.attr.y_weight, new_k
                        )
                        k.upload_data(v_)
                # print(self.choose_subject)

        return True  # 结束

    def choose_sub(self, k: list) -> Union[None, Subject]:
        k_l: list = []
        s: list = []
        return_ = None
        return__ = None
        rechoose = False
        new_learn = self.learning
        for i in self.learning:
            i: Subject
            k_l.append(i.attr.k_weight)
            s.append(i.attr.k_weight)
        # 对s 排序
        s.sort(reverse=True)
        s = s[:2]
        if s[0] - s[1] <= 1:
            index = 0
            for i in k_l:
                if i == s[0] or i == s[1]:
                    self.choose_subject_index.append(index)
                index += 1
        else:
            index = 0
            for i in k_l:
                if i == s[0]:
                    self.choose_subject_index.append(index)
                index += 1
        # print(self.choose_subject_index)  # 写到选择科目这里，应该要根据选择基础科目的夹角来判断是不是有最近的科目选择，然后切专识
        if self.choose_subject_index.__len__() == 1:
            self.choose_subject = self.learning[self.choose_subject_index[0]]
            if random.random() > 0.5:
                rechoose = True
        else:
            # 计算夹角
            theta1 = self.learning[self.choose_subject_index[0]].theta
            theta2 = self.learning[self.choose_subject_index[1]].theta
            average = (theta1 + theta2) / 2 + random.randint(-5, 5)
            c_l = []
            for i in k:
                i: Subject
                if abs(i.theta - average) <= 30:  # 创新条件
                    if c_l.__len__() == 0:
                        c_l.append(i)
                    else:
                        if abs(i.theta - average) >= abs(c_l[0].theta - average):
                            continue
                        else:
                            c_l[0] = i
            if c_l.__len__() == 0:
                self.choose_subject = Subject(str(uuid.uuid4())[:7], VectorDescriber(
                    (self.learning[self.choose_subject_index[0]].attr.x_weight +
                     self.learning[self.choose_subject_index[1]].attr.x_weight + random.randint(-5, 5)) / 2
                    + random.randint(-5, 5),
                    (self.learning[self.choose_subject_index[0]].attr.y_weight +
                     self.learning[self.choose_subject_index[1]].attr.y_weight + random.randint(-5, 5)) / 2
                    + random.randint(-5, 5),
                    (self.learning[self.choose_subject_index[0]].attr.k_weight +
                     self.learning[self.choose_subject_index[1]].attr.k_weight) / 2
                ))
                return_ = self.choose_subject
                # new_learn.append(return_)
                # print(new_learn[-1])
            else:
                self.choose_subject = c_l[0]
        # print(self.choose_subject)
        # 选课完毕
        index = 0
        for i in k:
            try:
                have_name = self.learning[index].name
                if have_name != i.name and i is not None:
                    j = i
                    j.upload_data(VectorDescriber(i.attr.x_weight, i.attr.y_weight, random.randint(1, 10)))
                    new_learn.append(j)
            except IndexError:
                if i is not None:
                    j = i
                    j.upload_data(VectorDescriber(i.attr.x_weight, i.attr.y_weight, random.randint(1, 10)))
                    new_learn.append(j)
            finally:
                index += 1
        if return_ is not None:
            new_learn.append(return_)
            return__ = copy.copy(return_)

            self.is_creative_sub = True
        self.learning = new_learn
        if rechoose:
            t = self.learning
            random.shuffle(t)
            self.choose_subject = t[-1]
        # print(new_learn)
        # print(new_learn[-1])

        return return__


class Civic:
    def __init__(self, age: int, init_kn: learn_list, generation: int = 10):
        self.generation = generation

        self.strategy = age  # 0: 通识；1: 专识  -> 改为 通识转专识年龄
        self.knowledge: learn_list = init_kn

        self.average_point = self.knowledge[0].attr.k_weight

        # self.now_p = None  # 现在的人
        # self.now_p_rule: bool = False  # false通识,true专识
        # self.now_p_age: int = 0  # 现在的年龄
        self.p_list: list = []  # 储存people对象

    def add_person(self, person: People) -> None:
        self.p_list.append(person)
        # self.now_p: People = person
        # self.now_p_rule = False
        max_k = 0
        max_s = None
        for i in person.learning:  # 判断是不是已经超越
            if i.attr.k_weight > max_k:
                max_k = i.attr.k_weight
                max_s = i
        for i in self.knowledge:
            if i.name == max_s.name:
                i.upload_data(max_s.attr)
                break

    def return_add(self) -> float:
        add = 0
        for cy in self.knowledge:
            if add >= 25:
                add += cy.attr.k_weight
            else:
                add += cy.attr.k_weight * 10
        return float(add)

    # def develop(self, max_age: int = 50):
    #     for i in range(max_age):
    #         self.now_p_age += 1
    #         if self.now_p_rule >= self.strategy:
    #             self.now_p_rule = True
    #         else: self.now_p_rule = False
    #     if self.now_p_rule:
    #         pass
    #     else:
    #         age_l = age_learn(self.now_p_age)
    #


def run(age: int, generation: int):
    civic = Civic(age, init_learning, generation)
    max_age: int = 50
    for i in range(civic.generation):
        person = People()
        person.talent_generate()
        # print("aa")
        # print(person.learning[0])

        for j in range(max_age):
            person.age += 1
            if person.age >= civic.strategy:
                if person.age == civic.strategy:
                    # for l in person.learning:
                    #     print(l)
                    r = person.choose_sub(civic.knowledge)
                    if r is not None:
                        civic.knowledge.append(r)
                person.learn(civic.knowledge, True)
            else:
                person.learn(civic.knowledge)
                # print(person.learning[0])
        civic.add_person(person)
    return civic.return_add()
    # for i in civic.knowledge:
    #     print(i)


if __name__ == "__main__":
    r_list = []
    a_list = []
    for e in range(12):
        a_list.append(0)
    for d in range(40):
        res_list = []
        for i in range(10, 22):
            res_list.append(run(i, 100))
        print(res_list)
        r_list.append(res_list)
        for f in range(res_list.__len__()):
            a_list[f] = (a_list[f] + res_list[f]) / 2
        # if a_list == []:
        #     a_list = r_list
        # else:
        #     # 新的一项与a list里的取平均
        #     for dd in range(res_list.__len__()):
        #         print(a_list[dd])
        #         a_list[dd] = a_list[dd] + r_list[dd]
    print(r_list)
    print(a_list)
    # 保存数据
    with open("result_a.txt", "w") as f:
        for i in a_list:
            f.write(str(i) + "\n")
    with open("result_r.txt", "w") as f:
        for i in r_list:
            f.write(str(i) + "\n")


#     for i in range(self.terminal):
#         self.terminal_l.append(self.average_point)
#
# def develop(self, person: People):
#     if self.strategy == 0:
#         all_work = self.terminal * self.average_point
#         all_ability = 0
#         for i in person.ability:
#             all_ability += i
#         for i in range(self.terminal):
#             person.learning.append(int(all_work * person.ability[i] / all_ability))
#
#         index = 0
#         for i in person.learning:
#             if i > self.terminal_l[index]:
#                 self.terminal_l[index] = i
#             index += 1
#     elif self.strategy == 1:
#         pass
# if __name__ == '__main__':
#     civic1 = Civic(0)
#     for j in range(civic1.generation):
#         person_ = People(civic1.terminal)
#         # print(person_.ability)
#         civic1.develop(person_)
#         print(person_.learning)
#     print()
#     print(civic1.terminal_l)
