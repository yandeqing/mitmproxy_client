pyinstaller -F -i ./icons/logo.ico   -p   C:\Users\Zuber\PycharmProjects\mitmproxy_client; ./proxy_util/proxy_helper.py
pyinstaller -D -i ./icons/logo.ico   -p   C:\Users\Zuber\PycharmProjects\mitmproxy_client; ./proxy_util/proxy_helper.py
pyinstaller -F -p  C:\Users\Zuber\PycharmProjects\mitmproxy_client; ./proxy_util/proxy_helper.py --noconsole
pyinstaller -F proxy_helper.spec
cmd