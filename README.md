# YahooScraping
**Código para extraer datos financieros de https://finance.yahoo.com hecho en Python.**

El archivo llamado evelyn_spider.py contiene el código para hacer scraping en Yahoo. 

Desde la terminal :
>              python evelyn_spider.py SIGLAS
              
donde siglas debe cambiarse por alguno de los activos en mayúsculas. El código crea un archivo .json donde guarda la información extraida
y además actualiza la tabla llamada FinanceY que tiene como renglones los activos y como columnas los datos Previous Close, Open Close,
Day's Range, 52 Week Range, Volume, Net Asset Value, PE Ratio, Yield, Date.

