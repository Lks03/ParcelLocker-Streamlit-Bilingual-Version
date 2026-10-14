# 快递柜管理系统 / Parcel Locker System

独立的中英文切换版本，使用本地 `data.json` 保存记录，无需 Supabase 或密钥。

A standalone Chinese/English app with local JSON storage. No Supabase account or API key is required.

## 运行 / Run

安装 Python 3.10 或更新版本，在本项目文件夹打开终端并运行：

Install Python 3.10 or later, open a terminal in this folder, and run:

```shell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Windows 也可以双击 `启动应用.bat`，首次使用需要联网安装依赖。

On Windows, you can also double-click `启动应用.bat`. The first launch needs internet access to install dependencies.

## 语言切换 / Language

侧边栏顶部选择“简体中文”或“English”。默认中文，当前浏览器会话内保留选择；刷新或开启新会话可能恢复默认。

Choose 简体中文 or English at the top of the sidebar. Chinese is the default; the selection is kept for the browser session and may reset in a new session.

支持首页、登记、取件、记录、柜子状态、验证提示、空状态和错误信息切换。姓名、联系方式、快递单号和取件码不会被翻译。Streamlit 自带的管理菜单和浏览器界面由平台控制。

App pages, buttons, statuses and messages are translated. Names, contacts, tracking numbers and pickup codes stay unchanged. Streamlit's own management menus and browser controls are managed by the platform.

## 数据 / Data

- 初次运行有 12 个空闲柜子，首次存件后自动生成 `data.json`。
- 存件、取件成功后立即保存。关闭和重新打开本机程序后，文件仍在则记录仍在。
- 在程序关闭时备份整个 `data.json`；恢复时将备份放回项目目录。
- 可使用环境变量 `PARCEL_LOCKER_DATA_FILE` 指定其他存储路径。
- 本地文件版本适合单个服务器进程的演示。没有登录权限控制，柜门和消息通知都是模拟。

- Starts with twelve empty lockers and creates `data.json` after the first registration.
- Successful registration and collection save immediately. Local records survive restarts while the file remains available.
- Back up the complete `data.json` while the app is stopped; restore it to the project folder.
- Set `PARCEL_LOCKER_DATA_FILE` to use a different storage path.
- Intended for a single-process demonstration. There is no login/access control; locker opening and notifications are simulated.

## 上传 GitHub / Upload to GitHub

建议为这份版本新建仓库，上传解压后文件夹内的文件，Streamlit 入口选 `app.py`。这样现有连接 Supabase 的网站可以继续使用。

如果选择替换原仓库，须一起上传本版本的 `controller.py`、`views.py`、`i18n.py` 和 `requirements.txt`。其余配套文件也包含在此完整项目中。不要只更新页面文件。此版本不会导入或连接原 Supabase 数据。

Prefer a separate repository for this version and use `app.py` as the Streamlit entry point. To replace an existing version, update `controller.py`, `views.py`, `i18n.py` and `requirements.txt` together. This package includes the complete supporting project. Existing Supabase records are not imported.

**部署到 Streamlit Community Cloud 时，本地文件不是持久数据库，重启或重新部署后可能丢失。需要长期保存时，请在自己的电脑或有持久磁盘的服务器运行。**

**On Streamlit Community Cloud, local files are not durable storage and may be lost on restart or redeployment. For lasting local storage, run on your computer or a server with a persistent disk.**
