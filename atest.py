import random
import tkinter as tk

# 计算k阶袋子可以兑换的奖牌数量
def get_medals_from_bag(k):
    return 2 ** (k - 1)

# 计算预期奖牌值
def calculate_expected_medals(bags, medals):
    expected = medals
    for k in range(1, 11):
        expected += bags[k] * get_medals_from_bag(k)
    return expected

class BagGame:
    def __init__(self, root):
        self.root = root
        self.root.title("袋子游戏")
        self.root.geometry("1200x600")  # 设置窗口大小为1200x600

        # 初始化变量
        self.bags = [0] * 11  # 1-10阶袋子
        self.medals = 0
        self.purchasable_medals = 0
        self.bag1_count = 45  # 默认初始1阶袋子数量
        self.purchasable_count = 88  # 默认初始可购买奖牌数量

        # 统计变量
        self.game_count = 0  # 游戏次数
        self.highest_score = 0  # 最高分数
        self.lowest_score = float('inf')  # 最低分数
        self.total_score = 0  # 总分数（用于计算平均分数）

        # 显示初始化界面
        self.show_init_screen()

    def show_init_screen(self):
        # 初始化界面
        self.init_frame = tk.Frame(self.root)
        self.init_frame.pack(pady=50)

        tk.Label(self.init_frame, text="初始化游戏", font=("Arial", 16)).pack(pady=10)

        # 1阶袋子输入
        tk.Label(self.init_frame, text="初始1阶袋子数量:", font=("Arial", 12)).pack()
        self.bag1_entry = tk.Entry(self.init_frame, font=("Arial", 12))
        self.bag1_entry.insert(0, str(self.bag1_count))  # 设置默认值
        self.bag1_entry.pack()

        # 可购买奖牌输入
        tk.Label(self.init_frame, text="初始可购买奖牌数量:", font=("Arial", 12)).pack()
        self.purchasable_entry = tk.Entry(self.init_frame, font=("Arial", 12))
        self.purchasable_entry.insert(0, str(self.purchasable_count))  # 设置默认值
        self.purchasable_entry.pack()

        # 开始游戏按钮
        tk.Button(self.init_frame, text="开始游戏", font=("Arial", 12), command=self.start_game).pack(pady=20)

    def start_game(self):
        # 获取用户输入
        try:
            self.bag1_count = int(self.bag1_entry.get())
            self.purchasable_count = int(self.purchasable_entry.get())
            if self.bag1_count < 0 or self.purchasable_count < 0:
                raise ValueError("数量不能为负数")
        except ValueError as e:
            self.show_message("错误：请输入有效的数字！")
            return

        # 初始化游戏状态
        self.bags = [0] * 11
        self.bags[1] = self.bag1_count
        self.medals = 0
        self.purchasable_medals = self.purchasable_count

        # 切换到主游戏界面
        self.init_frame.destroy()
        self.create_main_game_ui()

    def create_main_game_ui(self):
        # 主游戏界面
        # 统计信息显示区域
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.pack(anchor="nw", padx=20, pady=10)

        self.game_count_label = tk.Label(self.stats_frame, text="游戏次数: 0", font=("Arial", 12))
        self.game_count_label.pack(anchor="w")

        self.highest_score_label = tk.Label(self.stats_frame, text="最高分数: 0", font=("Arial", 12))
        self.highest_score_label.pack(anchor="w")

        self.lowest_score_label = tk.Label(self.stats_frame, text="最低分数: 0", font=("Arial", 12))
        self.lowest_score_label.pack(anchor="w")

        self.average_score_label = tk.Label(self.stats_frame, text="平均分数: 0", font=("Arial", 12))
        self.average_score_label.pack(anchor="w")

        # 显示区域
        self.status_label = tk.Label(self.root, text="当前状态：", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.bags_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.bags_label.pack()

        self.medals_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.medals_label.pack()

        self.expected_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.expected_label.pack()

        # 操作按钮（打开袋子）
        self.open_button_frame = tk.Frame(self.root)
        self.open_button_frame.pack(pady=20)

        for i in range(11):
            btn_frame = tk.Frame(self.open_button_frame)
            btn_frame.pack(side=tk.LEFT, padx=5)

            if i == 0:
                btn = tk.Button(btn_frame, text=f"兑换奖牌", command=self.exchange_all)
                btn.pack()
            else:
                btn1 = tk.Button(btn_frame, text=f"打开1个{i}阶袋", command=lambda k=i: self.open_bag(k, 1))
                btn1.pack()
                btn2 = tk.Button(btn_frame, text=f"全部打开{i}阶袋", command=lambda k=i: self.open_bag(k, "all"))
                btn2.pack()

        # 兑换高阶袋子按钮
        self.exchange_button_frame = tk.Frame(self.root)
        self.exchange_button_frame.pack(pady=20)

        for i in range(1, 11):
            btn_frame = tk.Frame(self.exchange_button_frame)
            btn_frame.pack(side=tk.LEFT, padx=5)

            btn = tk.Button(btn_frame, text=f"兑换1个{i}阶袋", command=lambda k=i: self.exchange_bag(k))
            btn.pack()

        # 重置按钮
        reset_btn = tk.Button(self.root, text="重置游戏", command=self.reset_game)
        reset_btn.pack(pady=10)

        # 操作结果显示区域
        self.message_label = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.message_label.pack(pady=20)

        # 初始化显示
        self.update_display()

    def reset_game(self):
        # 计算当前预期奖牌值
        current_score = calculate_expected_medals(self.bags, self.medals)

        # 更新统计信息
        self.game_count += 1
        self.total_score += current_score
        if current_score > self.highest_score:
            self.highest_score = current_score
        if current_score < self.lowest_score:
            self.lowest_score = current_score

        # 更新统计信息显示
        self.update_stats()

        # 重置游戏状态
        self.bags = [0] * 11
        self.bags[1] = self.bag1_count  # 使用保存的初始值
        self.medals = 0
        self.purchasable_medals = self.purchasable_count  # 使用保存的初始值
        self.update_display()
        self.show_message("游戏已重置为初始状态！")

    def update_stats(self):
        # 更新统计信息显示
        self.game_count_label.config(text=f"游戏次数: {self.game_count}")
        self.highest_score_label.config(text=f"最高分数: {self.highest_score}")
        self.lowest_score_label.config(text=f"最低分数: {self.lowest_score}")
        if self.game_count > 0:
            average_score = self.total_score / self.game_count
            self.average_score_label.config(text=f"平均分数: {average_score:.2f}")
        else:
            self.average_score_label.config(text=f"平均分数: 0")

    def update_display(self):
        # 更新显示区域
        bags_text = " | ".join([f"{i}阶袋子: {self.bags[i]}" for i in range(1, 11)])
        self.bags_label.config(text=bags_text)
        self.medals_label.config(text=f"奖牌: {self.medals} | 可购买奖牌: {self.purchasable_medals}")
        expected_medals = calculate_expected_medals(self.bags, self.medals)
        self.expected_label.config(text=f"预期奖牌值: {expected_medals}")

    def show_message(self, message):
        # 显示操作结果
        self.message_label.config(text=message)

    def exchange_all(self):
        # 兑换所有奖牌为1阶袋子
        if self.purchasable_medals <= 0 or self.medals <= 0:
            self.show_message("可购买奖牌或奖牌不足，无法兑换！")
            return

        exchange_count = min(self.purchasable_medals, self.medals)
        self.bags[1] += exchange_count
        self.purchasable_medals -= exchange_count
        self.medals -= exchange_count
        self.update_display()
        self.show_message(f"成功兑换{exchange_count}个1阶袋子！")

    def exchange_bag(self, k):
        # 兑换1个k阶袋子
        if self.bags[k] <= 0:
            self.show_message(f"{k}阶袋子数量不足，无法兑换！")
            return

        # 减去1个k阶袋子
        self.bags[k] -= 1

        # 增加奖牌
        earned_medals = get_medals_from_bag(k)
        self.medals += earned_medals

        self.update_display()
        self.show_message(f"成功兑换1个{k}阶袋子，获得{earned_medals}枚奖牌！")

    def open_bag(self, k, amount):
        # 打开袋子
        if self.bags[k] <= 0:
            self.show_message(f"{k}阶袋子数量不足！")
            return

        if amount == "all":
            total_bags = self.bags[k]
        else:
            total_bags = 1

        self.bags[k] -= total_bags
        upgraded = 0
        earned_medals = 0

        for _ in range(total_bags):
            if k < 10 and random.random() < 0.5:
                self.bags[k + 1] += 1
                upgraded += 1
            else:
                self.medals += 1
                earned_medals += 1

        self.update_display()
        self.show_message(f"打开了{total_bags}个{k}阶袋子：\n"
                         f"  - 升级为{k + 1}阶袋子: {upgraded}个\n"
                         f"  - 获得奖牌: {earned_medals}枚")

if __name__ == "__main__":
    root = tk.Tk()
    game = BagGame(root)
    root.mainloop()