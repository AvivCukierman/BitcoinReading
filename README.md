# BitcoinReading 
A package for reading and storing bitcoin information from bitstamp.
## Installation
```
git clone https://github.com/ekulyk/PythonPusherClient
cd PythonPusherClient
python setup.py install
cd ../
```
## Usage
```
python basic.py [flags]
```
### Options
Flag | Options | Description
--- | --- | ---
-s,--stream | 'order_book','live_trades','diff_order_book' | Which stream to read
-t,--time_diff | | How many seconds between each save
-q,--quiet | | Suppress all stdout
