#!/bin/bash
# Copyright 2017-present, Dingmin Wang
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

set -e

# Configure download location
DOWNLOAD_PATH="$CSC_DATA"
if [ "$CSC_DATA" == "" ]; then
    echo "CSC_DATA not set; downloading to default path ('data')."
    DOWNLOAD_PATH="./CSC/data"
fi


# Download trained model
wget -O "$DOWNLOAD_PATH/kenlm_3.bin" "https://s3-us-west-2.amazonaws.com/kenlm-model/kenlm_3.bin"
#wget -O "$DOWNLOAD_PATH/kenlm_3.bin" "https://s3-us-west-2.amazonaws.com/kenlm-model/kenlm_3_small.bin"
