# dirsearch GUI 界面设计规范

## 主题规范
- **主色**：#2196F3 (蓝色，用于按钮、标签和高亮元素)
- **辅助色**：#4CAF50 (绿色，用于成功状态和确认操作)
- **警告色**：#FF9800 (橙色，用于警告状态)
- **错误色**：#F44336 (红色，用于错误状态)
- **背景色**：#F5F5F5 (浅灰，用于主窗口背景)
- **面板色**：#FFFFFF (白色，用于面板和表单背景)
- **文字色**：#212121 (深灰，用于主要文本)
- **次级文字**：#757575 (中灰，用于次要文本)

## QSS样式表建议
```qss
/* 主窗口样式 */
QMainWindow {
    background-color: #F5F5F5;
}

/* 面板样式 */
QGroupBox {
    font-weight: bold;
    border: 2px solid #2196F3;
    border-radius: 5px;
    margin-top: 1ex;
    padding-top: 10px;
    padding-bottom: 10px;
    background-color: #FFFFFF;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    background-color: #2196F3;
    color: #FFFFFF;
}

/* 按钮样式 */
QPushButton {
    background-color: #2196F3;
    border: none;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
    min-height: 25px;
}

QPushButton:hover {
    background-color: #1E88E5;
}

QPushButton:pressed {
    background-color: #1976D2;
}

QPushButton:disabled {
    background-color: #BBDEFB;
}

/* 输入框样式 */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    border: 1px solid #BDBDBD;
    border-radius: 3px;
    padding: 5px;
    background-color: #FFFFFF;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #2196F3;
}

/* 复选框和单选框样式 */
QCheckBox, QRadioButton {
    spacing: 5px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:checked {
    background-color: #2196F3;
    border: 1px solid #1976D2;
    border-radius: 2px;
}

/* 组合框样式 */
QComboBox {
    border: 1px solid #BDBDBD;
    border-radius: 3px;
    padding: 5px;
    min-height: 25px;
}

QComboBox:focus {
    border: 2px solid #2196F3;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left: 1px solid #BDBDBD;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}

/* 标签样式 */
QLabel {
    color: #212121;
}
```

## 界面布局结构描述

### 主窗口
- **菜单栏** - 包含文件、编辑、视图、帮助菜单
- **工具栏** - 快速访问执行、停止、保存、加载等功能
- **中央部件** - 包含：
  - **参数输入区** - 滚动区域，包含所有参数输入控件，分为多个分组框
  - **控制按钮区** - 水平布局，包含执行、停止、重置按钮
  - **输出显示区** - 垂直布局，包含日志标签、输出文本框和进度条
- **状态栏** - 显示当前状态、处理进度等

### 参数输入区域布局设计

#### 1. 目标设置区 (Mandatory组)
- URL输入 (QLineEdit，支持多行输入)
- 文件输入 (QLineEdit + QPushButton 用于选择URL文件)
- 其他输入源选项 (多个QCheckBox用于选择stdin, CIDR, raw等)
- 会话选项 (QLineEdit + QPushButton 用于加载会话)

#### 2. 字典设置区 (Dictionary Settings组)
- 词典文件选择 (QLineEdit + QPushButton)
- 词典类别选择 (QComboBox多选)
- 扩展名输入 (QLineEdit)
- 词典处理选项 (多个QCheckBox)

#### 3. 通用设置区 (General Settings组)
- 线程数 (QSpinBox)
- 递归选项 (多个QCheckBox)
- 过滤选项 (状态码、大小等输入框)
- 时间限制 (QSpinBox)

#### 4. 请求设置区 (Request Settings组)
- HTTP方法 (QComboBox)
- 请求数据 (QTextEdit)
- 请求头 (QTextEdit)
- 认证设置 (QLineEdit对)
- 用户代理设置 (QLineEdit + QCheckBox)

#### 5. 连接设置区 (Connection Settings组)
- 超时设置 (QDoubleSpinBox)
- 延迟设置 (QDoubleSpinBox)
- 代理设置 (QLineEdit)
- 重试次数 (QSpinBox)

#### 6. 输出设置区 (Output Settings组)
- 输出文件 (QLineEdit + QPushButton)
- 输出格式 (QComboBox多选)
- 日志文件 (QLineEdit + QPushButton)

#### 7. 高级设置区 (Advanced Settings组)
- 爬取选项 (QCheckBox)

#### 8. 视图设置区 (View Settings组)
- 显示选项 (多个QCheckBox)

### 控制按钮区
- **执行按钮** - 启动dirsearch扫描
- **停止按钮** - 停止当前扫描
- **重置按钮** - 重置所有参数到默认值
- **保存配置按钮** - 保存当前配置
- **加载配置按钮** - 加载已保存的配置

### 输出显示区
- **实时输出标签** - 显示"扫描结果"标题
- **输出文本框** - QTextEdit，显示扫描输出
- **进度条** - 显示扫描进度

## 交互反馈设计

### 1. 参数互斥处理
- 当选中互斥参数时，自动禁用冲突参数
- 例如：选择--data-file后，--data参数被禁用

### 2. 参数依赖处理
- 当依赖参数被禁用时，依赖它的参数也被禁用
- 例如：--auth-type依赖--auth，当--auth未填写时，--auth-type被禁用

### 3. 实时预览
- 在底部显示当前配置将生成的命令行
- 随着参数的更改实时更新

### 4. 验证提示
- 输入错误时在控件旁显示错误图标和提示
- 例如：输入无效的URL时显示错误提示

### 5. 拖拽功能
- 支持拖拽文件到文件路径输入框

### 6. 快捷键
- Ctrl+E: 执行扫描
- Ctrl+S: 保存配置
- Ctrl+L: 加载配置
- Ctrl+R: 重置配置
- Ctrl+Q: 退出程序

## 信号与槽的交互逻辑

### 1. 参数值改变
- QLineEdit.textChanged, QCheckBox.stateChanged, QSpinBox.valueChanged等连接到更新命令行预览的槽函数

### 2. 按钮点击
- 执行按钮连接到执行dirsearch的槽函数
- 停止按钮连接到终止进程的槽函数

### 3. 文件选择
- QPushButton.clicked连接到QFileDialog，选择后更新相应QLineEdit

### 4. 参数联动
- 互斥参数通过QCheckBox.stateChanged信号控制其他控件的enable状态
- 依赖参数通过值变化信号动态启/禁用相关控件

### 5. 实时输出
- 扫描进程的输出通过信号发送到UI线程，更新输出文本框
- 进度信息通过信号更新进度条

## 窗口尺寸和响应式设计
- 默认窗口大小：1200x800像素
- 最小窗口大小：800x600像素
- 当窗口大小改变时，控件按比例调整位置和大小
- 使用QSplitter实现可调整的面板布局