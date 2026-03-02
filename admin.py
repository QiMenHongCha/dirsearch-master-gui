"""
dirsearch GUI - 基于PyQt6的dirsearch工具图形界面
author: Assistant
date: 2026-03-02
"""

import sys
import subprocess
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QGroupBox, QPushButton, QLineEdit, QTextEdit, 
                             QLabel, QCheckBox, QSpinBox, QDoubleSpinBox, QComboBox, 
                             QFileDialog, QTabWidget, QSplitter, QStatusBar, QMenuBar,
                             QToolBar, QMessageBox, QProgressBar, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont, QKeySequence
import os
import json


class ParameterWidget(QWidget):
    """
    参数输入组件
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 创建滚动区域并添加到标签页
        # 目标设置标签
        target_scroll = QScrollArea()
        target_widget = QWidget()
        target_layout = QVBoxLayout(target_widget)
        target_layout.addWidget(self.create_target_group())
        target_layout.addStretch()
        target_scroll.setWidget(target_widget)
        target_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(target_scroll, "目标设置")
        
        # 字典设置标签
        dictionary_scroll = QScrollArea()
        dictionary_widget = QWidget()
        dictionary_layout = QVBoxLayout(dictionary_widget)
        dictionary_layout.addWidget(self.create_dictionary_group())
        dictionary_layout.addStretch()
        dictionary_scroll.setWidget(dictionary_widget)
        dictionary_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(dictionary_scroll, "字典设置")
        
        # 通用设置标签
        general_scroll = QScrollArea()
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)
        general_layout.addWidget(self.create_general_group())
        general_layout.addStretch()
        general_scroll.setWidget(general_widget)
        general_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(general_scroll, "通用设置")
        
        # 请求设置标签
        request_scroll = QScrollArea()
        request_widget = QWidget()
        request_layout = QVBoxLayout(request_widget)
        request_layout.addWidget(self.create_request_group())
        request_layout.addStretch()
        request_scroll.setWidget(request_widget)
        request_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(request_scroll, "请求设置")
        
        # 连接设置标签
        connection_scroll = QScrollArea()
        connection_widget = QWidget()
        connection_layout = QVBoxLayout(connection_widget)
        connection_layout.addWidget(self.create_connection_group())
        connection_layout.addStretch()
        connection_scroll.setWidget(connection_widget)
        connection_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(connection_scroll, "连接设置")
        
        # 高级设置标签
        advanced_scroll = QScrollArea()
        advanced_widget = QWidget()
        advanced_layout = QVBoxLayout(advanced_widget)
        advanced_layout.addWidget(self.create_advanced_group())
        advanced_layout.addStretch()
        advanced_scroll.setWidget(advanced_widget)
        advanced_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(advanced_scroll, "高级设置")
        
        # 视图设置标签
        view_scroll = QScrollArea()
        view_widget = QWidget()
        view_layout = QVBoxLayout(view_widget)
        view_layout.addWidget(self.create_view_group())
        view_layout.addStretch()
        view_scroll.setWidget(view_widget)
        view_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(view_scroll, "视图设置")
        
        # 输出设置标签
        output_scroll = QScrollArea()
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.addWidget(self.create_output_group())
        output_layout.addStretch()
        output_scroll.setWidget(output_widget)
        output_scroll.setWidgetResizable(True)
        self.tab_widget.addTab(output_scroll, "输出设置")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        # 初始化参数联动
        self.init_parameter_links()
    
    def create_target_group(self):
        group = QGroupBox("目标设置 (Mandatory)")
        layout = QGridLayout()
        
        # URL输入
        layout.addWidget(QLabel("目标URL:"), 0, 0)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入目标URL，多个URL用逗号分隔")
        layout.addWidget(self.url_input, 0, 1)
        
        # URL文件输入
        layout.addWidget(QLabel("URL文件:"), 1, 0)
        url_file_layout = QHBoxLayout()
        self.urls_file_input = QLineEdit()
        self.urls_file_input.setPlaceholderText("选择包含URL的文件")
        url_file_layout.addWidget(self.urls_file_input)
        url_file_btn = QPushButton("浏览...")
        url_file_btn.clicked.connect(self.browse_urls_file)
        url_file_layout.addWidget(url_file_btn)
        layout.addLayout(url_file_layout, 1, 1)
        
        # STDIN复选框
        self.stdin_checkbox = QCheckBox("从STDIN读取URL")
        layout.addWidget(self.stdin_checkbox, 2, 0, 1, 2)
        
        # CIDR输入
        layout.addWidget(QLabel("CIDR:"), 3, 0)
        self.cidr_input = QLineEdit()
        self.cidr_input.setPlaceholderText("输入CIDR，如: 192.168.1.0/24")
        layout.addWidget(self.cidr_input, 3, 1)
        
        # Raw文件输入
        raw_file_layout = QHBoxLayout()
        layout.addWidget(QLabel("Raw文件:"), 4, 0)
        self.raw_file_input = QLineEdit()
        self.raw_file_input.setPlaceholderText("输入包含原始HTTP请求的文件路径")
        raw_file_layout.addWidget(self.raw_file_input)
        raw_file_btn = QPushButton("浏览...")
        raw_file_btn.clicked.connect(self.browse_raw_file)
        raw_file_layout.addWidget(raw_file_btn)
        layout.addLayout(raw_file_layout, 4, 1)
        
        # Nmap报告输入
        nmap_layout = QHBoxLayout()
        layout.addWidget(QLabel("Nmap报告:"), 5, 0)
        self.nmap_report_input = QLineEdit()
        self.nmap_report_input.setPlaceholderText("输入Nmap报告文件路径")
        nmap_layout.addWidget(self.nmap_report_input)
        nmap_btn = QPushButton("浏览...")
        nmap_btn.clicked.connect(self.browse_nmap_file)
        nmap_layout.addWidget(nmap_btn)
        layout.addLayout(nmap_layout, 5, 1)
        
        # 会话文件输入
        session_layout = QHBoxLayout()
        layout.addWidget(QLabel("会话文件:"), 6, 0)
        self.session_file_input = QLineEdit()
        self.session_file_input.setPlaceholderText("输入会话文件路径")
        session_layout.addWidget(self.session_file_input)
        session_btn = QPushButton("浏览...")
        session_btn.clicked.connect(self.browse_session_file)
        session_layout.addWidget(session_btn)
        layout.addLayout(session_layout, 6, 1)
        
        # 配置文件输入
        config_layout = QHBoxLayout()
        layout.addWidget(QLabel("配置文件:"), 7, 0)
        self.config_file_input = QLineEdit()
        self.config_file_input.setText("")  # 默认值为空
        config_layout.addWidget(self.config_file_input)
        config_btn = QPushButton("浏览...")
        config_btn.clicked.connect(self.browse_config_file)
        config_layout.addWidget(config_btn)
        layout.addLayout(config_layout, 7, 1)
        
        group.setLayout(layout)
        return group

    def create_dictionary_group(self):
        group = QGroupBox("字典设置 (Dictionary Settings)")
        layout = QGridLayout()
        
        # 词典文件输入
        wordlist_layout = QHBoxLayout()
        layout.addWidget(QLabel("词典文件:"), 0, 0)
        self.wordlists_input = QLineEdit()
        self.wordlists_input.setPlaceholderText("输入词典文件或目录路径，多个用逗号分隔")
        wordlist_layout.addWidget(self.wordlists_input)
        wordlist_btn = QPushButton("浏览...")
        wordlist_btn.clicked.connect(self.browse_wordlist_file)
        wordlist_layout.addWidget(wordlist_btn)
        layout.addLayout(wordlist_layout, 0, 1)
        
        # 词典类别输入
        layout.addWidget(QLabel("词典类别:"), 1, 0)
        self.wordlist_categories_input = QLineEdit()
        self.wordlist_categories_input.setPlaceholderText("输入词典类别，多个用逗号分隔 (如: common,conf,web)")
        layout.addWidget(self.wordlist_categories_input, 1, 1)
        
        # 扩展名输入
        layout.addWidget(QLabel("扩展名:"), 2, 0)
        self.extensions_input = QLineEdit()
        self.extensions_input.setPlaceholderText("输入扩展名，多个用逗号分隔 (如: php,asp,html)")
        layout.addWidget(self.extensions_input, 2, 1)
        
        # 强制扩展复选框
        self.force_extensions_checkbox = QCheckBox("强制扩展名")
        layout.addWidget(self.force_extensions_checkbox, 3, 0, 1, 2)
        
        # 覆盖扩展复选框
        self.overwrite_extensions_checkbox = QCheckBox("覆盖扩展名")
        layout.addWidget(self.overwrite_extensions_checkbox, 4, 0, 1, 2)
        
        # 排除扩展输入
        layout.addWidget(QLabel("排除扩展:"), 5, 0)
        self.exclude_extensions_input = QLineEdit()
        self.exclude_extensions_input.setPlaceholderText("输入要排除的扩展名，多个用逗号分隔")
        layout.addWidget(self.exclude_extensions_input, 5, 1)
        
        # 前缀输入
        layout.addWidget(QLabel("前缀:"), 6, 0)
        self.prefixes_input = QLineEdit()
        self.prefixes_input.setPlaceholderText("输入前缀，多个用逗号分隔")
        layout.addWidget(self.prefixes_input, 6, 1)
        
        # 后缀输入
        layout.addWidget(QLabel("后缀:"), 7, 0)
        self.suffixes_input = QLineEdit()
        self.suffixes_input.setPlaceholderText("输入后缀，多个用逗号分隔")
        layout.addWidget(self.suffixes_input, 7, 1)
        
        # 移除扩展复选框
        self.remove_extensions_checkbox = QCheckBox("移除扩展名")
        layout.addWidget(self.remove_extensions_checkbox, 8, 0, 1, 2)
        
        # 大小写处理复选框
        case_layout = QHBoxLayout()
        self.uppercase_checkbox = QCheckBox("大写")
        self.lowercase_checkbox = QCheckBox("小写")
        self.capital_checkbox = QCheckBox("首字母大写")
        case_layout.addWidget(self.uppercase_checkbox)
        case_layout.addWidget(self.lowercase_checkbox)
        case_layout.addWidget(self.capital_checkbox)
        case_layout.addStretch()
        layout.addLayout(case_layout, 9, 0, 1, 2)
        
        group.setLayout(layout)
        return group

    def create_general_group(self):
        group = QGroupBox("通用设置 (General Settings)")
        layout = QGridLayout()
        
        # 线程数
        layout.addWidget(QLabel("线程数:"), 0, 0)
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setRange(1, 200)
        self.threads_spinbox.setValue(25)  # 默认值
        layout.addWidget(self.threads_spinbox, 0, 1)
        
        # 异步模式复选框
        self.async_checkbox = QCheckBox("异步模式")
        layout.addWidget(self.async_checkbox, 1, 0, 1, 2)
        
        # 递归复选框
        self.recursive_checkbox = QCheckBox("递归扫描")
        layout.addWidget(self.recursive_checkbox, 2, 0, 1, 2)
        
        # 深度递归复选框
        self.deep_recursive_checkbox = QCheckBox("深度递归扫描")
        layout.addWidget(self.deep_recursive_checkbox, 3, 0, 1, 2)
        
        # 强制递归复选框
        self.force_recursive_checkbox = QCheckBox("强制递归扫描")
        layout.addWidget(self.force_recursive_checkbox, 4, 0, 1, 2)
        
        # 最大递归深度
        layout.addWidget(QLabel("最大递归深度:"), 5, 0)
        self.max_recursion_depth_spinbox = QSpinBox()
        self.max_recursion_depth_spinbox.setRange(0, 100)
        self.max_recursion_depth_spinbox.setValue(0)
        layout.addWidget(self.max_recursion_depth_spinbox, 5, 1)
        
        # 递归状态码
        layout.addWidget(QLabel("递归状态码:"), 6, 0)
        self.recursion_status_codes_input = QLineEdit()
        self.recursion_status_codes_input.setPlaceholderText("输入状态码，支持范围，多个用逗号分隔 (如: 200-399,401)")
        layout.addWidget(self.recursion_status_codes_input, 6, 1)
        
        # 子目录
        layout.addWidget(QLabel("子目录:"), 7, 0)
        self.subdirs_input = QLineEdit()
        self.subdirs_input.setPlaceholderText("输入子目录，多个用逗号分隔 (如: /,admin/,api/)")
        layout.addWidget(self.subdirs_input, 7, 1)
        
        # 排除子目录
        layout.addWidget(QLabel("排除子目录:"), 8, 0)
        self.exclude_subdirs_input = QLineEdit()
        self.exclude_subdirs_input.setPlaceholderText("输入要排除的子目录，多个用逗号分隔")
        layout.addWidget(self.exclude_subdirs_input, 8, 1)
        
        # 包含状态码
        layout.addWidget(QLabel("包含状态码:"), 9, 0)
        self.include_status_codes_input = QLineEdit()
        self.include_status_codes_input.setPlaceholderText("输入要包含的状态码，支持范围，多个用逗号分隔")
        layout.addWidget(self.include_status_codes_input, 9, 1)
        
        # 排除状态码
        layout.addWidget(QLabel("排除状态码:"), 10, 0)
        self.exclude_status_codes_input = QLineEdit()
        self.exclude_status_codes_input.setPlaceholderText("输入要排除的状态码，支持范围，多个用逗号分隔")
        layout.addWidget(self.exclude_status_codes_input, 10, 1)
        
        # 排除大小
        layout.addWidget(QLabel("排除大小:"), 11, 0)
        self.exclude_sizes_input = QLineEdit()
        self.exclude_sizes_input.setPlaceholderText("输入要排除的响应大小，多个用逗号分隔 (如: 0B,4KB)")
        layout.addWidget(self.exclude_sizes_input, 11, 1)
        
        # 排除文本
        layout.addWidget(QLabel("排除文本:"), 12, 0)
        self.exclude_text_input = QLineEdit()
        self.exclude_text_input.setPlaceholderText("输入要排除的响应文本")
        layout.addWidget(self.exclude_text_input, 12, 1)
        
        # 排除正则
        layout.addWidget(QLabel("排除正则:"), 13, 0)
        self.exclude_regex_input = QLineEdit()
        self.exclude_regex_input.setPlaceholderText("输入要排除的响应正则表达式")
        layout.addWidget(self.exclude_regex_input, 13, 1)
        
        # 排除重定向
        layout.addWidget(QLabel("排除重定向:"), 14, 0)
        self.exclude_redirect_input = QLineEdit()
        self.exclude_redirect_input.setPlaceholderText("输入重定向匹配规则")
        layout.addWidget(self.exclude_redirect_input, 14, 1)
        
        # 排除响应
        exclude_response_layout = QHBoxLayout()
        layout.addWidget(QLabel("排除响应:"), 15, 0)
        self.exclude_response_input = QLineEdit()
        self.exclude_response_input.setPlaceholderText("输入用于排除相似响应的页面文件路径")
        exclude_response_layout.addWidget(self.exclude_response_input)
        exclude_response_btn = QPushButton("浏览...")
        exclude_response_btn.clicked.connect(self.browse_exclude_response)
        exclude_response_layout.addWidget(exclude_response_btn)
        layout.addLayout(exclude_response_layout, 15, 1)
        
        # 跳过状态码
        layout.addWidget(QLabel("跳过状态码:"), 16, 0)
        self.skip_on_status_input = QLineEdit()
        self.skip_on_status_input.setPlaceholderText("输入需要跳过目标的状态码")
        layout.addWidget(self.skip_on_status_input, 16, 1)
        
        # 最小响应大小
        layout.addWidget(QLabel("最小响应大小:"), 17, 0)
        self.min_response_size_spinbox = QSpinBox()
        self.min_response_size_spinbox.setRange(0, 1000000)
        self.min_response_size_spinbox.setValue(0)
        layout.addWidget(self.min_response_size_spinbox, 17, 1)
        
        # 最大响应大小
        layout.addWidget(QLabel("最大响应大小:"), 18, 0)
        self.max_response_size_spinbox = QSpinBox()
        self.max_response_size_spinbox.setRange(0, 1000000)
        self.max_response_size_spinbox.setValue(0)
        layout.addWidget(self.max_response_size_spinbox, 18, 1)
        
        # 最大时间
        layout.addWidget(QLabel("最大时间(秒):"), 19, 0)
        self.max_time_spinbox = QSpinBox()
        self.max_time_spinbox.setRange(0, 1000000)
        self.max_time_spinbox.setValue(0)  # 0表示无限制
        layout.addWidget(self.max_time_spinbox, 19, 1)
        
        # 退出错误复选框
        self.exit_on_error_checkbox = QCheckBox("出错时退出")
        layout.addWidget(self.exit_on_error_checkbox, 20, 0, 1, 2)
        
        group.setLayout(layout)
        return group

    def create_request_group(self):
        group = QGroupBox("请求设置 (Request Settings)")
        layout = QGridLayout()
        
        # HTTP方法
        layout.addWidget(QLabel("HTTP方法:"), 0, 0)
        self.http_method_combobox = QComboBox()
        self.http_method_combobox.addItems(["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE", "PATCH"])
        self.http_method_combobox.setCurrentText("GET")
        layout.addWidget(self.http_method_combobox, 0, 1)
        
        # 请求数据
        layout.addWidget(QLabel("请求数据:"), 1, 0)
        self.data_input = QTextEdit()
        self.data_input.setMaximumHeight(60)
        self.data_input.setPlaceholderText("输入HTTP请求数据")
        layout.addWidget(self.data_input, 1, 1)
        
        # 数据文件
        data_file_layout = QHBoxLayout()
        layout.addWidget(QLabel("数据文件:"), 2, 0)
        self.data_file_input = QLineEdit()
        self.data_file_input.setPlaceholderText("输入包含HTTP请求数据的文件路径")
        data_file_layout.addWidget(self.data_file_input)
        data_file_btn = QPushButton("浏览...")
        data_file_btn.clicked.connect(self.browse_data_file)
        data_file_layout.addWidget(data_file_btn)
        layout.addLayout(data_file_layout, 2, 1)
        
        # 请求头
        layout.addWidget(QLabel("请求头:"), 3, 0)
        self.headers_input = QTextEdit()
        self.headers_input.setMaximumHeight(80)
        self.headers_input.setPlaceholderText("输入HTTP请求头，每行一个 (如: User-Agent: ...)")
        layout.addWidget(self.headers_input, 3, 1)
        
        # 请求头文件
        headers_file_layout = QHBoxLayout()
        layout.addWidget(QLabel("请求头文件:"), 4, 0)
        self.headers_file_input = QLineEdit()
        self.headers_file_input.setPlaceholderText("输入包含HTTP请求头的文件路径")
        headers_file_layout.addWidget(self.headers_file_input)
        headers_file_btn = QPushButton("浏览...")
        headers_file_btn.clicked.connect(self.browse_headers_file)
        headers_file_layout.addWidget(headers_file_btn)
        layout.addLayout(headers_file_layout, 4, 1)
        
        # 跟随重定向复选框
        self.follow_redirects_checkbox = QCheckBox("跟随重定向")
        layout.addWidget(self.follow_redirects_checkbox, 5, 0, 1, 2)
        
        # 随机代理复选框
        self.random_agent_checkbox = QCheckBox("随机User-Agent")
        layout.addWidget(self.random_agent_checkbox, 6, 0, 1, 2)
        
        # 认证
        layout.addWidget(QLabel("认证:"), 7, 0)
        self.auth_input = QLineEdit()
        self.auth_input.setPlaceholderText("输入认证信息 (如: user:password)")
        layout.addWidget(self.auth_input, 7, 1)
        
        # 认证类型
        layout.addWidget(QLabel("认证类型:"), 8, 0)
        self.auth_type_combobox = QComboBox()
        self.auth_type_combobox.addItems(["", "basic", "digest", "bearer", "ntlm", "jwt"])
        layout.addWidget(self.auth_type_combobox, 8, 1)
        
        # 证书文件
        cert_layout = QHBoxLayout()
        layout.addWidget(QLabel("证书文件:"), 9, 0)
        self.cert_file_input = QLineEdit()
        self.cert_file_input.setPlaceholderText("输入客户端证书文件路径")
        cert_layout.addWidget(self.cert_file_input)
        cert_btn = QPushButton("浏览...")
        cert_btn.clicked.connect(self.browse_cert_file)
        cert_layout.addWidget(cert_btn)
        layout.addLayout(cert_layout, 9, 1)
        
        # 密钥文件
        key_layout = QHBoxLayout()
        layout.addWidget(QLabel("密钥文件:"), 10, 0)
        self.key_file_input = QLineEdit()
        self.key_file_input.setPlaceholderText("输入客户端证书私钥文件路径")
        key_layout.addWidget(self.key_file_input)
        key_btn = QPushButton("浏览...")
        key_btn.clicked.connect(self.browse_key_file)
        key_layout.addWidget(key_btn)
        layout.addLayout(key_layout, 10, 1)
        
        # User-Agent
        layout.addWidget(QLabel("User-Agent:"), 11, 0)
        self.user_agent_input = QLineEdit()
        self.user_agent_input.setPlaceholderText("输入User-Agent字符串")
        layout.addWidget(self.user_agent_input, 11, 1)
        
        # Cookie
        layout.addWidget(QLabel("Cookie:"), 12, 0)
        self.cookie_input = QLineEdit()
        self.cookie_input.setPlaceholderText("输入Cookie字符串")
        layout.addWidget(self.cookie_input, 12, 1)
        
        group.setLayout(layout)
        return group

    def create_connection_group(self):
        group = QGroupBox("连接设置 (Connection Settings)")
        layout = QGridLayout()
        
        # 超时
        layout.addWidget(QLabel("超时(秒):"), 0, 0)
        self.timeout_spinbox = QDoubleSpinBox()
        self.timeout_spinbox.setRange(0.1, 100.0)
        self.timeout_spinbox.setSingleStep(0.5)
        self.timeout_spinbox.setValue(7.5)
        layout.addWidget(self.timeout_spinbox, 0, 1)
        
        # 延迟
        layout.addWidget(QLabel("延迟(秒):"), 1, 0)
        self.delay_spinbox = QDoubleSpinBox()
        self.delay_spinbox.setRange(0.0, 100.0)
        self.delay_spinbox.setSingleStep(0.1)
        self.delay_spinbox.setValue(0.0)
        layout.addWidget(self.delay_spinbox, 1, 1)
        
        # 代理
        layout.addWidget(QLabel("代理:"), 2, 0)
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("输入代理URL，多个用逗号分隔 (如: http://proxy:8080)")
        layout.addWidget(self.proxy_input, 2, 1)
        
        # 代理文件
        proxy_file_layout = QHBoxLayout()
        layout.addWidget(QLabel("代理文件:"), 3, 0)
        self.proxies_file_input = QLineEdit()
        self.proxies_file_input.setPlaceholderText("输入包含代理服务器的文件路径")
        proxy_file_layout.addWidget(self.proxies_file_input)
        proxy_file_btn = QPushButton("浏览...")
        proxy_file_btn.clicked.connect(self.browse_proxies_file)
        proxy_file_layout.addWidget(proxy_file_btn)
        layout.addLayout(proxy_file_layout, 3, 1)
        
        # 代理认证
        layout.addWidget(QLabel("代理认证:"), 4, 0)
        self.proxy_auth_input = QLineEdit()
        self.proxy_auth_input.setPlaceholderText("输入代理认证信息")
        layout.addWidget(self.proxy_auth_input, 4, 1)
        
        # 重放代理
        layout.addWidget(QLabel("重放代理:"), 5, 0)
        self.replay_proxy_input = QLineEdit()
        self.replay_proxy_input.setPlaceholderText("输入用于重放路径的代理")
        layout.addWidget(self.replay_proxy_input, 5, 1)
        
        # TOR复选框
        self.tor_checkbox = QCheckBox("使用TOR网络")
        layout.addWidget(self.tor_checkbox, 6, 0, 1, 2)
        
        # 协议
        layout.addWidget(QLabel("协议:"), 7, 0)
        self.scheme_combobox = QComboBox()
        self.scheme_combobox.addItems(["", "http", "https"])
        layout.addWidget(self.scheme_combobox, 7, 1)
        
        # 最大速率
        layout.addWidget(QLabel("最大速率:"), 8, 0)
        self.max_rate_spinbox = QSpinBox()
        self.max_rate_spinbox.setRange(0, 10000)
        self.max_rate_spinbox.setValue(0)  # 0表示无限制
        layout.addWidget(self.max_rate_spinbox, 8, 1)
        
        # 重试次数
        layout.addWidget(QLabel("重试次数:"), 9, 0)
        self.retries_spinbox = QSpinBox()
        self.retries_spinbox.setRange(0, 20)
        self.retries_spinbox.setValue(1)
        layout.addWidget(self.retries_spinbox, 9, 1)
        
        # IP地址
        layout.addWidget(QLabel("IP地址:"), 10, 0)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("输入服务器IP地址")
        layout.addWidget(self.ip_input, 10, 1)
        
        # 网络接口
        layout.addWidget(QLabel("网络接口:"), 11, 0)
        self.interface_input = QLineEdit()
        self.interface_input.setPlaceholderText("输入网络接口名称")
        layout.addWidget(self.interface_input, 11, 1)
        
        group.setLayout(layout)
        return group

    def create_advanced_group(self):
        group = QGroupBox("高级设置 (Advanced Settings)")
        layout = QVBoxLayout()
        
        # 爬取复选框
        self.crawl_checkbox = QCheckBox("爬取响应中的新路径")
        layout.addWidget(self.crawl_checkbox)
        
        group.setLayout(layout)
        return group

    def create_view_group(self):
        group = QGroupBox("视图设置 (View Settings)")
        layout = QGridLayout()
        
        # 完整URL复选框
        self.full_url_checkbox = QCheckBox("显示完整URL")
        layout.addWidget(self.full_url_checkbox, 0, 0)
        
        # 重定向历史复选框
        self.redirects_history_checkbox = QCheckBox("显示重定向历史")
        layout.addWidget(self.redirects_history_checkbox, 0, 1)
        
        # 无颜色复选框
        self.no_color_checkbox = QCheckBox("无颜色输出")
        layout.addWidget(self.no_color_checkbox, 1, 0)
        
        # 安静模式复选框
        self.quiet_mode_checkbox = QCheckBox("安静模式")
        layout.addWidget(self.quiet_mode_checkbox, 1, 1)
        
        # 禁用CLI复选框
        self.disable_cli_checkbox = QCheckBox("禁用CLI输出")
        layout.addWidget(self.disable_cli_checkbox, 2, 0, 1, 2)
        
        group.setLayout(layout)
        return group

    def create_output_group(self):
        group = QGroupBox("输出设置 (Output Settings)")
        layout = QGridLayout()
        
        # 输出格式
        layout.addWidget(QLabel("输出格式:"), 0, 0)
        self.output_formats_input = QLineEdit()
        self.output_formats_input.setPlaceholderText("输入输出格式，多个用逗号分隔 (如: simple,plain,json)")
        layout.addWidget(self.output_formats_input, 0, 1)
        
        # 输出文件
        output_file_layout = QHBoxLayout()
        layout.addWidget(QLabel("输出文件:"), 1, 0)
        self.output_file_input = QLineEdit()
        self.output_file_input.setPlaceholderText("输入输出文件路径")
        output_file_layout.addWidget(self.output_file_input)
        output_file_btn = QPushButton("浏览...")
        output_file_btn.clicked.connect(self.browse_output_file)
        output_file_layout.addWidget(output_file_btn)
        layout.addLayout(output_file_layout, 1, 1)
        
        # MySQL URL
        layout.addWidget(QLabel("MySQL URL:"), 2, 0)
        self.mysql_url_input = QLineEdit()
        self.mysql_url_input.setPlaceholderText("输入MySQL数据库URL")
        layout.addWidget(self.mysql_url_input, 2, 1)
        
        # PostgreSQL URL
        layout.addWidget(QLabel("PostgreSQL URL:"), 3, 0)
        self.postgres_url_input = QLineEdit()
        self.postgres_url_input.setPlaceholderText("输入PostgreSQL数据库URL")
        layout.addWidget(self.postgres_url_input, 3, 1)
        
        # 日志文件
        log_file_layout = QHBoxLayout()
        layout.addWidget(QLabel("日志文件:"), 4, 0)
        self.log_file_input = QLineEdit()
        self.log_file_input.setPlaceholderText("输入日志文件路径")
        log_file_layout.addWidget(self.log_file_input)
        log_file_btn = QPushButton("浏览...")
        log_file_btn.clicked.connect(self.browse_log_file)
        log_file_layout.addWidget(log_file_btn)
        layout.addLayout(log_file_layout, 4, 1)
        
        group.setLayout(layout)
        return group

    def init_parameter_links(self):
        """
        初始化参数联动，处理互斥和依赖关系
        """
        # 互斥参数联动
        self.urls_file_input.textChanged.connect(self.handle_urls_file_change)
        self.stdin_checkbox.stateChanged.connect(self.handle_stdin_change)
        self.cidr_input.textChanged.connect(self.handle_cidr_change)
        self.raw_file_input.textChanged.connect(self.handle_raw_file_change)
        self.nmap_report_input.textChanged.connect(self.handle_nmap_change)
        
        # 依赖参数联动
        self.auth_input.textChanged.connect(self.handle_auth_change)
        self.auth_type_combobox.currentTextChanged.connect(self.handle_auth_type_change)
        
        # 其他联动
        self.force_extensions_checkbox.stateChanged.connect(self.handle_force_ext_change)
        self.overwrite_extensions_checkbox.stateChanged.connect(self.handle_overwrite_ext_change)
        self.remove_extensions_checkbox.stateChanged.connect(self.handle_remove_ext_change)
        self.tor_checkbox.stateChanged.connect(self.handle_tor_change)
        self.random_agent_checkbox.stateChanged.connect(self.handle_random_agent_change)

    def handle_urls_file_change(self):
        if self.urls_file_input.text():
            self.url_input.setEnabled(False)
            self.stdin_checkbox.setChecked(False)
            self.stdin_checkbox.setEnabled(False)
            self.cidr_input.setEnabled(False)
            self.raw_file_input.setEnabled(False)
            self.nmap_report_input.setEnabled(False)
        else:
            self.url_input.setEnabled(True)
            self.stdin_checkbox.setEnabled(True)
            self.cidr_input.setEnabled(True)
            self.raw_file_input.setEnabled(True)
            self.nmap_report_input.setEnabled(True)

    def handle_stdin_change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.url_input.setEnabled(False)
            self.urls_file_input.setEnabled(False)
            self.cidr_input.setEnabled(False)
            self.raw_file_input.setEnabled(False)
            self.nmap_report_input.setEnabled(False)
        else:
            self.url_input.setEnabled(True)
            self.urls_file_input.setEnabled(True)
            self.cidr_input.setEnabled(True)
            self.raw_file_input.setEnabled(True)
            self.nmap_report_input.setEnabled(True)

    def handle_cidr_change(self):
        if self.cidr_input.text():
            self.url_input.setEnabled(False)
            self.urls_file_input.setEnabled(False)
            self.stdin_checkbox.setChecked(False)
            self.stdin_checkbox.setEnabled(False)
            self.raw_file_input.setEnabled(False)
            self.nmap_report_input.setEnabled(False)
        else:
            self.url_input.setEnabled(True)
            self.urls_file_input.setEnabled(True)
            self.stdin_checkbox.setEnabled(True)
            self.raw_file_input.setEnabled(True)
            self.nmap_report_input.setEnabled(True)

    def handle_raw_file_change(self):
        if self.raw_file_input.text():
            self.url_input.setEnabled(False)
            self.urls_file_input.setEnabled(False)
            self.stdin_checkbox.setChecked(False)
            self.stdin_checkbox.setEnabled(False)
            self.cidr_input.setEnabled(False)
            self.nmap_report_input.setEnabled(False)
        else:
            self.url_input.setEnabled(True)
            self.urls_file_input.setEnabled(True)
            self.stdin_checkbox.setEnabled(True)
            self.cidr_input.setEnabled(True)
            self.nmap_report_input.setEnabled(True)

    def handle_nmap_change(self):
        if self.nmap_report_input.text():
            self.url_input.setEnabled(False)
            self.urls_file_input.setEnabled(False)
            self.stdin_checkbox.setChecked(False)
            self.stdin_checkbox.setEnabled(False)
            self.cidr_input.setEnabled(False)
            self.raw_file_input.setEnabled(False)
        else:
            self.url_input.setEnabled(True)
            self.urls_file_input.setEnabled(True)
            self.stdin_checkbox.setEnabled(True)
            self.cidr_input.setEnabled(True)
            self.raw_file_input.setEnabled(True)

    def handle_auth_change(self):
        if self.auth_input.text():
            self.auth_type_combobox.setEnabled(True)
        else:
            self.auth_type_combobox.setEnabled(False)
            self.auth_type_combobox.setCurrentIndex(0)

    def handle_auth_type_change(self, text):
        if text and not self.auth_input.text():
            # 如果选择了认证类型但没有认证信息，给用户提示
            reply = QMessageBox.question(self, '认证信息', 
                                         '您选择了认证类型但未输入认证信息，是否要输入认证信息？',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # 这里可以弹出输入框，暂时跳过
                pass

    def handle_force_ext_change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.remove_extensions_checkbox.setChecked(False)

    def handle_overwrite_ext_change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.remove_extensions_checkbox.setChecked(False)

    def handle_remove_ext_change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.force_extensions_checkbox.setChecked(False)
            self.overwrite_extensions_checkbox.setChecked(False)

    def handle_tor_change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.proxy_input.setEnabled(False)
        else:
            self.proxy_input.setEnabled(True)

    def handle_random_agent_change(self, state):
        if state == Qt.CheckState.Checked.value:
            self.user_agent_input.setEnabled(False)
        else:
            self.user_agent_input.setEnabled(True)

    # 文件浏览方法
    def browse_urls_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择URL文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.urls_file_input.setText(file_path)

    def browse_raw_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Raw文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.raw_file_input.setText(file_path)

    def browse_nmap_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Nmap报告", "", "XML Files (*.xml);;All Files (*)")
        if file_path:
            self.nmap_report_input.setText(file_path)

    def browse_session_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择会话文件", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.session_file_input.setText(file_path)

    def browse_config_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择配置文件", "", "Config Files (*.ini);;All Files (*)")
        if file_path:
            self.config_file_input.setText(file_path)

    def browse_wordlist_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择词典文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.wordlists_input.setText(file_path)

    def browse_exclude_response(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择排除响应文件", "", "All Files (*)")
        if file_path:
            self.exclude_response_input.setText(file_path)

    def browse_data_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", "All Files (*)")
        if file_path:
            self.data_file_input.setText(file_path)

    def browse_headers_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择请求头文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.headers_file_input.setText(file_path)

    def browse_cert_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择证书文件", "", "All Files (*)")
        if file_path:
            self.cert_file_input.setText(file_path)

    def browse_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择密钥文件", "", "All Files (*)")
        if file_path:
            self.key_file_input.setText(file_path)

    def browse_proxies_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择代理文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.proxies_file_input.setText(file_path)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "选择输出文件", "", "All Files (*)")
        if file_path:
            self.output_file_input.setText(file_path)

    def browse_log_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "选择日志文件", "", "Log Files (*.log);;Text Files (*.txt);;All Files (*)")
        if file_path:
            self.log_file_input.setText(file_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('dirsearch GUI')
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
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
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
                border: 1px solid #BDBDBD;
                border-radius: 3px;
                padding: 5px;
                background-color: #FFFFFF;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #2196F3;
            }
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
            QLabel {
                color: #212121;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 参数输入区域
        self.param_widget = ParameterWidget()
        
        # 控制按钮区域
        control_layout = QHBoxLayout()
        
        self.run_button = QPushButton('执行扫描')
        self.run_button.clicked.connect(self.run_dirsearch)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        control_layout.addWidget(self.run_button)
        
        self.stop_button = QPushButton('停止扫描')
        self.stop_button.clicked.connect(self.stop_dirsearch)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        control_layout.addWidget(self.stop_button)
        
        self.reset_button = QPushButton('重置参数')
        self.reset_button.clicked.connect(self.reset_parameters)
        control_layout.addWidget(self.reset_button)
        
        self.save_config_button = QPushButton('保存配置')
        self.save_config_button.clicked.connect(self.save_config)
        control_layout.addWidget(self.save_config_button)
        
        self.load_config_button = QPushButton('加载配置')
        self.load_config_button.clicked.connect(self.load_config)
        control_layout.addWidget(self.load_config_button)
        
        control_layout.addStretch()
        
        # 命令行预览
        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(QLabel("命令行预览:"))
        self.cmd_preview = QLineEdit()
        self.cmd_preview.setReadOnly(True)
        self.cmd_preview.setStyleSheet("QLineEdit { background-color: #E3F2FD; font-family: 'Courier New'; }")
        cmd_layout.addWidget(self.cmd_preview)
        
        # 更新命令预览的定时器
        self.cmd_update_timer = QTimer()
        self.cmd_update_timer.timeout.connect(self.update_command_preview)
        self.cmd_update_timer.start(1000)  # 每秒更新一次
        

        
        # 添加到主布局
        main_layout.addWidget(self.param_widget)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(cmd_layout)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.statusBar().showMessage('就绪')
        
        # 更新命令预览
        self.update_command_preview()

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        save_action = QAction('保存配置', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_config)
        file_menu.addAction(save_action)
        
        load_action = QAction('加载配置', self)
        load_action.setShortcut(QKeySequence.StandardKey.Open)
        load_action.triggered.connect(self.load_config)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 操作菜单
        action_menu = menubar.addMenu('操作')
        
        run_action = QAction('执行扫描', self)
        run_action.setShortcut(QKeySequence("Ctrl+E"))
        run_action.triggered.connect(self.run_dirsearch)
        action_menu.addAction(run_action)
        
        stop_action = QAction('停止扫描', self)
        stop_action.setShortcut(QKeySequence("Ctrl+T"))
        stop_action.triggered.connect(self.stop_dirsearch)
        action_menu.addAction(stop_action)
        
        reset_action = QAction('重置参数', self)
        reset_action.setShortcut(QKeySequence("Ctrl+R"))
        reset_action.triggered.connect(self.reset_parameters)
        action_menu.addAction(reset_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        toolbar = self.addToolBar('工具')
        
        run_action = QAction('执行', self)
        run_action.triggered.connect(self.run_dirsearch)
        toolbar.addAction(run_action)
        
        stop_action = QAction('停止', self)
        stop_action.triggered.connect(self.stop_dirsearch)
        stop_action.setEnabled(False)
        self.stop_toolbar_action = stop_action
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        save_action = QAction('保存配置', self)
        save_action.triggered.connect(self.save_config)
        toolbar.addAction(save_action)
        
        load_action = QAction('加载配置', self)
        load_action.triggered.connect(self.load_config)
        toolbar.addAction(load_action)

    def update_command_preview(self):
        """
        更新命令行预览
        """
        cmd_parts = ["python dirsearch.py"]
        
        # 添加URL参数
        if self.param_widget.url_input.text():
            urls = [url.strip() for url in self.param_widget.url_input.text().split(',')]
            for url in urls:
                if url:
                    cmd_parts.append(f"-u {url}")
        
        # 添加URLs文件参数
        if self.param_widget.urls_file_input.text():
            cmd_parts.append(f"-l {self.param_widget.urls_file_input.text()}")
        
        # 添加STDIN参数
        if self.param_widget.stdin_checkbox.isChecked():
            cmd_parts.append("--stdin")
        
        # 添加CIDR参数
        if self.param_widget.cidr_input.text():
            cmd_parts.append(f"--cidr {self.param_widget.cidr_input.text()}")
        
        # 添加Raw文件参数
        if self.param_widget.raw_file_input.text():
            cmd_parts.append(f"--raw {self.param_widget.raw_file_input.text()}")
        
        # 添加Nmap报告参数
        if self.param_widget.nmap_report_input.text():
            cmd_parts.append(f"--nmap-report {self.param_widget.nmap_report_input.text()}")
        
        # 添加会话参数
        if self.param_widget.session_file_input.text():
            cmd_parts.append(f"-s {self.param_widget.session_file_input.text()}")
        
        # 添加配置文件参数
        if self.param_widget.config_file_input.text():
            cmd_parts.append(f"--config {self.param_widget.config_file_input.text()}")
        
        # 添加词典参数
        if self.param_widget.wordlists_input.text():
            cmd_parts.append(f"-w {self.param_widget.wordlists_input.text()}")
        
        if self.param_widget.wordlist_categories_input.text():
            cmd_parts.append(f"--wordlist-categories {self.param_widget.wordlist_categories_input.text()}")
        
        if self.param_widget.extensions_input.text():
            cmd_parts.append(f"-e {self.param_widget.extensions_input.text()}")
        
        if self.param_widget.force_extensions_checkbox.isChecked():
            cmd_parts.append("-f")
        
        if self.param_widget.overwrite_extensions_checkbox.isChecked():
            cmd_parts.append("--overwrite-extensions")
        
        if self.param_widget.remove_extensions_checkbox.isChecked():
            cmd_parts.append("--remove-extensions")
        
        if self.param_widget.exclude_extensions_input.text():
            cmd_parts.append(f"--exclude-extensions {self.param_widget.exclude_extensions_input.text()}")
        
        if self.param_widget.prefixes_input.text():
            cmd_parts.append(f"--prefixes {self.param_widget.prefixes_input.text()}")
        
        if self.param_widget.suffixes_input.text():
            cmd_parts.append(f"--suffixes {self.param_widget.suffixes_input.text()}")
        
        if self.param_widget.uppercase_checkbox.isChecked():
            cmd_parts.append("-U")
        
        if self.param_widget.lowercase_checkbox.isChecked():
            cmd_parts.append("-L")
        
        if self.param_widget.capital_checkbox.isChecked():
            cmd_parts.append("-C")
        
        # 添加通用参数
        if self.param_widget.threads_spinbox.value() != 25:
            cmd_parts.append(f"-t {self.param_widget.threads_spinbox.value()}")
        
        if self.param_widget.async_checkbox.isChecked():
            cmd_parts.append("--async")
        
        if self.param_widget.recursive_checkbox.isChecked():
            cmd_parts.append("-r")
        
        if self.param_widget.deep_recursive_checkbox.isChecked():
            cmd_parts.append("--deep-recursive")
        
        if self.param_widget.force_recursive_checkbox.isChecked():
            cmd_parts.append("--force-recursive")
        
        if self.param_widget.max_recursion_depth_spinbox.value() > 0:
            cmd_parts.append(f"-R {self.param_widget.max_recursion_depth_spinbox.value()}")
        
        if self.param_widget.recursion_status_codes_input.text():
            cmd_parts.append(f"--recursion-status {self.param_widget.recursion_status_codes_input.text()}")
        
        if self.param_widget.subdirs_input.text():
            cmd_parts.append(f"--subdirs {self.param_widget.subdirs_input.text()}")
        
        if self.param_widget.exclude_subdirs_input.text():
            cmd_parts.append(f"--exclude-subdirs {self.param_widget.exclude_subdirs_input.text()}")
        
        if self.param_widget.include_status_codes_input.text():
            cmd_parts.append(f"-i {self.param_widget.include_status_codes_input.text()}")
        
        if self.param_widget.exclude_status_codes_input.text():
            cmd_parts.append(f"-x {self.param_widget.exclude_status_codes_input.text()}")
        
        if self.param_widget.exclude_sizes_input.text():
            cmd_parts.append(f"--exclude-sizes {self.param_widget.exclude_sizes_input.text()}")
        
        if self.param_widget.exclude_text_input.text():
            cmd_parts.append(f"--exclude-text {self.param_widget.exclude_text_input.text()}")
        
        if self.param_widget.exclude_regex_input.text():
            cmd_parts.append(f"--exclude-regex {self.param_widget.exclude_regex_input.text()}")
        
        if self.param_widget.exclude_redirect_input.text():
            cmd_parts.append(f"--exclude-redirect {self.param_widget.exclude_redirect_input.text()}")
        
        if self.param_widget.exclude_response_input.text():
            cmd_parts.append(f"--exclude-response {self.param_widget.exclude_response_input.text()}")
        
        if self.param_widget.skip_on_status_input.text():
            cmd_parts.append(f"--skip-on-status {self.param_widget.skip_on_status_input.text()}")
        
        if self.param_widget.min_response_size_spinbox.value() > 0:
            cmd_parts.append(f"--min-response-size {self.param_widget.min_response_size_spinbox.value()}")
        
        if self.param_widget.max_response_size_spinbox.value() > 0:
            cmd_parts.append(f"--max-response-size {self.param_widget.max_response_size_spinbox.value()}")
        
        if self.param_widget.max_time_spinbox.value() > 0:
            cmd_parts.append(f"--max-time {self.param_widget.max_time_spinbox.value()}")
        
        if self.param_widget.exit_on_error_checkbox.isChecked():
            cmd_parts.append("--exit-on-error")
        
        # 添加请求参数
        if self.param_widget.http_method_combobox.currentText() != "GET":
            cmd_parts.append(f"-m {self.param_widget.http_method_combobox.currentText()}")
        
        if self.param_widget.data_input.toPlainText():
            cmd_parts.append(f"-d '{self.param_widget.data_input.toPlainText()}'")
        
        if self.param_widget.data_file_input.text():
            cmd_parts.append(f"--data-file {self.param_widget.data_file_input.text()}")
        
        headers = self.param_widget.headers_input.toPlainText()
        if headers:
            for header in headers.split('\n'):
                if header.strip():
                    cmd_parts.append(f"-H '{header.strip()}'")
        
        if self.param_widget.headers_file_input.text():
            cmd_parts.append(f"--headers-file {self.param_widget.headers_file_input.text()}")
        
        if self.param_widget.follow_redirects_checkbox.isChecked():
            cmd_parts.append("-F")
        
        if self.param_widget.random_agent_checkbox.isChecked():
            cmd_parts.append("--random-agent")
        
        if self.param_widget.auth_input.text():
            cmd_parts.append(f"--auth {self.param_widget.auth_input.text()}")
        
        if self.param_widget.auth_type_combobox.currentText():
            cmd_parts.append(f"--auth-type {self.param_widget.auth_type_combobox.currentText()}")
        
        if self.param_widget.cert_file_input.text():
            cmd_parts.append(f"--cert-file {self.param_widget.cert_file_input.text()}")
        
        if self.param_widget.key_file_input.text():
            cmd_parts.append(f"--key-file {self.param_widget.key_file_input.text()}")
        
        if self.param_widget.user_agent_input.text():
            cmd_parts.append(f"--user-agent '{self.param_widget.user_agent_input.text()}'")
        
        if self.param_widget.cookie_input.text():
            cmd_parts.append(f"--cookie '{self.param_widget.cookie_input.text()}'")
        
        # 添加连接参数
        if self.param_widget.timeout_spinbox.value() != 7.5:
            cmd_parts.append(f"--timeout {self.param_widget.timeout_spinbox.value()}")
        
        if self.param_widget.delay_spinbox.value() > 0:
            cmd_parts.append(f"--delay {self.param_widget.delay_spinbox.value()}")
        
        if self.param_widget.proxy_input.text():
            proxies = [proxy.strip() for proxy in self.param_widget.proxy_input.text().split(',')]
            for proxy in proxies:
                if proxy:
                    cmd_parts.append(f"-p {proxy}")
        
        if self.param_widget.proxies_file_input.text():
            cmd_parts.append(f"--proxies-file {self.param_widget.proxies_file_input.text()}")
        
        if self.param_widget.proxy_auth_input.text():
            cmd_parts.append(f"--proxy-auth {self.param_widget.proxy_auth_input.text()}")
        
        if self.param_widget.replay_proxy_input.text():
            cmd_parts.append(f"--replay-proxy {self.param_widget.replay_proxy_input.text()}")
        
        if self.param_widget.tor_checkbox.isChecked():
            cmd_parts.append("--tor")
        
        if self.param_widget.scheme_combobox.currentText():
            cmd_parts.append(f"--scheme {self.param_widget.scheme_combobox.currentText()}")
        
        if self.param_widget.max_rate_spinbox.value() > 0:
            cmd_parts.append(f"--max-rate {self.param_widget.max_rate_spinbox.value()}")
        
        if self.param_widget.retries_spinbox.value() != 1:
            cmd_parts.append(f"--retries {self.param_widget.retries_spinbox.value()}")
        
        if self.param_widget.ip_input.text():
            cmd_parts.append(f"--ip {self.param_widget.ip_input.text()}")
        
        if self.param_widget.interface_input.text():
            cmd_parts.append(f"--interface {self.param_widget.interface_input.text()}")
        
        # 添加高级参数
        if self.param_widget.crawl_checkbox.isChecked():
            cmd_parts.append("--crawl")
        
        # 添加视图参数
        if self.param_widget.full_url_checkbox.isChecked():
            cmd_parts.append("--full-url")
        
        if self.param_widget.redirects_history_checkbox.isChecked():
            cmd_parts.append("--redirects-history")
        
        if not self.param_widget.no_color_checkbox.isChecked():  # 默认是有颜色的
            pass  # 有颜色是默认行为，不需要添加参数
        else:
            cmd_parts.append("--no-color")
        
        if self.param_widget.quiet_mode_checkbox.isChecked():
            cmd_parts.append("-q")
        
        if self.param_widget.disable_cli_checkbox.isChecked():
            cmd_parts.append("--disable-cli")
        
        # 添加输出参数
        if self.param_widget.output_formats_input.text():
            cmd_parts.append(f"-O {self.param_widget.output_formats_input.text()}")
        
        if self.param_widget.output_file_input.text():
            cmd_parts.append(f"-o {self.param_widget.output_file_input.text()}")
        
        if self.param_widget.mysql_url_input.text():
            cmd_parts.append(f"--mysql-url {self.param_widget.mysql_url_input.text()}")
        
        if self.param_widget.postgres_url_input.text():
            cmd_parts.append(f"--postgres-url {self.param_widget.postgres_url_input.text()}")
        
        if self.param_widget.log_file_input.text():
            cmd_parts.append(f"--log {self.param_widget.log_file_input.text()}")
        
        # 更新预览文本
        cmd_text = ' '.join(cmd_parts)
        self.cmd_preview.setText(cmd_text)

    def run_dirsearch(self):
        """
        执行dirsearch，在独立的CMD窗口中运行
        """
        # 获取dirsearch.py的路径
        dirsearch_path = os.path.join(os.path.dirname(__file__), 'dirsearch-master', 'dirsearch.py')
        if not os.path.exists(dirsearch_path):
            QMessageBox.critical(self, "错误", f"找不到dirsearch.py文件: {dirsearch_path}")
            return

        # 构建命令
        cmd = self.cmd_preview.text()
        if not cmd or cmd == "python dirsearch.py":
            QMessageBox.warning(self, "警告", "请先配置扫描参数")
            return

        # 替换python dirsearch.py为实际路径
        cmd = cmd.replace("python dirsearch.py", f"python \"{dirsearch_path}\"")

        try:
            # 在Windows上使用start命令打开新的CMD窗口
            # 使用subprocess.Popen来启动新窗口
            if os.name == 'nt':  # Windows
                # 使用cmd /k来保持窗口打开显示结果
                full_cmd = f'start "dirsearch扫描" cmd /k "{cmd}"'
                subprocess.Popen(full_cmd, shell=True)
            else:  # Unix/Linux/MacOS
                # 对于非Windows系统，使用xterm或gnome-terminal（如果可用）
                terminal_cmd = f'xterm -e "{cmd}; read -p \'Press Enter to exit...\'" &'
                subprocess.Popen(terminal_cmd, shell=True)
            
            self.statusBar().showMessage('已在独立窗口启动扫描')
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动独立窗口失败: {str(e)}")

    def stop_dirsearch(self):
        """
        停止dirsearch（在独立窗口模式下无法停止）
        """
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.stop_toolbar_action.setEnabled(False)
        self.statusBar().showMessage('扫描在独立窗口中运行，无法停止')



    def reset_parameters(self):
        """
        重置参数
        """
        reply = QMessageBox.question(self, '重置参数', 
                                     '确定要重置所有参数到默认值吗？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # 重置所有参数
            self.param_widget.url_input.clear()
            self.param_widget.urls_file_input.clear()
            self.param_widget.stdin_checkbox.setChecked(False)
            self.param_widget.cidr_input.clear()
            self.param_widget.raw_file_input.clear()
            self.param_widget.nmap_report_input.clear()
            self.param_widget.session_file_input.clear()
            self.param_widget.config_file_input.clear()
            
            self.param_widget.wordlists_input.clear()
            self.param_widget.wordlist_categories_input.clear()
            self.param_widget.extensions_input.clear()
            self.param_widget.force_extensions_checkbox.setChecked(False)
            self.param_widget.overwrite_extensions_checkbox.setChecked(False)
            self.param_widget.remove_extensions_checkbox.setChecked(False)
            self.param_widget.exclude_extensions_input.clear()
            self.param_widget.prefixes_input.clear()
            self.param_widget.suffixes_input.clear()
            self.param_widget.uppercase_checkbox.setChecked(False)
            self.param_widget.lowercase_checkbox.setChecked(False)
            self.param_widget.capital_checkbox.setChecked(False)
            
            self.param_widget.threads_spinbox.setValue(25)
            self.param_widget.async_checkbox.setChecked(False)
            self.param_widget.recursive_checkbox.setChecked(False)
            self.param_widget.deep_recursive_checkbox.setChecked(False)
            self.param_widget.force_recursive_checkbox.setChecked(False)
            self.param_widget.max_recursion_depth_spinbox.setValue(0)
            self.param_widget.recursion_status_codes_input.clear()
            self.param_widget.subdirs_input.clear()
            self.param_widget.exclude_subdirs_input.clear()
            self.param_widget.include_status_codes_input.clear()
            self.param_widget.exclude_status_codes_input.clear()
            self.param_widget.exclude_sizes_input.clear()
            self.param_widget.exclude_text_input.clear()
            self.param_widget.exclude_regex_input.clear()
            self.param_widget.exclude_redirect_input.clear()
            self.param_widget.exclude_response_input.clear()
            self.param_widget.skip_on_status_input.clear()
            self.param_widget.min_response_size_spinbox.setValue(0)
            self.param_widget.max_response_size_spinbox.setValue(0)
            self.param_widget.max_time_spinbox.setValue(0)
            self.param_widget.exit_on_error_checkbox.setChecked(False)
            
            self.param_widget.http_method_combobox.setCurrentText("GET")
            self.param_widget.data_input.clear()
            self.param_widget.data_file_input.clear()
            self.param_widget.headers_input.clear()
            self.param_widget.headers_file_input.clear()
            self.param_widget.follow_redirects_checkbox.setChecked(False)
            self.param_widget.random_agent_checkbox.setChecked(False)
            self.param_widget.auth_input.clear()
            self.param_widget.auth_type_combobox.setCurrentIndex(0)
            self.param_widget.cert_file_input.clear()
            self.param_widget.key_file_input.clear()
            self.param_widget.user_agent_input.clear()
            self.param_widget.cookie_input.clear()
            
            self.param_widget.timeout_spinbox.setValue(7.5)
            self.param_widget.delay_spinbox.setValue(0.0)
            self.param_widget.proxy_input.clear()
            self.param_widget.proxies_file_input.clear()
            self.param_widget.proxy_auth_input.clear()
            self.param_widget.replay_proxy_input.clear()
            self.param_widget.tor_checkbox.setChecked(False)
            self.param_widget.scheme_combobox.setCurrentIndex(0)
            self.param_widget.max_rate_spinbox.setValue(0)
            self.param_widget.retries_spinbox.setValue(1)
            self.param_widget.ip_input.clear()
            self.param_widget.interface_input.clear()
            
            self.param_widget.crawl_checkbox.setChecked(False)
            
            self.param_widget.full_url_checkbox.setChecked(False)
            self.param_widget.redirects_history_checkbox.setChecked(False)
            self.param_widget.no_color_checkbox.setChecked(False)
            self.param_widget.quiet_mode_checkbox.setChecked(False)
            self.param_widget.disable_cli_checkbox.setChecked(False)
            
            self.param_widget.output_formats_input.clear()
            self.param_widget.output_file_input.clear()
            self.param_widget.mysql_url_input.clear()
            self.param_widget.postgres_url_input.clear()
            self.param_widget.log_file_input.clear()
            
            self.update_command_preview()

    def save_config(self):
        """
        保存配置
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "保存配置", "", "Config Files (*.json);;All Files (*)")
        if file_path:
            config = {
                'url': self.param_widget.url_input.text(),
                'urls_file': self.param_widget.urls_file_input.text(),
                'stdin': self.param_widget.stdin_checkbox.isChecked(),
                'cidr': self.param_widget.cidr_input.text(),
                'raw_file': self.param_widget.raw_file_input.text(),
                'nmap_report': self.param_widget.nmap_report_input.text(),
                'session_file': self.param_widget.session_file_input.text(),
                'config_file': self.param_widget.config_file_input.text(),
                
                'wordlists': self.param_widget.wordlists_input.text(),
                'wordlist_categories': self.param_widget.wordlist_categories_input.text(),
                'extensions': self.param_widget.extensions_input.text(),
                'force_extensions': self.param_widget.force_extensions_checkbox.isChecked(),
                'overwrite_extensions': self.param_widget.overwrite_extensions_checkbox.isChecked(),
                'remove_extensions': self.param_widget.remove_extensions_checkbox.isChecked(),
                'exclude_extensions': self.param_widget.exclude_extensions_input.text(),
                'prefixes': self.param_widget.prefixes_input.text(),
                'suffixes': self.param_widget.suffixes_input.text(),
                'uppercase': self.param_widget.uppercase_checkbox.isChecked(),
                'lowercase': self.param_widget.lowercase_checkbox.isChecked(),
                'capital': self.param_widget.capital_checkbox.isChecked(),
                
                'threads': self.param_widget.threads_spinbox.value(),
                'async': self.param_widget.async_checkbox.isChecked(),
                'recursive': self.param_widget.recursive_checkbox.isChecked(),
                'deep_recursive': self.param_widget.deep_recursive_checkbox.isChecked(),
                'force_recursive': self.param_widget.force_recursive_checkbox.isChecked(),
                'max_recursion_depth': self.param_widget.max_recursion_depth_spinbox.value(),
                'recursion_status_codes': self.param_widget.recursion_status_codes_input.text(),
                'subdirs': self.param_widget.subdirs_input.text(),
                'exclude_subdirs': self.param_widget.exclude_subdirs_input.text(),
                'include_status_codes': self.param_widget.include_status_codes_input.text(),
                'exclude_status_codes': self.param_widget.exclude_status_codes_input.text(),
                'exclude_sizes': self.param_widget.exclude_sizes_input.text(),
                'exclude_text': self.param_widget.exclude_text_input.text(),
                'exclude_regex': self.param_widget.exclude_regex_input.text(),
                'exclude_redirect': self.param_widget.exclude_redirect_input.text(),
                'exclude_response': self.param_widget.exclude_response_input.text(),
                'skip_on_status': self.param_widget.skip_on_status_input.text(),
                'min_response_size': self.param_widget.min_response_size_spinbox.value(),
                'max_response_size': self.param_widget.max_response_size_spinbox.value(),
                'max_time': self.param_widget.max_time_spinbox.value(),
                'exit_on_error': self.param_widget.exit_on_error_checkbox.isChecked(),
                
                'http_method': self.param_widget.http_method_combobox.currentText(),
                'data': self.param_widget.data_input.toPlainText(),
                'data_file': self.param_widget.data_file_input.text(),
                'headers': self.param_widget.headers_input.toPlainText(),
                'headers_file': self.param_widget.headers_file_input.text(),
                'follow_redirects': self.param_widget.follow_redirects_checkbox.isChecked(),
                'random_agent': self.param_widget.random_agent_checkbox.isChecked(),
                'auth': self.param_widget.auth_input.text(),
                'auth_type': self.param_widget.auth_type_combobox.currentText(),
                'cert_file': self.param_widget.cert_file_input.text(),
                'key_file': self.param_widget.key_file_input.text(),
                'user_agent': self.param_widget.user_agent_input.text(),
                'cookie': self.param_widget.cookie_input.text(),
                
                'timeout': self.param_widget.timeout_spinbox.value(),
                'delay': self.param_widget.delay_spinbox.value(),
                'proxy': self.param_widget.proxy_input.text(),
                'proxies_file': self.param_widget.proxies_file_input.text(),
                'proxy_auth': self.param_widget.proxy_auth_input.text(),
                'replay_proxy': self.param_widget.replay_proxy_input.text(),
                'tor': self.param_widget.tor_checkbox.isChecked(),
                'scheme': self.param_widget.scheme_combobox.currentText(),
                'max_rate': self.param_widget.max_rate_spinbox.value(),
                'retries': self.param_widget.retries_spinbox.value(),
                'ip': self.param_widget.ip_input.text(),
                'interface': self.param_widget.interface_input.text(),
                
                'crawl': self.param_widget.crawl_checkbox.isChecked(),
                
                'full_url': self.param_widget.full_url_checkbox.isChecked(),
                'redirects_history': self.param_widget.redirects_history_checkbox.isChecked(),
                'no_color': self.param_widget.no_color_checkbox.isChecked(),
                'quiet_mode': self.param_widget.quiet_mode_checkbox.isChecked(),
                'disable_cli': self.param_widget.disable_cli_checkbox.isChecked(),
                
                'output_formats': self.param_widget.output_formats_input.text(),
                'output_file': self.param_widget.output_file_input.text(),
                'mysql_url': self.param_widget.mysql_url_input.text(),
                'postgres_url': self.param_widget.postgres_url_input.text(),
                'log_file': self.param_widget.log_file_input.text()
            }
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                self.statusBar().showMessage(f'配置已保存到: {file_path}')
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存配置失败: {str(e)}")

    def load_config(self):
        """
        加载配置
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "加载配置", "", "Config Files (*.json);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 加载配置
                self.param_widget.url_input.setText(config.get('url', ''))
                self.param_widget.urls_file_input.setText(config.get('urls_file', ''))
                self.param_widget.stdin_checkbox.setChecked(config.get('stdin', False))
                self.param_widget.cidr_input.setText(config.get('cidr', ''))
                self.param_widget.raw_file_input.setText(config.get('raw_file', ''))
                self.param_widget.nmap_report_input.setText(config.get('nmap_report', ''))
                self.param_widget.session_file_input.setText(config.get('session_file', ''))
                self.param_widget.config_file_input.setText(config.get('config_file', ''))
                
                self.param_widget.wordlists_input.setText(config.get('wordlists', ''))
                self.param_widget.wordlist_categories_input.setText(config.get('wordlist_categories', ''))
                self.param_widget.extensions_input.setText(config.get('extensions', ''))
                self.param_widget.force_extensions_checkbox.setChecked(config.get('force_extensions', False))
                self.param_widget.overwrite_extensions_checkbox.setChecked(config.get('overwrite_extensions', False))
                self.param_widget.remove_extensions_checkbox.setChecked(config.get('remove_extensions', False))
                self.param_widget.exclude_extensions_input.setText(config.get('exclude_extensions', ''))
                self.param_widget.prefixes_input.setText(config.get('prefixes', ''))
                self.param_widget.suffixes_input.setText(config.get('suffixes', ''))
                self.param_widget.uppercase_checkbox.setChecked(config.get('uppercase', False))
                self.param_widget.lowercase_checkbox.setChecked(config.get('lowercase', False))
                self.param_widget.capital_checkbox.setChecked(config.get('capital', False))
                
                self.param_widget.threads_spinbox.setValue(config.get('threads', 25))
                self.param_widget.async_checkbox.setChecked(config.get('async', False))
                self.param_widget.recursive_checkbox.setChecked(config.get('recursive', False))
                self.param_widget.deep_recursive_checkbox.setChecked(config.get('deep_recursive', False))
                self.param_widget.force_recursive_checkbox.setChecked(config.get('force_recursive', False))
                self.param_widget.max_recursion_depth_spinbox.setValue(config.get('max_recursion_depth', 0))
                self.param_widget.recursion_status_codes_input.setText(config.get('recursion_status_codes', ''))
                self.param_widget.subdirs_input.setText(config.get('subdirs', ''))
                self.param_widget.exclude_subdirs_input.setText(config.get('exclude_subdirs', ''))
                self.param_widget.include_status_codes_input.setText(config.get('include_status_codes', ''))
                self.param_widget.exclude_status_codes_input.setText(config.get('exclude_status_codes', ''))
                self.param_widget.exclude_sizes_input.setText(config.get('exclude_sizes', ''))
                self.param_widget.exclude_text_input.setText(config.get('exclude_text', ''))
                self.param_widget.exclude_regex_input.setText(config.get('exclude_regex', ''))
                self.param_widget.exclude_redirect_input.setText(config.get('exclude_redirect', ''))
                self.param_widget.exclude_response_input.setText(config.get('exclude_response', ''))
                self.param_widget.skip_on_status_input.setText(config.get('skip_on_status', ''))
                self.param_widget.min_response_size_spinbox.setValue(config.get('min_response_size', 0))
                self.param_widget.max_response_size_spinbox.setValue(config.get('max_response_size', 0))
                self.param_widget.max_time_spinbox.setValue(config.get('max_time', 0))
                self.param_widget.exit_on_error_checkbox.setChecked(config.get('exit_on_error', False))
                
                self.param_widget.http_method_combobox.setCurrentText(config.get('http_method', 'GET'))
                self.param_widget.data_input.setPlainText(config.get('data', ''))
                self.param_widget.data_file_input.setText(config.get('data_file', ''))
                self.param_widget.headers_input.setPlainText(config.get('headers', ''))
                self.param_widget.headers_file_input.setText(config.get('headers_file', ''))
                self.param_widget.follow_redirects_checkbox.setChecked(config.get('follow_redirects', False))
                self.param_widget.random_agent_checkbox.setChecked(config.get('random_agent', False))
                self.param_widget.auth_input.setText(config.get('auth', ''))
                self.param_widget.auth_type_combobox.setCurrentText(config.get('auth_type', ''))
                self.param_widget.cert_file_input.setText(config.get('cert_file', ''))
                self.param_widget.key_file_input.setText(config.get('key_file', ''))
                self.param_widget.user_agent_input.setText(config.get('user_agent', ''))
                self.param_widget.cookie_input.setText(config.get('cookie', ''))
                
                self.param_widget.timeout_spinbox.setValue(config.get('timeout', 7.5))
                self.param_widget.delay_spinbox.setValue(config.get('delay', 0.0))
                self.param_widget.proxy_input.setText(config.get('proxy', ''))
                self.param_widget.proxies_file_input.setText(config.get('proxies_file', ''))
                self.param_widget.proxy_auth_input.setText(config.get('proxy_auth', ''))
                self.param_widget.replay_proxy_input.setText(config.get('replay_proxy', ''))
                self.param_widget.tor_checkbox.setChecked(config.get('tor', False))
                self.param_widget.scheme_combobox.setCurrentText(config.get('scheme', ''))
                self.param_widget.max_rate_spinbox.setValue(config.get('max_rate', 0))
                self.param_widget.retries_spinbox.setValue(config.get('retries', 1))
                self.param_widget.ip_input.setText(config.get('ip', ''))
                self.param_widget.interface_input.setText(config.get('interface', ''))
                
                self.param_widget.crawl_checkbox.setChecked(config.get('crawl', False))
                
                self.param_widget.full_url_checkbox.setChecked(config.get('full_url', False))
                self.param_widget.redirects_history_checkbox.setChecked(config.get('redirects_history', False))
                self.param_widget.no_color_checkbox.setChecked(config.get('no_color', False))
                self.param_widget.quiet_mode_checkbox.setChecked(config.get('quiet_mode', False))
                self.param_widget.disable_cli_checkbox.setChecked(config.get('disable_cli', False))
                
                self.param_widget.output_formats_input.setText(config.get('output_formats', ''))
                self.param_widget.output_file_input.setText(config.get('output_file', ''))
                self.param_widget.mysql_url_input.setText(config.get('mysql_url', ''))
                self.param_widget.postgres_url_input.setText(config.get('postgres_url', ''))
                self.param_widget.log_file_input.setText(config.get('log_file', ''))
                
                self.update_command_preview()
                self.statusBar().showMessage(f'配置已加载: {file_path}')
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加载配置失败: {str(e)}")

    def show_about(self):
        """
        显示关于对话框
        """
        QMessageBox.about(self, "关于 dirsearch GUI", 
                         "dirsearch GUI v1.0\n\n"
                         "这是一个为dirsearch工具开发的图形用户界面。\n"
                         "dirsearch是一个高级的web路径爆破工具。\n\n"
                         "使用PyQt6开发。")

    def closeEvent(self, event):
        """
        关闭事件处理
        """
        # 由于现在在独立窗口中运行，没有内部工作线程需要管理
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('dirsearch GUI')
    app.setApplicationVersion('1.0')
    
    # 设置应用图标（如果有的话）
    # app.setWindowIcon(QIcon('icon.png'))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
