import os
a=0.2
b=440
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( a, b))
a=0.2
b=660
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( a, b))
