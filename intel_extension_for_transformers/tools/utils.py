#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility."""

import importlib
import sys
import torch
import warnings
if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

try:
    import habana_frameworks.torch.hpu as hthpu
    is_hpu_available = True
except ImportError:
    is_hpu_available = False

def supported_gpus():
    return ['flex', 'max', 'arc']

def get_gpu_family():
    """Get gpu device family info.

    Return 'flex'|'max'|'arc'| 'no_gpu'| assert

    Note, this function need to import intel_extension_for_pytorch


    Additional info (common gpu name):
      'Intel(R) Data Center GPU Flex 170'
      'Intel(R) Data Center GPU Max 1100'
      'Intel(R) Arc(TM) A770 Graphics'
    """

    import intel_extension_for_pytorch as ipex
    if not (hasattr(torch, "xpu") and torch.xpu.is_available()):
        return 'no_gpu'

    name = torch.xpu.get_device_name()
    if torch.xpu.has_xmx() and torch.xpu.has_2d_block_array():
        return "PVC"
    elif torch.xpu.has_xmx() and not torch.xpu.has_2d_block_array():
        return "ARC"
    elif not torch.xpu.has_xmx() and not torch.xpu.has_2d_block_array():
        return "MTL"
    else:
        warnings.warn("Unverified GPU device: {}".format(name))
        return name

_ipex_available = importlib.util.find_spec("intel_extension_for_pytorch") is not None
_ipex_version = "N/A"
if _ipex_available:
    try:
        _ipex_version = importlib_metadata.version("intel_extension_for_pytorch")
    except importlib_metadata.PackageNotFoundError:
        _ipex_available = False

def is_ipex_available():
    return _ipex_available

_autoround_available = importlib.util.find_spec("auto_round") is not None
_autoround_version = "N/A"
if _autoround_available:
    try:
        _autoround_version = importlib_metadata.version("auto_round")
    except importlib_metadata.PackageNotFoundError:
        _autoround_available = False

def is_autoround_available():
    return _autoround_available

def get_device_type():
    if torch.cuda.is_available():
        device = "cuda"
    elif is_hpu_available:
        device = "hpu"
    elif is_ipex_available() and torch.xpu.is_available():
        device = "xpu"
    else:
        device = "cpu"
    return device
