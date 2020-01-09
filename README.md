###### tags: `git project`

# Cache-replacement
* 高等計算機結構 Project3
* 說明
    * 至少要做兩種Cache replacement演算法！
    * 其中一種要用LRU。
    * 上課有說盡量不要寫FIFO或是FILO這種。
* HackMD 連結: https://hackmd.io/@EzhUyvwWT32Gy69CeyFNyA/ryBRgH4kI

# 目錄
[TOC]

## 程式執行方法
```=
python main.py [case] [type] [cache size] [block size] [way] [address]

執行範例:
python main.py case1.txt 0 16 16 4 20
```
* [case]
    * case 輸入測資檔名 i.e. case1.txt
* [type]
    * type = 0 : LRU
    * type = 1 : MRU
* [cache size]
    * data cache 的大小
    * 單位 : KB
* [block size]
    * black 的個數
    * 單位 : Byte
* [way]
    * w-way set-associative
* [address]
    * main memory 有 m-bit address，byte addressable

## Data Replacement Alogrithm
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
```=
index: 4e
Cycle  |                                           |  tag   | Hit/Miss
  1    |  c6(1)   |          |          |          |   c6   | Miss
  3    |  c6(1)   |  c7(3)   |          |          |   c7   | Miss
  4    |  c6(4)   |  c7(3)   |          |          |   c6   | Hit
  6    |  c6(4)   |  c7(3)   |  f6(6)   |          |   f6   | Miss
  7    |  c6(4)   |  c7(3)   |  f6(6)   |  f7(7)   |   f7   | Miss
  8    |  c6(4)   |  f8(8)   |  f6(6)   |  f7(7)   |   f8   | Miss
  10   |  c6(10)  |  f8(8)   |  f6(6)   |  f7(7)   |   c6   | Hit
  12   |  c6(10)  |  f8(8)   |  c7(12)  |  f7(7)   |   c7   | Miss

index: 4c
Cycle  |                                           |  tag   | Hit/Miss
  2    |  c6(2)   |          |          |          |   c6   | Miss
  5    |  c6(5)   |          |          |          |   c6   | Hit
  9    |  c6(5)   |  c7(9)   |          |          |   c7   | Miss
  11   |  c6(11)  |  c7(9)   |          |          |   c6   | Hit
```
## 系統流程
1. 執行 main()
2. 用 readfile() 將資料讀取進來
3. 用 init_info() 計算出 offset、index、tag 長度
4. 開始執行 run()
5. 用 init_cache() 將 cache 建出來
6. 跑 loop
7. 看有沒有 hit，miss->8，hit->11
8. 看有沒有 空的 cache cell 可以放這次 miss 的 tag，有->9，沒有->10
9. 直接放進空的 cache cell
10. 執行 cache replace()
11. loop 還沒結束->6，結束->12
12. 用 output() 輸出所有的 log


## Function 說明
* def main():  
    * 程式進入位置
    * 接收參數([case] [type] [cache size] [block size] [way] [address])
    * 呼叫 init_info 
    * 呼叫 run
* def init_info(cache_size, block_size, way, address):  
    * 計算出 offset_size, index_size, tag_size
    * return offset_size, index_size, tag_size
* def hex2bin(HEX):  
    * 回傳 16進位轉2進位
    * return 2進位
* def bin2hex(BIN):  
    * 回傳 2進位轉16進位
    * return 16進位
* def readfile(case_dir):  
    * 讀取 case 資料，儲存進 list
    * return list
* def init_cache(index_size, way):  
    * 建立 cache 資料結構
    * return cache
* def find_empty_node(cache, index):  
    * pos = 找到空的位置
    * return pos
* def hit(cache, index, tag, cycle):  
    * return bool
* def replace(cache, index, tag, alg, cycle):  
    * 根據 alg 決定 要 replace 哪一個
* def run(lines, offset_size, index_size, tag_size, way, alg):  
    * 開始執行
* def output(logs):  
    * 輸出執行結果