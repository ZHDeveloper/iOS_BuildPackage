
## iOS_BuildPackage

一个简单的iOS项目自动化打包、上传到蒲公英的Python脚本。需要更多持续集成的功能，例如自动截图、自动打包上传到AppStroe,请使用`fastlan`。

## 使用方法

> 将build_package.py放到项目的根目录。

```
Usage: python3 build_package.py [command] [arguments]

Command:
-u              Optional,Upload ipa to pgyer
-s              Optional,Xcode project's scheme name.
-c              Optional,Realease or Debug,default is Realease.
-o              Optional,AppStore , AdHoc, Enterprise or Development default is Development.

```

> 自动化生成测试包

```
python3 build_package.py
or 
python3 build_package.py -c Debug -o Development

```

> 自动化生成正式包

```
python3 build_package.py -c Release -o AppStore

```
> 上传到蒲公英

```
#根据蒲公英账号编辑uKey和_api_key
python3 build_package.py -u

```
## 