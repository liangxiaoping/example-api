#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 www.jd.com
#
# Author: liangxiaoping <liangxiaoping@jd.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import abc


class Storage():
    """ Base class for storage """
    __metaclass__ = abc.ABCMeta

    # message
    @abc.abstractmethod
    def create_message(self, context, *args, **kwargs):
        pass
