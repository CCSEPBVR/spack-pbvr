# パッケージマネージャーSpackでCS-PBVRをインストールする方法
## はじめに
CS-PBVRはパッケージマネージャーSpackに対応している。<br>
Spackにはオリジナルのレポジトリを追加する機能があり、それを利用してCS-PBVRをインストールする。

## 公式のSpackと富士通コンパイラ対応のSpackについて
Spackには公式のSpackと富岳などで使用するための富士通コンパイラに対応したSpackが存在する。<br>
富士通コンパイラに対応したSpackは[理化学研究所](https://github.com/RIKEN-RCCS)が公式のSpackをフォークして開発している。<br>
公式のSpackのgithubのレポジトリは[こちら](https://github.com/spack/spack)<br>
富士通コンパイラに対応したSpackのgithubのレポジトリは[こちら](https://github.com/RIKEN-RCCS/spack)<br>
このレポジトリは公式のSpackに使用するオリジナルのレポジトリである。<br>
富士通コンパイラに対応したSpackで使用するオリジナルのレポジトリは[こちら](https://github.com/CCSEPBVR/spack-pbvr-fujitsu)。<br>
ここでは公式のSpackでオリジナルのレポジトリを追加する方法を説明する。

## 公式のSpackにオリジナルのレポジトリを追加する
以下のコマンドでインストールすることができる。<br>
インストール時に使用したコンパイラはgcc@8.5.0
```
spack install gcc@8.5.0 # 必要であれば
git clone https://github.com/CCSEPBVR/spack-pbvr.git # レポジトリのクローン
spack repo add /path/to/spack-pbvr # Spackにレポジトリを追加
spack install pbvr %gcc@8.5.0　# コンパイラgcc@8.5.0を使ってインストール
```
インストール時にオプションを設定することができる。<br>
すべてのオプションがデフォルトでONになっている
- client：クライアントをビルドする
- mpi：MPI並列化を有効にする
- extended_fileformat：データ形式拡張(VTK)を有効にする

オプションの設定方法のサンプルは以下の通り。
```
spack install pbvr +client +mpi +extended_fileformat %gcc@8.5.0 # すべて有効(デフォルト)
spack install pbvr ~client ~mpi ~extended_fileformat %gcc@8.5.0 # すべて無効
```
データ形式拡張(VTK)を有効にすると、フィルタプログラム・KVSMLコンバータを使用せずにサンプルデータを可視化することができる。<br>
大規模データを扱う場合は、フィルタプログラム・KVSMLコンバータを使用し、KVSML形式に変換して可視化することを推奨する。