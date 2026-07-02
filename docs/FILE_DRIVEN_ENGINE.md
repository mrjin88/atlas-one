# Atlas ONE File-Driven Engine

## Quyết định kiến trúc

Giữ Markdown/YAML là source of truth.

Không chuyển sang Project Object database.

## Cài đặt

Copy file:

```text
validators/validate_project.py → E:\atlas-one\system\validators\validate_project.py
builders/build_batches.py → E:\atlas-one\system\builders\build_batches.py
```

Nếu chưa có thư mục:

```powershell
New-Item -ItemType Directory -Force -Path E:\atlas-one\system\validators
New-Item -ItemType Directory -Force -Path E:\atlas-one\system\builders
```

## Chạy kiểm tra project

```powershell
cd E:\atlas-one\projects\lost-archive\content\LA-0001-roman-concrete
python E:\atlas-one\system\validators\validate_project.py
```

## Xuất batch prompt

```powershell
python E:\atlas-one\system\builders\build_batches.py
```

Output:

```text
exports/archive/image_prompt_batch.csv
exports/archive/video_prompt_batch.csv
exports/archive/edit_decision_list.csv
```

## Source of truth

```text
research.md
script.md
timeline.md
shots.md
shots.yaml
review.md
publish_checklist.md
seo.json
```
