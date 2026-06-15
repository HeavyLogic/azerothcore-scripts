@echo off
COLOR F
echo __________________________Portable MySQL Server__________________________
echo ______________________________MySQL 8.4.7________________________________
echo.
echo MySQL is currently running. Please only close this window for shutdown.
echo Please disregard any InoDB messages that are prompted. They have no use.
echo After your server is shut off, press CTRL C to shut down this service.
echo __________________________________________________________________________
:: mysql\bin\mysqld --standalone --console --max_allowed_packet=128M --innodb_redo_log_capacity=200MB --binlog_expire_logs_seconds=432000 --innodb_buffer_pool_size=2G --innodb_io_capacity=500 --innodb_io_capacity_max=2500 --innodb_use_fdatasync=ON --innodb_buffer_pool_instances=12 --innodb_log_buffer_size=32M --transaction_isolation="READ-COMMITTED"
mysql\bin\mysqld --standalone --console --max_allowed_packet=128M --innodb_flush_log_at_trx_commit=0 --innodb_buffer_pool_size=4G --innodb_log_buffer_size=256M --innodb_write_io_threads=8 --innodb_read_io_threads=8 --innodb_flush_log_at_timeout=10 --innodb_max_dirty_pages_pct=90


if errorlevel 1 goto error
goto finish

:error
echo.
echo MySQL could not be started.
pause

:finish
