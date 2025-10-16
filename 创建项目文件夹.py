import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime

# --- 核心逻辑区  ---
# 目录结构
SUBFOLDERS = [
    os.path.join("01_Data", "Raw", "Boundary"),
    os.path.join("01_Data", "Raw", "DEM"),
    os.path.join("01_Data", "Raw", "Imagery"),
    os.path.join("01_Data", "Raw", "Network"),
    os.path.join("01_Data", "Raw", "POI"),
    os.path.join("01_Data", "Raw", "Tabular"),
    os.path.join("01_Data", "Raw", "Misc"),
    os.path.join("01_Data", "Processed"),
    os.path.join("01_Data", "Final"),
    os.path.join("02_GIS_Project"),
    os.path.join("03_Scripts", "python"),
    os.path.join("03_Scripts", "arcpy"),
    os.path.join("04_Documents", "Literature"),
    os.path.join("04_Documents", "Reports"),
    os.path.join("04_Documents", "Meeting_Notes"),
    os.path.join("05_Outputs", "Maps"),
    os.path.join("05_Outputs", "Figures"),
    os.path.join("05_Outputs", "Tables"),
    os.path.join("06_Fieldwork", "Photos"),
    os.path.join("06_Fieldwork", "Recordings"),
    os.path.join("06_Fieldwork", "Videos"),
    os.path.join("06_Fieldwork", "Questionnaires"),
    os.path.join("06_Fieldwork", "Field_Notes")
]

# README模板
README_TEMPLATE = """# 文件夹说明: {folder_name}

## 用途 (Purpose)
- [请在这里简要说明这个文件夹存放什么内容]

## 数据来源 (Data Source)
- [如果适用，请说明数据的来源]

## 注意事项 (Notes)
- 
"""

class ProjectGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("科研项目文件夹生成器 by Siqi Miao")
        self.root.geometry("600x450")

        # --- 界面布局 (与之前版本相同) ---
        tk.Label(root, text="1. 选择基础路径 (Base Path):").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.base_path_var = tk.StringVar(value="G:/100-科研/")
        self.base_path_entry = tk.Entry(root, textvariable=self.base_path_var, width=60)
        self.base_path_entry.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Button(root, text="浏览...", command=self.browse_directory).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="2. 输入项目名称 (Project Name):").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        today_str = datetime.now().strftime('%Y%m%d')
        self.project_name_var = tk.StringVar(value=f"{today_str}_新项目名称")
        self.project_name_entry = tk.Entry(root, textvariable=self.project_name_var, width=60)
        self.project_name_entry.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.create_button = tk.Button(root, text="一键生成项目文件夹", command=self.create_project, bg="lightgreen", font=('Helvetica', 10, 'bold'))
        self.create_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        tk.Label(root, text="日志输出:").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=12, state='disabled')
        self.log_area.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.root.update_idletasks()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.base_path_var.set(directory.replace("\\", "/"))

    def create_project(self):
        base_path = self.base_path_var.get().strip()
        project_name = self.project_name_var.get().strip()
        
        if not base_path or not project_name:
            messagebox.showerror("错误", "基础路径和项目名称不能为空！")
            return
        
        if not os.path.isdir(base_path):
            messagebox.showerror("错误", f"基础路径 '{base_path}' 不存在。")
            return

        project_root = os.path.join(base_path, project_name)

        if os.path.exists(project_root):
            if not messagebox.askyesno("确认", f"项目文件夹 '{project_root}' 已存在，是否继续？"):
                return
        
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')

        self.log(f"开始创建项目 '{project_name}'...")
        self.log(f"项目根目录: {project_root}")

        try:
            # 创建主目录
            os.makedirs(project_root, exist_ok=True)

            # 循环创建所有子文件夹
            for folder_path in SUBFOLDERS:
                full_path = os.path.join(project_root, folder_path)
                os.makedirs(full_path, exist_ok=True)
                self.log(f"  -> 已创建文件夹: {folder_path}")

                # ---- 新增功能：创建readme和log文件 ----
                try:
                    # 创建 readme.txt
                    readme_path = os.path.join(full_path, "readme.txt")
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(README_TEMPLATE.format(folder_name=os.path.basename(full_path)))
                    
                    # 创建空的 log.txt
                    log_path = os.path.join(full_path, "log.txt")
                    open(log_path, 'w').close()
                    
                    self.log(f"      -> 已生成 readme.txt & log.txt")

                except Exception as e:
                    self.log(f"      -> [错误] 创建readme/log文件失败: {e}")

            self.log("\n项目目录结构已成功创建！")
            messagebox.showinfo("成功", f"项目 '{project_name}' 已成功创建！")

        except Exception as e:
            self.log(f"\n发生错误: {e}")
            messagebox.showerror("创建失败", f"创建过程中发生错误:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectGeneratorApp(root)
    root.mainloop()