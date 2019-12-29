###### tags: `git project`

# Cache-replacement
* 高等計算機結構 Project3
* HackMD 連結: https://hackmd.io/@EzhUyvwWT32Gy69CeyFNyA/ryBRgH4kI

# 目錄
[TOC]

## 程式執行方法
```=
python main.py [case] [type] [cache size]

執行範例:
python main.py case1.txt 0 4
```
* [case]
    * case 輸入測資檔名 i.e. case1.txt
* [type]
    * type = 0 : LRU
    * type = 1 : MRU
* [cache size]
    * cache 的大小

## Background
### LRU
* 丟棄最近最少使用的資料
* example
    * cache size : 4
    * input : ABCDEDF


| cycle | c1       | c2       | c3       | c4       |
| ----- | -------- | -------- | -------- | -------- |
| 1     | **A(1)** |          |          |          |
| 2     | A(1)     | **B(2)** |          |          |
| 3     | A(1)     | B(2)     | **C(3)** |          |
| 4     | A(1)     | B(2)     | C(3)     | **D(4)** |
| 5     | **E(5)** | B(2)     | C(3)     | D(4)     |
| 6     | E(5)     | B(2)     | C(3)     | **D(6)** |
| 7     | E(5)     | **F(7)** | C(3)     | D(6)     |

### MRU
* 丟棄最近使用的資料
* 對於隨機訪問模式和對大型數據集的重複掃描（有時稱為循環訪問模式），MRU緩存算法比LRU更具吸引力，因為它們傾向於保留較舊的數據。
* example
    * cache size : 4
    * input : ABCDECDB

| cycle | c1       | c2       | c3       | c4       |
| ----- | -------- | -------- | -------- | -------- |
| 1     | **A(1)** |          |          |          |
| 2     | A(1)     | **B(2)** |          |          |
| 3     | A(1)     | B(2)     | **C(3)** |          |
| 4     | A(1)     | B(2)     | C(3)     | **D(4)** |
| 4     | A(1)     | B(2)     | C(3)     | **E(5)** |
| 4     | A(1)     | B(2)     | **C(6)** | E(5)     |
| 4     | A(1)     | B(2)     | **D(7)** | E(5)     |
| 4     | A(1)     | **B(3)** | D(7)     | E(5)     |

### 資料來源
* 維基百科 : https://en.wikipedia.org/wiki/Cache_replacement_policies


## 測資
```=  
C64E5
C64C5
C74EA
C64E8
C64CF
F64E6
F74EA
F84E6
C74CF
C64E6
C64C9
C74E8
```

## 執行結果

## 系統流程
```mermaid
classDiagram

main -- > LRU : type == 0
main -- > MRU : type == 1

main : type:int
main : cache_size:int
main : chahe:list
main : readfile()
main : LRU()
main : MRU()
```
## Function 說明