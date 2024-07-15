import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 定义股票代码和图片路径的映射
stock_images = {
    '万润科技【002654】': {
        'bar': '002654_bar.jpg',
        'line': '002654_line.jpg',
        'pie': '002654_pie.jpg'
    },
    '中文在线【300364】': {
        'bar': '300364_bar.jpg',
        'line': '300364_line.jpg',
        'pie': '300364_pie.jpg'
    }
}

# 创建主窗口
root = tk.Tk()
root.title("情感分析图表")
root.geometry("1200x800")
# 创建字体样式，设置大小为 16
custom_font = font.Font(family="Helvetica", size=16, weight="bold")
label = tk.Label(root, text="选中你想查看的股票", font=custom_font)
label.pack(side=tk.BOTTOM)
# 创建一个matplotlib图形和画布
fig, ax = plt.subplots(figsize=(8, 6))
plt.axis('off')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# 初始化按钮列表
buttons = []


# 定义按钮点击事件处理函数
def switch_to_image(image_path):
    ax.clear()
    plt.axis('off')
    img = plt.imread(image_path)
    ax.imshow(img)
    fig.canvas.draw()


# 创建选择股票代码的下拉菜单
def stock_selected(event):
    selected_stock = stock_var.get()
    update_buttons(selected_stock)


stock_var = tk.StringVar()
stock_menu = ttk.Combobox(root, textvariable=stock_var, font=custom_font)
stock_menu['values'] = list(stock_images.keys())
stock_menu.bind('<<ComboboxSelected>>', stock_selected)
stock_menu.pack(side=tk.TOP, padx=10, pady=10)


# 更新按钮函数
def update_buttons(stock_code):
    for btn in buttons:
        btn.destroy()
    buttons.clear()
    for chart_type, image_path in stock_images[stock_code].items():
        btn = tk.Button(root, text=chart_type.capitalize(), command=lambda path=image_path: switch_to_image(path))
        btn.pack(side=tk.LEFT, padx=10, pady=10)
        buttons.append(btn)


def guigui():
    # 启动Tkinter事件循环
    root.mainloop()
