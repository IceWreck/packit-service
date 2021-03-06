# MIT License
#
# Copyright (c) 2019 Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from http import HTTPStatus
from logging import getLogger

try:
    from flask_restx import Namespace, Resource
except ModuleNotFoundError:
    from flask_restplus import Namespace, Resource

from packit_service.models import WhitelistModel


logger = getLogger("packit_service")

ns = Namespace("whitelist", description="Whitelisted FAS accounts")


@ns.route("")
class WhiteList(Resource):
    @ns.response(HTTPStatus.OK.value, "OK, whitelist follows")
    def get(self):
        """List all Whitelisted FAS accounts"""
        return [account.to_dict() for account in WhitelistModel.get_all()]


@ns.route("/<string:login>")
@ns.param("login", "Account login")
class WhiteListItem(Resource):
    @ns.response(HTTPStatus.OK.value, "OK, whitelisted account details follow")
    @ns.response(HTTPStatus.NO_CONTENT.value, "login not in whitelist")
    def get(self, login):
        """A specific whitelist item details"""
        account = WhitelistModel.get_account(login)
        return account.to_dict() if account else ("", HTTPStatus.NO_CONTENT.value)
