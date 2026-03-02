# dirsearch GUI

一个基于 PyQt6 的 dirsearch 图形用户界面工具，让 web 路径发现变得更加简单易用。

## 功能特性

- **直观的图形界面**：基于 PyQt6 构建，提供用户友好的图形界面
- **参数配置**：全面支持 dirsearch 的所有参数配置
- **命令预览**：实时预览将要执行的命令
- **独立窗口执行**：在独立的 CMD 窗口中执行扫描，提供原生输出体验
- **配置保存/加载**：支持保存和加载配置文件
- **标签式界面**：使用标签页组织不同类型的参数，便于查找和使用

## 安装

### 前置要求

- Python 3.9 或更高版本
- PyQt6
- dirsearch (已包含在项目中)

### 安装步骤

1. 克隆或下载此仓库
2. 确保已安装 Python 3.9+
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
   或者单独安装：
   ```bash
   pip install PyQt6 requests PySocks Jinja2 defusedxml pyOpenSSL requests-ntlm colorama ntlm-auth beautifulsoup4 mysql-connector-python psycopg[binary] defusedcsv requests-toolbelt httpx httpx-ntlm
   ```
4. 运行 GUI：
   ```bash
   python admin.py
   ```

## 使用方法

1. 运行 `python admin.py`
2. 在"目标设置"标签页中输入要扫描的目标 URL
3. 在"字典设置"标签页中配置词典文件和扩展名
4. 根据需要配置其他参数（通用设置、请求设置、连接设置等）
5. 点击"执行扫描"按钮开始扫描
6. 扫描将在独立的 CMD 窗口中运行

## 主要界面

- **目标设置**：配置扫描目标（URL、文件、CIDR 等）
- **字典设置**：配置词典文件、扩展名、前缀后缀等
- **通用设置**：配置线程数、递归扫描、状态码过滤等
- **请求设置**：配置 HTTP 方法、请求头、认证等
- **连接设置**：配置超时、代理、重试次数等
- **高级设置**：配置爬取功能
- **视图设置**：配置输出格式
- **输出设置**：配置输出文件和格式

## 配置文件

- **保存配置**：使用"保存配置"按钮将当前参数保存到 JSON 文件
- **加载配置**：使用"加载配置"按钮从 JSON 文件加载参数

## 命令预览

界面底部会显示根据当前参数生成的命令行，方便用户了解将要执行的完整命令。

## 版权信息

原始 dirsearch 工具由 Mauro Soria 开发。此 GUI 界面为第三方开发，基于原工具构建。

## 许可证

遵循原始 dirsearch 工具的 GNU General Public License v2.0 许可证。