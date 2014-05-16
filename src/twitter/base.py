#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Twitter API
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Twitter API.
#
# Hive Twitter API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Twitter API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Twitter API. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import appier

from twitter import user

BASE_URL = "https://api.twitter.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

CLIENT_KEY = None
""" The default value to be used for the client key
in case no client key is provided to the api client """

CLIENT_SECRET = None
""" The secret value to be used for situations where
no client secret has been provided to the client """

REDIRECT_URL = "http://localhost:8080/oauth"
""" The redirect url used as default (fallback) value
in case none is provided to the api (client) """

class Api(
    appier.OAuth1Api,
    user.UserApi
):

    def __init__(self, *args, **kwargs):
        appier.OAuth1Api.__init__(self, *args, **kwargs)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.client_key = kwargs.get("client_key", CLIENT_KEY)
        self.client_secret = kwargs.get("client_secret", CLIENT_SECRET)
        self.redirect_url = kwargs.get("redirect_url", REDIRECT_URL)
        self.oauth_token = kwargs.get("oauth_token", None)
        self.oauth_token_secret = kwargs.get("oauth_token_secret", None)

    def oauth_request(self):
        url = self.base_url + "oauth/request_token"
        contents = self.post(url, oauth_callback = self.redirect_url)
        contents = contents.decode("utf-8")
        contents = appier.parse_qs(contents)
        self.oauth_token = contents["oauth_token"][0]
        self.oauth_token_secret = contents["oauth_token_secret"][0]

    def oauth_authorize(self, state = None):
        self.oauth_request()
        url = self.base_url + "oauth/authorize"
        values = dict(
            oauth_token = self.oauth_token
        )
        data = appier.urlencode(values)
        url = url + "?" + data
        return url

    def oauth_access(self, code, long = True):
        url = self.base_url + "oauth/access_token"
        contents = self.post(url)
        contents = contents.decode("utf-8")
        contents = appier.parse_qs(contents)
        self.oauth_token = contents["oauth_token"][0]
        self.oauth_token_secret = contents["oauth_token_secret"][0]
        self.trigger("oauth_token", self.oauth_token)
        return self.oauth_token
