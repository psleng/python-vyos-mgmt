# Copyright (c) 2016 Hochikong

from pxssh import pxssh
from .mgmt_common import messenger


class Router(object):
    def __init__(self, address, cred):
        """Initial a router object

        :param address: Router address,example:'192.168.10.10'
        :param cred: Router user and password,example:'vyos:vyos'
        """
        self.__address = address
        self.__cred = list(cred)
        self.__divi = self.__cred.index(":")
        self.__username = ''.join(self.__cred[:self.__divi])
        self.__passwd = ''.join(self.__cred[self.__divi+1:])
        self.__conn = pxssh()
        self.__status = {"status": None, "commit": None, "save": None, "configure": None}
        self.__basic_string = {0: 'set ', 1: 'delete '}

    def status(self):
        """Check the router object inner status

        :return: A python dictionary include the status of the router object
        """
        return self.__status

    def login(self):
        """Login the router

        :return: A message or an error
        """
        try:
            if self.__conn.login(self.__address, self.__username, self.__passwd) is True:
                self.__status["status"] = "login"
                return "Result : Login successfully."
            else:
                return "Error : Connect Failed."
        except Exception as e:
            return e

    def logout(self):
        """Logout the router

        :return: A message or an error
        """
        try:
            self.__conn.close()
            self.__status["status"] = "logout"
            self.__status["configure"] = None
            self.__conn = pxssh()
            return "Result : Logout successfully."
        except Exception as e:
            return e

    def configure(self):
        """Enter the VyOS configure mode

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] is not "Yes":
                    self.__conn.sendline("configure")
                    self.__conn.prompt(0)
                    self.__conn.set_unique_prompt()
                    self.__status["configure"] = "Yes"
                    return "Result : Active configure mode successfully."
                else:
                    return "Error : In configure mode now!"
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def commit(self):
        """Commit the configuration changes

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if self.__status["commit"] is None:
                        return "Error : You don't need to commit."
                    if self.__status["commit"] == "No":
                        self.__conn.sendline("commit")
                        self.__conn.prompt()
                        self.__status["commit"] = "Yes"
                        return "Result : Commit successfully."
                    else:
                        return "Error : You have committed!"
                else:
                    return "Error : Router not in configure mode!"
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def save(self):
        """Save the configuration after commit

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if self.__status["commit"] == "Yes":
                        if self.__status["save"] is None:
                            return "Error : You don't need to save."
                        if self.__status["save"] == "No":
                            self.__conn.sendline("save")
                            self.__conn.prompt(0)
                            self.__status["save"] = "Yes"
                            return "Result : Save successfully."
                        else:
                            return "Error : You have saved!"
                    elif self.__status["commit"] is None:
                        return "Error : You don't need to save."
                    else:
                        return "Error : You need to commit first!"
                else:
                    return "Error : Router not in configure mode!"
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def exit(self, force=False):
        """Exit VyOS configure mode

        :param force: True or False
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if force is True:
                        self.__conn.sendline("exit discard")
                        self.__conn.prompt()
                        self.__status["configure"] = "No"
                        self.__status["save"] = None
                        self.__status["commit"] = None
                        return "Result : Exit configure mode successfully."
                    else:
                        if self.__status["commit"] == "Yes":
                            if self.__status["save"] == "Yes":
                                self.__conn.sendline("exit")
                                self.__conn.prompt()
                                self.__status["configure"] = "No"
                                self.__status["save"] = None
                                self.__status["commit"] = None
                                return "Result : Exit configure mode successfully."
                            else:
                                return "Error : You should save first."
                        elif self.__status["commit"] is None:
                            self.__conn.sendline("exit")
                            self.__conn.prompt()
                            self.__status['configure'] = "No"
                            return "Result : Exit configure mode successfully."
                        else:
                            return "Error : You should commit first."
                else:
                    return "Error : You are not in configure mode,need not exit."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def set(self, config):
        """Basic 'set' method,execute the set command in VyOS

        :param config: A configuration string.
                       e.g. 'protocols static route ... next-hop ... distance ...'
        :return: A message or an error
        """
        full_config = self.__basic_string[0] + config
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = messenger(self.__conn, full_config)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def delete(self, config):
        """Basic 'delete' method,execute the delete command in VyOS

        :param config: A configuration string.
                               e.g. 'protocols static route ... next-hop ... distance ...'
        :return: A message or an error
        """
        full_config = self.__basic_string[1] + config
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = messenger(self.__conn, full_config)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e