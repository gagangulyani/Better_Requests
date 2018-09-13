"""
################################################################################
Requests Library Reborn...
(everything you needed with Requests!)

Written by :
- Gagan Gulyani

IG - gagan_gulyani

References:

    1. Progress Bar for Downloading:
https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads

    2. Requests Timeout Fix:
https://stackoverflow.com/questions/47375153/requests-get-in-python-giving-connection-timeout-error

    3. Calculating Percentage for downloading:
https://stackoverflow.com/questions/22169081/how-to-calculate-percentage-in-python

###############################################################################
"""

from os import rename,remove,mkdir,rmdir,system #for renaming and removing existing downloads
from os.path import basename,exists #for Downloading Stuff
from time import sleep as pause #For Delaying requests for rectifying errors
# import logging #For Maintaning logs
from json import dumps,loads #For Managing Custom Headers

try:
    import requests
except ImportError:
    print ("\nYou need \"requests\" Library installed in your system.\n(Use \"pip install requests\")")

try:
    from fake_useragent import UserAgent
except ImportError:
    print ("\nYou need \"fake_useragent\" Library installed in your system.\n(Use \"pip install fake_useragent\")")

from shutil import copyfileobj

class BRequests():

    """BRequests uses existing requests methods and Fake User Agent for Advanced Functionality!"""

    def __init__(self,custom_headers=None):
            self.page=requests.session()
            while True:
                try:
                    self.page.headers={"User-Agent":UserAgent().chrome}
                except fake_useragent.errors.FakeUserAgentError:
                    pass
                except Exception as e:
                    print(e)
                else:
                    break
            if custom_headers!=None:
                if "dict" in str(type(custom_headers)):
                    self.page.headers=custom_headers
                elif "str" in str(type(custom_headers)):
                    try:
                        self.page.headers=loads(custom_headers)
                    except Exception as e:
                        print ("\nUnable to Load Custom Headers")
                else:
                    print ("\nUnable to Load Custom Headers")

    def Get_Content(self,link,force_retrying=True,stream=None):
        """Gets Content from Site and retries for three time in case of failure.
            You can disable Force Retrying by adding "show_progress=True"
            in argument while calling the method.
        """
        if force_retrying!=True:
            if stream==True:
                page_=self.page.get(link,stream=stream,timeout=4)
            else:
                page_=self.page.get(link)
            return page_
        else:
            for i in range(3):
                try:
                    if stream==True:
                        page_=self.page.get(link,stream=stream,timeout=4)
                    else:
                        page_=self.page.get(link)
                    return page_
                    break

                except requests.exceptions.ConnectionError:
                    print ("\nConnection Error.. Retrying",end="")
                    for i in range(3):
                        print (".",end="")
                        pause(1)
                    print("\n\n")

                except requests.exceptions.ConnectTimeout:
                    print ("\nConnection Timeout.. Retrying",end="")
                    for i in range(3):
                        print (".",end="")
                        pause(1)
                    print("\n\n")

                except Exception as e:
                    print ("\nSomething Went Wrong..Error: {} Retrying".format(e),end="")
                    for i in range(3):
                        print (".",end="")
                        pause(1)
                    print("\n\n")
            else:
                print ("\nCan't Get Content :(\n")

    def Download(self,link,show_progress=True,rep_files=True):
        """This method downloads file you want from the link user needs to provide.
        If you want to see the progress bar...
        Make Sure to add "show_progress=True" in argument while calling the method.
        """
        def dload(link,file_name,show_progress):
            if show_progress==True:
                print ("\nDownloading {}..".format(file_name))

                file_=self.Get_Content(link,stream=True)

                if file_!=None:
                    if not file_.ok:
                        print ("\nCan't Download File!\nResponse:\n{}".format(file_.content))
                    else:
                        total_length=file_.headers.get('content-length')
                        if total_length is None:
                            print ("\nCan't Show Progress Bar while Downloading it.. :|")
                        else:
                            with open(file_name,"wb") as f:
                                dl = 0
                                per=0.0
                                total_length = int(total_length)
                                for i in range(3):
                                    try:
                                        for data in file_.iter_content(chunk_size=4096):
                                            dl += len(data)
                                            f.write(data)
                                            done = int(50 * dl / total_length)
                                            per=100.0 * (dl/total_length)
                                            print(("%.2f" % per)+"% "+"[%s%s]" % ('=' * done, ' ' * (50-done)),end="\r")
                                        print ("\nFile Downloaded Successfully!\n")

                                    except requests.exceptions.ConnectionError:
                                        print ("\nConnection Error.. Retrying",end="")
                                        for i in range(3):
                                            print (".",end="")
                                            pause(1)
                                        print("\n\n")

                                    except requests.exceptions.ConnectTimeout:
                                        print ("\nConnection Timeout.. Retrying",end="")
                                        for i in range(3):
                                            print (".",end="")
                                            pause(1)
                                        print("\n\n")

                                    except Exception as e:
                                        print ("\nSomething Went Wrong..Error: {} Retrying".format(e),end="")
                                        for i in range(3):
                                            print (".",end="")
                                            pause(1)
                                        print("\n\n")
                else:
                    print ("Can't Download File! :(")
            else:
                print("\nDownloading file..")
                with open(file_name,"wb") as f:
                    f.write(file_.raw)
                print ("\nFile Downloaded Successfully!")

        file_name=basename(link)

        if "?" in file_name:
            file_name=file_name.split("?")[0]

        dload(link,file_name,show_progress)
