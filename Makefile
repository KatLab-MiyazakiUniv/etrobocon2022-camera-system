# @file: Makefile
# @brief: etrobocon2022 カメラシステムのタスクランナー!?
# @author: Takahiro55555
# NOTE: foolproofのために、'make'単体のコマンドではプログラムを実行できないようにしておく

SHELL       := powershell.exe
.SHELLFLAGS := -NoProfile -Command

all: style test

clean: coverage-clean

run-L:
	poetry run python camera --is-left True

run-R:
	poetry run python camera --is-left False

# NOTE: tox.ini ファイルの設定に従って、全てのソースコードの静的解析を実行する
style:
	[Environment]::SetEnvironmentVariable('PYTHONUTF8',1); poetry run python -m pycodestyle camera/ tests/
	[Environment]::SetEnvironmentVariable('PYTHONUTF8',1); poetry run python -m pydocstyle camera/ tests/

# NOTE: unittestを実行する
test:
	poetry run python -m unittest

coverage:
	poetry run python -m coverage run --source=camera/ -m unittest discover -s tests/
	poetry run python -m coverage report

# NOTE: htmlcovディレクトリが生成され、index.htmlをブラウザで開くことでカバレッジを視覚的に確認できる
coverage-html: coverage
	poetry run python -m coverage html

# NOTE: 下記のコマンドは、2行に分けると何故かRemove-Itemコマンドが実行できずにエラーが発生した。
#		poetry run python -m coverage erase; Remove-Item -Force -Recurse .\htmlcov
coverage-clean:
	poetry run python -m coverage erase; Remove-Item -Force -Recurse htmlcov

# NOTE: tox.ini ファイルの設定に従って、全てのソースコードをフォーマットする
format:
	[Environment]::SetEnvironmentVariable('PYTHONUTF8',1); poetry run python -m autopep8 -i -r camera/ tests/
