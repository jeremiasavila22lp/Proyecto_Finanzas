@echo off
title Servidor Web - FinanzasPro
echo ===========================================
echo   PREPARANDO ENTORNO
echo ===========================================
echo Instalando dependencias necesarias...
pip install fastapi uvicorn

echo.
echo ===========================================
echo   INICIANDO SERVIDOR WEB (API)
echo ===========================================
echo.
echo Ve a http://127.0.0.1:8000 en tu navegador
echo.
python -m uvicorn api_corregido:app --reload
pause
