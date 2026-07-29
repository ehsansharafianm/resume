@echo off
python "%~dp0system\resume_tool.py" migrate --quiet
python "%~dp0system\resume_tool.py" render -Input "%~dp0master\Ehsan_Sharafian_Master.yaml" -OutputHtml "%~dp0system\index.html" -OutputPdf "%~dp0Ehsan-Sharafian-Resume.pdf" %*
