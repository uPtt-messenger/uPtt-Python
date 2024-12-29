# UPTT Project

uPtt 是一款專為批踢踢使用者設計的開源即時通訊軟體，支援 MacOS 和 Windows 作業系統。
有了 uPtt，您可以在電腦上透過批踢踢伺服器傳送即時訊息，再也不必再另行開啟瀏覽器登入 Ptt。
uPtt 所有訊息與驗證皆透過批踢踢伺服器進行登入驗證。無論是您的帳號或者訊息傳遞完全建立在批踢踢現有架構上。無需額外註冊，只要有批踢踢帳號，即可開始使用 uPtt。
uPtt 旨在提供現代化簡約直覺的操作介面，讓您輕鬆透過批踢踢傳送即時訊息。無論是接收、閱讀或發送訊息，一切即時通訊需求都能在 uPtt 視窗中完成，帶來流暢無阻的溝通體驗。

## Features

- User authentication system
- System tray integration
- Dark mode interface

## Requirements

- Python 3.x
- Required packages (check requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/uptt_python.git
cd uptt_python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Project Structure

- `src/main.py` - Application entry point
- `src/login.py` - Login window implementation
- `src/system_tray.py` - System tray functionality

## License

[MIT License](LICENSE)

## Contributing

Feel free to open issues and pull requests for any improvements.

---
Last updated: 2024-12-29
