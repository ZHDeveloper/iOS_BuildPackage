
## iOS_BuildPackage

一个简单的iOS项目自动化打包、上传到AppStore或者蒲公英的Python脚本。需要更多持续集成的功能，例如自动截图,请使用`fastlan`。

## 使用方法

> 将build_package.py放到项目的根目录。

```
Usage: python3 build_package.py [command] [arguments]

Command:
-u              Optional,AppStore , Pgyer
-s              Optional,Xcode project's scheme name.
-c              Optional,Release or Debug,default is Realease.
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
python3 build_package.py -c Debug -o AdHoc -u Pgyer
```

> 上传到AppStore

```
#编辑苹果账号和专属密码
python3 build_package.py -c Release -o AppStore -u AppStore
```

## 参考资料

* [xcodebuild](https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man1/xcodebuild.1.html)
* [蒲公英上传APP](https://www.pgyer.com/doc/api#paramInfo)
* [通过 altool 上传 App 的二进制文件](https://help.apple.com/itc/apploader/#/apdATD1E53-D1E1A1303-D1E53A1126)

