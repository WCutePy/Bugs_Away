@echo off
call C:\pythonVenvs\FrameShooter\Scripts\activate 
pip install --no-deps --no-build-isolation -r requirements.txt
deactivate