# QR Reader App (Multi-Camera)

- Canon EOS (EDSDK, スタブ) / ONVIF/RTSP / ダミーカメラ対応
- 1〜8台までマルチプロセスで並列制御
- GUIからシリアル番号・IP・RTSP URL 等を入力して接続

## セットアップ
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
