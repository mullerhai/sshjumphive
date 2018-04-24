DSTL
====

https://github.com/mullerhai/sshjumphive

Note: this repo is not supported. License is MIT.

.. contents::

Object types
------------

Note that ssh_jump_hive  is an tools can  jump the jump machine  to connect hive get hive data to pandas dataframe:

- 0: hive_client  for  simple connect hive server  with  no jump server
- 1: Jump_Tunnel just  for  connect hive server with  jump server separete
- 2: SSH_Tunnel  for  get ssh tunnel channel


General approach
----------------

if  you want to use it ,you need  to know some things
for example these parameters [ jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelAPPport,localhost,localbindport]
for hive server  you also need to know params [localhost, hiveusername, hivepassword, localbindport,database, auth]
for query hive data you need to know params [ table, query_fileds_list, partions_param_dict, query_limit]

if your hive server has  jump server separete， you need do  like this
[
from ssh_jump_hive import Jump_Tunnel_HIVE
import pandas as pd
.....
    table = 'tab_client_label'
    partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
    query_fileds_list = ['gid', 'realname', 'card']
    querylimit = 1000
    jump=Jump_Tunnel(jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelhiveport,localhost,localbindport)
    df2=jump.get_JUMP_df(table,partions_param_dict,query_fileds_list,querylimit)
    print(df2.shape)
    print(df2.head(100))
    print(df2.columns())
]


UNet network with batch-normalization added, training with Adam optimizer with
a loss that is a sum of 0.1 cross-entropy and 0.9 dice loss.
Input for UNet was a 116 by 116 pixel patch, output was 64 by 64 pixels,
so there were 16 additional pixels on each side that just provided context for
the prediction.
Batch size was 128, learning rate was set to 0.0001
(but loss was multiplied by the batch size).
Learning rate was divided by 5 on the 25-th epoch
and then again by 5 on the 50-th epoch,
most models were trained for 70-100 epochs.
Patches that formed a batch were selected completely randomly across all images.
During one epoch, network saw patches that covered about one half
of the whole training set area. Best results for individual classes
were achieved when training on related classes, for example buildings
and structures, roads and tracks, two kinds of vehicles.

Augmentations included small rotations for some classes
(±10-25 degrees for houses, structures and both vehicle classes),
full rotations and vertical/horizontal flips
for other classes. Small amount of dropout (0.1) was used in some cases.
Alignment between channels was fixed with the help of
``cv2.findTransformECC``, and lower-resolution layers were upscaled to
match RGB size. In most cases, 12 channels were used (RGB, P, M),
while in some cases just RGB and P or all 20 channels made results
slightly better.


Validation
----------

Validation was very hard, especially for both water and both vehicle
classes. In most cases, validation was performed on 5 images
(6140_3_1, 6110_1_2, 6160_2_1, 6170_0_4, 6100_2_2), while other 20 were used
for training. Re-training the model with the same parameters on all 25 images
improved LB score.
