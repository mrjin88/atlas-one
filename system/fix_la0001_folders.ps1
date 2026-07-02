# Fix LA-0001 required folders

cd E:\atlas-one\projects\lost-archive\content\LA-0001-roman-concrete

New-Item -ItemType Directory -Force -Path "assets\images"
New-Item -ItemType Directory -Force -Path "assets\videos"
New-Item -ItemType Directory -Force -Path "assets\voice"
New-Item -ItemType Directory -Force -Path "assets\music"
New-Item -ItemType Directory -Force -Path "assets\sfx"
New-Item -ItemType Directory -Force -Path "assets\thumbnail"

New-Item -ItemType Directory -Force -Path "exports\youtube"
New-Item -ItemType Directory -Force -Path "exports\shorts"
New-Item -ItemType Directory -Force -Path "exports\archive"

python E:\atlas-one\system\validators\validate_project.py
