
import os,sys,getopt
import subprocess
import shutil
import requests

tips = '''
Usage: python3 build_package.py [command] [arguments]

Command:
-u              Optional,Upload ipa to pgyer
-s              Optional,Xcode project's scheme name.
-c              Optional,Realease or Debug,default is Realease.
-o              Optional,AppStore , AdHoc, Enterprise or Development default is Development.
'''

ExportOptions = {
"AppStore": '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>method</key>
	<string>app-store</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>compileBitcode</key>
	<true/>
</dict>
</plist>
''',
"AdHoc":'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>method</key>
	<string>ad-hoc</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>compileBitcode</key>
	<false/>
</dict>
</plist>
''',
"Enterprise":'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>method</key>
	<string>enterprise</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>compileBitcode</key>
	<false/>
</dict>
</plist>
''',
"Development":'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>method</key>
	<string>development</string>
	<key>signingStyle</key>
	<string>automatic</string>
	<key>compileBitcode</key>
	<false/>
</dict>
</plist>
'''
}

# 编译存放的文件目录
build_path = "./build"

def build_ipa(scheme_name="",config="Debug",export_option="Development"):
    
    dirs = os.listdir(".")

    xcodeproj = ""
    xcworkspace = ""
    is_workspace = False

    for adir in dirs:
        if adir.find("xcodeproj") >= 0:
            xcodeproj = adir
        elif adir.find("xcworkspace") >= 0:
            is_workspace = True
            xcworkspace = adir

    if len(scheme_name) == 0:
        if is_workspace:
            scheme_name = xcworkspace.split(".")[0]
        else:
            scheme_name = xcodeproj.split(".")[0]

    if len(scheme_name) == 0:
        print("Cannot find the scheme, please confirm whether the scheme is correct,or use -h to see more.")
        os._exit(0)

    # 清空build文件夹
    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    os.mkdir(build_path)

    archive_path = build_path + "/" + scheme_name + ".xcarchive"
    export_path = build_path + scheme_name

    # 生成导出的plist文件
    export_option_path = build_path + "/PackageExportOptions.plist"
    f = open(export_option_path,"w")
    f.write(ExportOptions[export_option])
    f.close()

    try:
        if is_workspace:
            subprocess.check_call(["xcodebuild","clean","-workspace",xcworkspace,"-scheme",scheme_name,"-configuration",config])
            subprocess.check_call(["xcodebuild","archive","-workspace",xcworkspace,"-scheme",scheme_name,"-configuration",config,"-archivePath",archive_path])
        else:
            subprocess.check_call(["xcodebuild","clean","-project",xcodeproj,"-scheme",scheme_name,"-configuration",config])
            subprocess.check_call(["xcodebuild","archive","-project",xcodeproj,"-scheme",scheme_name,"-configuration",config,"-archivePath",archive_path])

        subprocess.check_call(["xcodebuild","-exportArchive","-archivePath",archive_path,"-exportPath",build_path,"-exportOptionsPlist",export_option_path]) 

    except Exception as error:
        os._exit(0)

def upload_ipa():

    ipa_path = ""

    try:
        files = os.listdir(build_path)
        for file in files:
            if file.find(".ipa") >= 0 :
                ipa_path = file

        if len(ipa_path) == 0:
            print("ipa file does not exist, please compile the project first.")
            return
        
    except Exception as identifier:
        print("ipa file does not exist, please compile the project first")
        return

    url = "https://qiniu-storage.pgyer.com/apiv1/app/upload"

    # 需要从蒲公英官网获取
    data = {
        "uKey": "d5dfd81cf2f62fb65e6e67f0bed034de",
        "_api_key": "51f5737e29e008c857053467a0d618b3",
    }
    files = {
        "file": open(ipa_path,"rb")
    }
    print("😊  😊  😊  😊  😊  😊  Uploading... 😊  😊  😊  😊  😊  😊")
    resp = requests.post(url,data=data,files=files)
    try:
        json = resp.json()
        if json["code"] == 0:
            print("🎉  🎉  🎉  🎉  🎉  🎉   Uploaded Successfully!!!  🎉  🎉  🎉  🎉  🎉  🎉")
        else:
            print("❌  ❌  ❌  ❌  ❌  ❌ Uploaded Failued!!! ❌  ❌  ❌  ❌  ❌  ❌")
            print(json["message"])
    except Exception as error:
        print("❌  ❌  ❌  ❌  ❌  ❌ Uploaded Failued!!! ❌  ❌  ❌  ❌  ❌  ❌")
        print(error)

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:c:o:u",["help","scheme=","config=","option=","upload"])

        scheme_name = ""
        config = "Debug"
        export_option = "Development"

        for name, value in opts:
            if name in ("-h","--help"):
                print(tips)
                os._exit(0)
            elif name in ("-s","--scheme"):
                scheme_name = value
            elif name in ("-c","--config"):
                if value in ("Release","Debug"):
                    config = value 
                else:
                    print(tips)
                    os._exit(0)
            elif name in ("-o","--option"):
                if value in ("AppStore","AdHoc","Enterprise","Development"):
                    export_option = value
                else:
                    print(tips)
                    os._exit(0)
            
            elif name in ("-u","--upload"):
                upload_ipa()
                os._exit(0)

        build_ipa(scheme_name,config,export_option)

    except BaseException as err:
        print(tips)
        os._exit(0)
