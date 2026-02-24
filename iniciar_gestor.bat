@echo off
title Lanzador - Gestor de Finanzas Pro
echo ===========================================
echo   INICIANDO GESTOR DE FINANZAS PRO
echo ===========================================
echo.

echo [1/2] Verificando e instalando dependencias...
pip install -r requirements.txt

echo.
echo [2/2] Lanzando aplicacion...
python main.py

echo.
echo Aplicacion cerrada.
pause